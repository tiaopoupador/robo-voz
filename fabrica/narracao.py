# Peca do robo: abre os pedacos da voz que o GitHub gravou, confere cada um ouvindo (Whisper) e junta a narracao.
# Uso: python fabrica/narracao.py 02 <pasta com parte-N/parte-N.enc ou pN.wav> [--sem-conferir]
# Sai em: teste-vozes/NARRACAO-video-NN.mp3 e a lista dos pedacos ruins (para regravar) em fabrica/saida/NN-voz-ruins.json
import difflib, glob, json, os, re, subprocess, sys, unicodedata
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
NN, PASTA = sys.argv[1], sys.argv[2]
CONFERIR = "--sem-conferir" not in sys.argv
env = dict(l.strip().split("=", 1) for l in open(P + "/acessos.env", encoding="utf-8") if "=" in l and not l.startswith("#"))
textos = open(f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
secoes = json.load(open(f"{P}/robo-voz/roteiro-{NN}-secoes.json"))
TMP = PASTA + "/_junta"; os.makedirs(TMP, exist_ok=True); os.makedirs(P + "/fabrica/saida", exist_ok=True)
# 1. abre os cifrados (a senha fica so dentro do programa)
for enc in [e for e in glob.glob(PASTA + "/**/parte-*.enc", recursive=True) if not e.endswith(".json.enc")]:
    n = re.search(r"parte-(\d+)\.enc", enc).group(1); wav = f"{PASTA}/p{n}.wav"
    if not os.path.exists(wav) or os.path.getmtime(enc) > os.path.getmtime(wav):
        subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-in", enc, "-out", wav, "-pass", "env:VOZ_SENHA"],
                       check=True, env={**os.environ, "VOZ_SENHA": env["VOZ_SENHA"]})
# 1b. 09/11: o relatorio de cada fala (o gerar.py novo ja escutou cada frase na nuvem e regravou as ruins)
for enc in glob.glob(PASTA + "/**/parte-*.json.enc", recursive=True):
    n = re.search(r"parte-(\d+)\.json\.enc", enc).group(1); js = f"{PASTA}/j{n}.json"
    if not os.path.exists(js) or os.path.getmtime(enc) > os.path.getmtime(js):
        subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-in", enc, "-out", js, "-pass", "env:VOZ_SENHA"],
                       check=True, env={**os.environ, "VOZ_SENHA": env["VOZ_SENHA"]})
# 2. confere ouvindo e junta
if CONFERIR:
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
def norm(s):
    s = unicodedata.normalize("NFKD", s.lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", " ", s).split()
# 08/11 (Ed: «Ela para vira o pacote, sem respiração» e «um som de zumbi no fundo da fala»):
# 1. RESPIRO: em cada ponto final, interrogação, exclamação e dois-pontos, a pausa tem de ter pelo menos 0,42 s
#    (vírgula: 0,18 s). Se o gravador emendou, o robô abre o silêncio no ponto mais quieto entre as duas palavras.
# 2. CAUDA: depois da última palavra não pode haver som (o gravador às vezes geme ou chia no fim). Corta no primeiro
#    silêncio depois da última palavra; se ainda houver som forte ali, a fala vai para a lista de regravar.
import numpy as np
SR = 24000
def ler(f): return np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]), dtype=np.float32).copy()
def rms(a, t0, t1): x = a[max(0, int(t0 * SR)):max(0, int(t1 * SR))]; return float(np.sqrt((x ** 2).mean())) if len(x) else 0.0
def quieto(a, t0, t1, j=0.01):
    """o instante mais silencioso entre t0 e t1"""
    best = (9, t0)
    for t in np.arange(t0, max(t0 + j, t1 - j), j): best = min(best, (rms(a, t, t + j), t))
    return best[1] + j / 2
def respirar(a, txt, ws):
    """ws: [(ini, fim, palavra)] do Whisper. Devolve (audio novo, quantas pausas abriu, aviso de cauda ou None)"""
    toks = txt.split(); A = [" ".join(norm(t)) for t in toks]; B = [" ".join(norm(w[2])) for w in ws]
    pos = {}
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if op == "equal":
            for d in range(i2 - i1): pos[i1 + d] = j1 + d
    cortes = []
    for i, t in enumerate(toks[:-1]):
        alvo = 0.42 if re.search(r"[.!?:][\"»”]?$", t) else 0.18 if re.search(r"[,;][\"»”]?$", t) else 0
        j = pos.get(i)
        if not alvo or j is None or j + 1 >= len(ws): continue
        gap = ws[j + 1][0] - ws[j][1]
        if gap < alvo: cortes.append((quieto(a, ws[j][1] - 0.03, ws[j + 1][0] + 0.03), alvo - max(0, gap)))
    aviso = None
    if ws:  # a cauda
        fim = ws[-1][1]; c = None
        for t in np.arange(fim - 0.05, len(a) / SR - 0.03, 0.01):
            if rms(a, t, t + 0.15) < 0.004: c = t + 0.03; break
        forte = sum(0.02 for t in np.arange(fim + 0.08, min(len(a) / SR, fim + 0.7), 0.02) if rms(a, t, t + 0.02) > 0.012)
        if forte > 0.3 and not re.search(r"\d", ws[-1][2]): aviso = f"som estranho depois da ultima palavra ({forte:.2f} s): regravar"
        if c is not None and c < len(a) / SR:
            n = int(c * SR); a = a[:n].copy(); k = min(len(a), int(0.04 * SR)); a[-k:] *= np.linspace(1, 0, k)
    for t, d in sorted(cortes, reverse=True):
        n = int(t * SR); a = np.concatenate([a[:n], np.zeros(int(d * SR), np.float32), a[n:]])
    return a, len(cortes), aviso
