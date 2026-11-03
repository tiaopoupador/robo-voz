# Gera UMA parte do texto com a voz clonada. Uso: python gerar.py ref.wav <numero_da_parte> saida.wav
import sys, time, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

ref, parte, saida = sys.argv[1], int(sys.argv[2]), sys.argv[3]
texto = open("textos.txt", encoding="utf-8").read().splitlines()[parte]
t0 = time.time()
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
print("MEDIDA modelo carregado em", round(time.time() - t0), "s", flush=True)
t = time.time()
w = m.generate(texto, language_id="pt", audio_prompt_path=ref, exaggeration=0.5, cfg_weight=0.5, temperature=0.8)
gasto = time.time() - t
dur = w.shape[1] / m.sr
ta.save(saida, w, m.sr)
print(f"MEDIDA parte {parte}: {dur:.1f} s de voz em {gasto:.0f} s de maquina ({gasto/dur:.1f} s por segundo de voz)", flush=True)
