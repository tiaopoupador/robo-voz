# Gera UMA parte do texto com a voz clonada. Uso: python gerar.py ref.wav <numero_da_parte> saida.wav
import sys, time, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

ref, parte, saida = sys.argv[1], int(sys.argv[2]), sys.argv[3]
arq = sys.argv[4] if len(sys.argv) > 4 else "textos.txt"
texto = open(arq, encoding="utf-8").read().splitlines()[parte]
# o roteiro escreve "Tião" normal; para a voz sair certa escreve-se "Tchião" (escolha do Ed, 03/11/2026)
texto = texto.replace("Tiãão", "Tião").replace("TIÃO", "Tião").replace("Tião", "Tchião")
# pronuncia escolhida pelo Ed de ouvido (04/11/2026): o roteiro escreve normal, a voz le assim
import re
FALA = [(r"FinMoovi", "Fin Múvi"), (r"picapes", "pikápis"), (r"picape", "pikápi"), (r"Picape", "Pikápi"),
        (r"setecentos", "sete centos"), (r"Setecentos", "Sete centos"),
        (r"IPVA", "i pê vê á"),
        (r"quilômetros", "quilôometros"), (r"quilômetro", "quilôometro"),
        (r"opções", "ôpissões"), (r"Opções", "Ôpissões"), (r"opção", "ôpissão"), (r"Opção", "Ôpissão"),
        # Ed, 08/11/2026: «o correto é falar nótinhas (...) o certo é pão de fôrma»
        (r"notinha", "nótinha"), (r"Notinha", "Nótinha"), (r"pão de forma", "pão de fôrma")]
for a, b in FALA:
    texto = re.sub(a, b, texto)
t0 = time.time()
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
print("MEDIDA modelo carregado em", round(time.time() - t0), "s", flush=True)
t = time.time()
w = m.generate(texto, language_id="pt", audio_prompt_path=ref, exaggeration=0.5, cfg_weight=0.5, temperature=0.8)
gasto = time.time() - t
dur = w.shape[1] / m.sr
ta.save(saida, w, m.sr)
print(f"MEDIDA parte {parte}: {dur:.1f} s de voz em {gasto:.0f} s de maquina ({gasto/dur:.1f} s por segundo de voz)", flush=True)
