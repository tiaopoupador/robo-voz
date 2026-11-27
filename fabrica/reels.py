# 25/11/2026 (Ed: «A partir desse já é possivel criar o short, aquele do gancho do inicio que comentamos!»)
# O gancho de cada longo (do 1.º segundo até antes do «Vamos começar?») vira um Short em pé, com o som do próprio longo.
# A tela (frase isca, emoji, faixa correndo, legenda grande, cartão final) vive no fabrica/vertical.py.
# Plano: pesquisa/PLANO-REELS-DO-GANCHO.md. No cenas.py: REELS_TOPO (a frase isca) e REELS_EMOJI (código do emoji).
# Uso: python fabrica/reels.py 05 [--sem-drive]
import importlib, json, os, sys
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/.."); sys.path.insert(0, P)
from fabrica import vertical
NN = sys.argv[1]
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
W = json.load(open(f"{P}/fabrica/saida/{NN}-palavras.json", encoding="utf-8"))
# 27/11: do 06 em diante a fala 0 e o «No episodio anterior» (REELS_DE) e o VIDEO-NN.mp4 sai acelerado (RITMO).
# Este programa ainda corta do segundo 0 com os tempos da voz normal: parar antes de sair um Reels errado.
if getattr(C, "REELS_DE", 0) or getattr(C, "RITMO", 1.0) != 1.0:
    raise SystemExit("ERRO: falta ensinar o reels.py a comecar na fala REELS_DE e a usar o RITMO (27/11). Nao gerar ate la.")
fim_i = next(i for i in range(len(W) - 1) if W[i][2].lower().startswith("vamos") and W[i + 1][2].lower().startswith("começar"))
T = W[fim_i - 1][1] + 0.25          # um respiro depois do «...puxa a cadeira.»
OUT = f"{P}/videos-prontos/REELS-{NN}.mp4"
total = vertical.montar(f"{P}/videos-prontos/VIDEO-{NN}.mp4", [(0, T)], W[:fim_i], T, getattr(C, "REELS_TOPO", C.TITULO), OUT,
                        emoji=getattr(C, "REELS_EMOJI", "1f631"), pasta=f"{P}/fabrica/saida/_reels-{NN}")
print(f"Reels {NN}: {total:.1f} s -> {OUT}")
if "--sem-drive" not in sys.argv:
    from fabrica import drive
    print("no Drive:", drive.guardar(NN, OUT))
