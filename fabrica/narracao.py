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
for enc in glob.glob(PASTA + "/**/parte-*.enc", recursive=True):
    n = re.search(r"parte-(\d+)\.enc", enc).group(1); wav = f"{PASTA}/p{n}.wav"
    if not os.path.exists(wav) or os.path.getmtime(enc) > os.path.getmtime(wav):
        subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-in", enc, "-out", wav, "-pass", "env:VOZ_SENHA"],
                       check=True, env={**os.environ, "VOZ_SENHA": env["VOZ_SENHA"]})
# 2. confere ouvindo e junta
if CONFERIR:
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
def norm(s):
    s = unicodedata.normalize("NFKD", s.lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", " ", s).split()
ruins = []; lista = open(TMP + "/lista.txt", "w")
for i, txt in enumerate(textos):
    f = f"{PASTA}/p{i}.wav"
    if not os.path.exists(f): ruins.append([i, "faltou"]); continue
    if CONFERIR:
        seg, _ = m.transcribe(f, language="pt")
        ouviu = " ".join(s.text for s in seg)
        a, b = norm(txt.replace("FinMoovi", "Fin Muvi")), norm(ouviu)
        sim = difflib.SequenceMatcher(None, a, b).ratio()
        if sim < 0.80 or len(b) > len(a) * 1.15 + 1:
            ruins.append([i, f"sim={sim:.2f} palavras {len(a)}->{len(b)} | {ouviu.strip()[:160]}"])
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
