# Peca do robo: o tempo de cada palavra da narracao (faster-whisper small). Uso: python fabrica/palavras.py 02
# 09/11: a narracao do 02 passou de 25 min e o Whisper inteiro passava de 10 min (o terminal cortava). Agora vai em
# pedacos de uns 4 min, cortados sempre na pausa entre duas falas (o _junta do narracao.py diz onde cada fala comeca),
# e cada pedaco fica guardado: se parar no meio, na proxima vez continua de onde parou.
import json, os, subprocess, sys
from faster_whisper import WhisperModel
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
NN = sys.argv[1]
MP3 = f"{P}/teste-vozes/NARRACAO-video-{NN}.mp3"; JUNTA = f"{P}/teste-vozes/pedacos-video-{NN}/_junta"
def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
total = dur(MP3)
# onde cortar: o fim de cada fala (q0.wav, q1.wav... ja com a pausa), juntando ate dar uns 4 min
cortes, t, i = [0.0], 0.0, 0
while os.path.exists(f"{JUNTA}/q{i}.wav"):
    t += dur(f"{JUNTA}/q{i}.wav"); i += 1
    if t - cortes[-1] >= 240 and t < total - 30: cortes.append(round(t - 0.15, 2))  # 0,15 s antes do fim: ainda no silencio
cortes.append(total)
CAD = f"{P}/fabrica/saida/_palavras-{NN}"; os.makedirs(CAD, exist_ok=True)
m = None; out = []
for a, b in zip(cortes, cortes[1:]):
    cf = f"{CAD}/{os.path.getsize(MP3)}-{a:.2f}-{b:.2f}.json"
    if os.path.exists(cf): ws = json.load(open(cf, encoding="utf-8"))
    else:
        if m is None: m = WhisperModel("small", device="cpu", compute_type="int8")
        tmp = f"{CAD}/_trecho.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.2f}", "-to", f"{b:.2f}", "-i", MP3, "-ac", "1", "-ar", "16000", "-y", tmp], check=True)
        seg, _ = m.transcribe(tmp, language="pt", word_timestamps=True, vad_filter=False)
        ws = [[round(w.start + a, 2), round(w.end + a, 2), w.word.strip()] for s in seg for w in s.words]
        json.dump(ws, open(cf, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"trecho {a / 60:.1f} a {b / 60:.1f} min: {len(ws)} palavras", flush=True)
    out += ws
json.dump(out, open(f"{P}/fabrica/saida/{NN}-palavras.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), "palavras")
