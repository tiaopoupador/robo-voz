# Peca do robo: o tempo de cada palavra da narracao (faster-whisper small). Uso: python fabrica/palavras.py 02
import json, os, sys
from faster_whisper import WhisperModel
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
NN = sys.argv[1]
m = WhisperModel("small", device="cpu", compute_type="int8")
seg, _ = m.transcribe(f"{P}/teste-vozes/NARRACAO-video-{NN}.mp3", language="pt", word_timestamps=True, vad_filter=False)
out = [[round(w.start, 2), round(w.end, 2), w.word.strip()] for s in seg for w in s.words]
json.dump(out, open(f"{P}/fabrica/saida/{NN}-palavras.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), "palavras")