def gravar(a, f): subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-y", f], input=a.astype(np.float32).tobytes(), check=True)
ruins = []; lista = open(TMP + "/lista.txt", "w")
for i, txt in enumerate(textos):
    f = f"{PASTA}/p{i}.wav"
    if not os.path.exists(f): ruins.append([i, "faltou"]); continue
    # ja conferido antes (mesmo texto, mesmo arquivo de voz): usa o que ficou guardado e nao escuta de novo
    # 09/11: fala gravada pelo gerar.py novo (frase a frase, ja escutada na nuvem): entra como veio, sem "respiro"
    # inserido no meio (era isso que picotava a fala: silencio digital enfiado entre palavras).
    rel = f"{PASTA}/j{i}.json"
    if os.path.exists(rel):
        rj = json.load(open(rel, encoding="utf-8"))
        ruins += [[i, f"frase {k + 1}: {fr_['motivo']} | {fr_.get('ouviu', '')[:120]}"] for k, fr_ in enumerate(rj["frases"]) if not fr_["ok"]]
        CONFERIR_ESTA = False; marca = None
    else: marca = ""
    if marca is not None: marca = f"{TMP}/ok{i}.json"; chave = f"{os.path.getsize(f)}|{txt}"
    if marca is None: pass
    elif CONFERIR and os.path.exists(marca) and os.path.exists(f"{TMP}/r{i}.wav"):
        j = json.load(open(marca, encoding="utf-8"))
        if j.get("chave") == chave:
            ruins += j["ruins"]; f = f"{TMP}/r{i}.wav"; CONFERIR_ESTA = False
        else: CONFERIR_ESTA = True
    else: CONFERIR_ESTA = CONFERIR
    if CONFERIR_ESTA:
        antes = len(ruins)
        seg, _ = m.transcribe(f, language="pt", word_timestamps=True); seg = list(seg)
        ouviu = " ".join(s.text for s in seg)
        ws = [(w.start, w.end, w.word) for s_ in seg for w in s_.words]
        au, npausas, aviso = respirar(ler(f), txt, ws)
        if aviso: ruins.append([i, aviso])
        f = f"{TMP}/r{i}.wav"; gravar(au, f)
        if npausas: print(f"  fala {i}: abri {npausas} respiro(s)", flush=True)
        a, b = norm(txt.replace("FinMoovi", "Fin Muvi")), norm(ouviu)
        sim = difflib.SequenceMatcher(None, a, b).ratio()
        if sim < 0.80 or len(b) > len(a) * 1.15 + 1:
            ruins.append([i, f"sim={sim:.2f} palavras {len(a)}->{len(b)} | {ouviu.strip()[:160]}"])
        json.dump({"chave": chave, "ruins": ruins[antes:]}, open(marca, "w", encoding="utf-8"), ensure_ascii=False)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
    if dur >= 39.5: ruins.append([i, f"bateu no limite de 40 s do gravador: pode ter cortado ou inventado som no fim ({dur:.1f} s)"])
    pausa = 0.9 if secoes[i] else 0.35
    subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-af", f"apad=pad_dur={pausa}", "-ar", "24000", "-ac", "1", "-y", f"{TMP}/q{i}.wav"], check=True)
    lista.write(f"file 'q{i}.wav'\n")
lista.close()
json.dump(ruins, open(f"{P}/fabrica/saida/{NN}-voz-ruins.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RUINS", [r[0] for r in ruins])
for r in ruins: print(" ", r)
saida = f"{P}/teste-vozes/NARRACAO-video-{NN}.mp3"
# em DUAS etapas: juntar e normalizar numa so cortava o fim (06/11: deu 15 min em vez de 21)
subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", TMP + "/lista.txt", "-c", "copy", "-y", TMP + "/tudo.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-i", TMP + "/tudo.wav", "-af", "loudnorm=I=-16:TP=-1.5", "-c:a", "libmp3lame", "-q:a", "2", "-y", saida], check=True)
d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", saida]).decode())
print(f"duracao {int(d // 60)}m{int(d % 60):02d}s ->", saida)
