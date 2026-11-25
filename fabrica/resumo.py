# 25/11/2026 (Ed: «De cada video longo vc cria um resumo com os personagens, mas tudo muito sensacionalista, com muito clickbait»)
# O 2.º Short de cada longo: um resumo de novela em ~50 s, com voz nova (o texto em robo-voz/resumo-NN.txt, uma frase forte por
# linha, gravado de graça na nuvem pelo voz-teste.yml) e as cenas do próprio longo com a turma. NUNCA conta o fim (a resposta,
# a virada): mostra o começo e manda ver o longo (regra da novela, canal-dark novela.md).
# No cenas.py: RESUMO = [[segundo onde começa cada cena no VIDEO-NN.mp4, ...] por linha do resumo-NN.txt], RESUMO_TOPO, RESUMO_EMOJI.
# Uso: python fabrica/resumo.py 05 <pasta com parte-N.enc> [--sem-drive]
import glob, importlib, json, os, re, subprocess, sys
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/.."); sys.path.insert(0, P)
from fabrica import vertical
NN, PASTA = sys.argv[1], sys.argv[2]
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
env = dict(l.strip().split("=", 1) for l in open(P + "/acessos.env", encoding="utf-8") if "=" in l and not l.startswith("#"))
textos = [l for l in open(f"{P}/robo-voz/resumo-{NN}.txt", encoding="utf-8").read().splitlines() if l.strip()]
assert len(C.RESUMO) == len(textos), f"RESUMO tem {len(C.RESUMO)} linhas e o resumo-{NN}.txt tem {len(textos)}"
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
# 1. abre a voz (a senha fica só dentro do programa)
for enc in [e for e in glob.glob(PASTA + "/**/parte-*.enc", recursive=True) if not e.endswith(".json.enc")]:
    n = re.search(r"parte-(\d+)\.enc", enc).group(1)
    subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-in", enc, "-out", f"{PASTA}/p{n}.wav",
                    "-pass", "env:VOZ_SENHA"], check=True, env={**os.environ, "VOZ_SENHA": env["VOZ_SENHA"]})
# 2. junta as falas com um respiro curto e põe as palavras no tempo (cada palavra pelo tamanho dela, dentro da sua fala)
RESP = 0.25
lista, t, palavras, trechos = [], 0.0, [], []
for i, txt in enumerate(textos):
    wav = f"{PASTA}/p{i}.wav"; d = dur(wav); lista.append(wav)
    leg = txt  # a legenda mostra o número («R$ 189 mil»), a voz diz por extenso (RESUMO_TROCAS no cenas.py)
    for de, para in getattr(C, "RESUMO_TROCAS", {}).items(): leg = leg.replace(de, para)
    ws = leg.split(); peso = [len(w) + 2 for w in ws]; tot = sum(peso); a = t + 0.08
    for w, p in zip(ws, peso):
        b = a + (d - 0.2) * p / tot; palavras.append([round(a, 2), round(b, 2), w]); a = b
    # as cenas desta fala: os trechos do longo dividem o tempo dela por igual
    cenas = C.RESUMO[i]; cada = (d + RESP) / len(cenas)
    trechos += [(ini, ini + cada) for ini in cenas]
    t += d + RESP
T = t
pasta = f"{P}/fabrica/saida/_resumo-{NN}"; os.makedirs(pasta, exist_ok=True)
with open(f"{pasta}/lista.txt", "w", encoding="utf-8") as f:
    for w in lista: f.write(f"file '{os.path.abspath(w)}'\n")
# a voz inteira: cada fala seguida de um respiro
partes = "".join(f"[{k}:a]apad=pad_dur={RESP}[s{k}];" for k in range(len(lista)))
subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", w] for w in lista), []), "-filter_complex",
                partes + "".join(f"[s{k}]" for k in range(len(lista))) + f"concat=n={len(lista)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[a]",
                "-map", "[a]", "-ar", "48000", f"{pasta}/voz.wav"], check=True)
OUT = f"{P}/videos-prontos/RESUMO-{NN}.mp4"
total = vertical.montar(f"{P}/videos-prontos/VIDEO-{NN}.mp4", trechos, palavras, T, C.RESUMO_TOPO, OUT,
                        emoji=getattr(C, "RESUMO_EMOJI", "1f92f"), voz=f"{pasta}/voz.wav", pasta=pasta,
                        musica=(f"{P}/render/public/v{NN}/trilha.mp3", getattr(C, "RESUMO_MUSICA", 0.0)))  # a trilha sem a narração
print(f"Resumo {NN}: {total:.1f} s -> {OUT}")
if "--sem-drive" not in sys.argv:
    from fabrica import drive
    print("no Drive:", drive.guardar(NN, OUT))
