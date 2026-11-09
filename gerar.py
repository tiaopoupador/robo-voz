# Gera UMA fala do roteiro com a voz clonada. Uso: python gerar.py ref.wav <numero_da_parte> saida.wav [roteiro.txt]
#
# 09/11/2026 (Ed: «no 3:20 ele muda o idioma (...) a voz fica mais rapida», «ficou um zumbi fazendo barulho de zumbido de
# filme de terror», «fica picotando, o som some e volta»). O que estava errado e como ficou:
#   1. O gravador (Chatterbox) grava no maximo uns 40 s de uma vez. As falas 13 e 97 tinham 580 e 485 letras e sairam com
#      40,0 s certinhos: ele ACELEROU para caber, trocou de idioma e gemeu no fim. Agora cada FRASE e gravada sozinha
#      (pedacos de ate ~200 letras, sempre cortados no ponto final, nunca no meio da frase).
#   2. Cada frase e ESCUTADA aqui mesmo, logo depois de gravada (Whisper), e regravada com outra semente se:
#      a lingua nao for portugues, as palavras nao baterem, a velocidade sair fora do normal (a voz do Ed fala
#      uns 19 letras por segundo; acima de 23 = acelerou) ou houver som forte sem palavra (o "zumbi"), no meio ou no fim.
#   3. As frases se juntam com a pausa natural da pontuacao (ponto 0,45 s, virgula 0,25 s), com o silencio de verdade
#      entre elas. Nada e inserido no meio de uma frase (o antigo "respiro" do narracao.py picotava a fala).
# Sai: saida.wav e saida.json (o relatorio de cada frase: tentativas, nota, o que o Whisper ouviu).
import json, re, sys, time
import numpy as np, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

ref, parte, saida = sys.argv[1], int(sys.argv[2]), sys.argv[3]
arq = sys.argv[4] if len(sys.argv) > 4 else "textos.txt"
original = open(arq, encoding="utf-8").read().splitlines()[parte]

def falado(texto):
    # o roteiro escreve "Tião" normal; para a voz sair certa escreve-se "Tchião" (escolha do Ed, 03/11/2026)
    texto = texto.replace("Tiãão", "Tião").replace("TIÃO", "Tião").replace("Tião", "Tchião")
    # pronuncia escolhida pelo Ed de ouvido (04/11/2026): o roteiro escreve normal, a voz le assim
    FALA = [(r"FinMoovi", "Fin Múvi"), (r"picapes", "pikápis"), (r"picape", "pikápi"), (r"Picape", "Pikápi"),
            (r"setecentos", "sete centos"), (r"Setecentos", "Sete centos"),
            (r"IPVA", "i pê vê á"),
            (r"quilômetros", "quilôometros"), (r"quilômetro", "quilôometro"),
            (r"opções", "ôpissões"), (r"Opções", "Ôpissões"), (r"opção", "ôpissão"), (r"Opção", "Ôpissão"),
            # Ed, 08/11/2026: «o correto é falar nótinhas (...) o certo é pão de fôrma»
            (r"notinha", "nótínha"), (r"Notinha", "Nótínha"), (r"pão de forma", "pão de fôrma"), (r"(?<![a-zà-ú])de cor(?=[:,.!?])", "de cór")]
    for a, b in FALA: texto = re.sub(a, b, texto)
    return texto

# ---------- 1. as frases ----------
def frases(t, maxc=200):
    """corta no fim de frase; frase curta junta com a seguinte; frase longa demais corta na virgula"""
    ps = [p for p in re.split(r'(?<=[.!?:])["»”]?\s+', t.strip()) if p]
    out = []
    for p in ps:
        if len(p) > maxc + 60:  # frase enorme: corta na virgula mais perto do meio
            vs = [m.end() for m in re.finditer(r",\s", p)]
            if vs:
                c = min(vs, key=lambda x: abs(x - len(p) / 2)); out += [p[:c].strip(), p[c:].strip()]; continue
        out.append(p)
    grupos = []
    for p in out:
        if grupos and len(grupos[-1]) + len(p) < 90: grupos[-1] += " " + p
        else: grupos.append(p)
    return grupos

# ---------- 2. escutar ----------
import difflib, unicodedata
from faster_whisper import WhisperModel
try:
    from num2words import num2words
except ImportError: num2words = None
def norm(s):
    if num2words:
        s = re.sub(r"(\d+),(\d+)", lambda m: f"{m.group(1)} vírgula {m.group(2)}", s)
        s = re.sub(r"\d+", lambda m: num2words(int(m.group()), lang="pt_BR"), s.replace(".", " ").replace("R$", " reais "))
    s = unicodedata.normalize("NFKD", s.lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", " ", s).split()
SR_W = 16000
def nota(wav, sr, texto, whisper):
    """devolve (ok, motivo, dados). wav: tensor [1, n]"""
    a = ta.functional.resample(wav, sr, SR_W)[0].numpy().astype(np.float32)
    seg, info = whisper.transcribe(a, language=None, word_timestamps=True, vad_filter=False, beam_size=5)
    seg = list(seg); ws = [(w.start, w.end, w.word) for s in seg for w in s.words]
    ouviu = " ".join(s.text for s in seg).strip()
    d = {"ouviu": ouviu, "lingua": info.language, "prob": round(info.language_probability, 2), "dur": round(len(a) / SR_W, 2)}
    if info.language != "pt" or info.language_probability < 0.6: return False, f"lingua {info.language} ({info.language_probability:.2f})", d
    A, B = norm(texto.replace("Tchião", "Tião")), norm(ouviu)
    sim = difflib.SequenceMatcher(None, A, B).ratio(); d["sim"] = round(sim, 2)
    if sim < 0.82: return False, f"palavras nao batem ({sim:.2f})", d
    if not ws: return False, "sem palavras", d
    # energia em janelas de 20 ms
    fr = a[: len(a) // 320 * 320].reshape(-1, 320); r = np.sqrt((fr ** 2).mean(1)); voz = (r > 0.01).sum() * 0.02
    vel = len(texto) / max(voz, 0.1); d["letras_s"] = round(vel, 1)
    if len(texto) > 40 and vel > 23.0: return False, f"acelerou ({vel:.1f} letras/s)", d
    if len(texto) > 40 and vel < 13.0: return False, f"lento ou com som a mais ({vel:.1f} letras/s)", d
    # som forte sem palavra: no meio (buraco entre palavras > 0,7 s com energia) e depois da ultima palavra
    def forte(t0, t1):
        i0, i1 = int(t0 / 0.02), int(t1 / 0.02); return float((r[i0:i1] > 0.02).sum() * 0.02)
    for (s0, e0, _), (s1, e1, _) in zip(ws, ws[1:]):
        if s1 - e0 > 0.7 and forte(e0 + 0.15, s1 - 0.15) > 0.25: return False, f"som sem palavra no meio ({e0:.1f}-{s1:.1f} s)", d
    cauda = forte(ws[-1][1] + 0.15, len(a) / SR_W)
    if cauda > 0.25: return False, f"som depois da ultima palavra ({cauda:.2f} s)", d
    if forte(0, max(0, ws[0][0] - 0.15)) > 0.25: return False, "som antes da primeira palavra", d
    return True, "ok", d

# ---------- 3. aparar e juntar ----------
def aparar(w, sr):
    x = w[0].numpy(); j = int(0.02 * sr); n = len(x) // j
    r = np.sqrt((x[: n * j].reshape(n, j) ** 2).mean(1)); idx = np.where(r > 0.006)[0]
    if not len(idx): return w
    a, b = max(0, (idx[0] - 2) * j), min(len(x), (idx[-1] + 4) * j)
    y = x[a:b].copy(); k = int(0.012 * sr); y[:k] *= np.linspace(0, 1, k); y[-k:] *= np.linspace(1, 0, k)
    return torch.from_numpy(y).unsqueeze(0)

t0 = time.time()
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
whisper = WhisperModel("small", device="cpu", compute_type="int8")
print("MEDIDA modelos carregados em", round(time.time() - t0), "s", flush=True)
import os
RODADA = 7919 * (int(os.environ.get("GITHUB_RUN_ID", "0")) % 1000)  # cada rodada nova tenta outras sementes (regravar uma fala nao repete a mesma voz ruim)
rel, pedacos = {"parte": parte, "frases": []}, []
fs = frases(original)
for k, fr in enumerate(fs):
    melhor = None
    for tent in range(5):
        torch.manual_seed(1000 * parte + 17 * k + tent + RODADA)
        w = m.generate(falado(fr), language_id="pt", audio_prompt_path=ref, exaggeration=0.5, cfg_weight=0.5, temperature=0.8)
        ok, motivo, d = nota(w, m.sr, falado(fr), whisper)
        print(f"  frase {k + 1}/{len(fs)} tentativa {tent + 1}: {motivo} | {d.get('ouviu', '')[:90]}", flush=True)
        pontos = (2 if ok else 0) + d.get("sim", 0)
        if melhor is None or pontos > melhor[0]: melhor = (pontos, w, ok, motivo, d, tent + 1)
        if ok: break
    _, w, ok, motivo, d, nt = melhor
    rel["frases"].append({"texto": fr, "ok": ok, "motivo": motivo, "tentativas": nt, **d})
    pedacos.append((aparar(w, m.sr), fr))
sr = m.sr; partes = []
for i, (w, fr) in enumerate(pedacos):
    partes.append(w)
    if i < len(pedacos) - 1:
        pausa = 0.45 if re.search(r'[.!?:]["»”]?$', fr) else 0.25
        partes.append(torch.zeros(1, int(pausa * sr)))
tudo = torch.cat(partes, dim=1)
ta.save(saida, tudo, sr)
rel["ok"] = all(f["ok"] for f in rel["frases"]); rel["dur"] = round(tudo.shape[1] / sr, 2)
json.dump(rel, open(saida.rsplit(".", 1)[0] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"MEDIDA parte {parte}: {rel['dur']} s, {len(fs)} frases, {'TUDO OK' if rel['ok'] else 'COM AVISO'} em {time.time() - t0:.0f} s", flush=True)
