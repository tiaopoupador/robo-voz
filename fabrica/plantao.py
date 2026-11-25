# 25/11/2026: os Shorts do «Plantão do Tião: o que muda no seu bolso» (3 por dia; Ed: «quero 3 shorts por dia desse novo jeito!»).
# Caminho de cada dia:
#   1. python pesquisa/quentes.py              -> as notícias quentes (Shorts que explodem, Google Trends, Agência Brasil)
#   2. o texto (robo-voz/plantao-AAAA-MM-DD.txt, 1 frase forte por linha) e o plantao/AAAA-MM-DD/shorts.json (quais linhas são de
#      qual Short e o quadro que entra em cada palavra), com a ficha de fontes oficiais ao lado (fontes.md)
#   3. a voz de graça na nuvem (voz-teste.yml, arquivo=plantao-AAAA-MM-DD.txt)
#   4. python fabrica/plantao.py AAAA-MM-DD <pasta da voz>   -> junta a voz de cada Short, põe as palavras no tempo, escreve o props.json
#      e manda para a nuvem (robo-voz/plantao/AAAA-MM-DD, a voz cifrada) e liga o plantao.yml, que gera os vídeos e guarda no Drive
#      (Tiao Poupador/robo/plantao/AAAA-MM-DD). --local só prepara, sem mandar.
import glob, json, os, re, shutil, subprocess, sys
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/.."); sys.path.insert(0, P)
DIA, PASTA = sys.argv[1], sys.argv[2]
env = dict(l.strip().split("=", 1) for l in open(P + "/acessos.env", encoding="utf-8") if "=" in l and not l.startswith("#"))
SPEC = json.load(open(f"{P}/plantao/{DIA}/shorts.json", encoding="utf-8"))
textos = [l for l in open(f"{P}/{SPEC['texto']}", encoding="utf-8").read().splitlines() if l.strip()]
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
cripta = lambda a, b, d="-d": subprocess.run(["openssl", "enc", d, "-aes-256-cbc", "-pbkdf2", "-iter", "200000", *(["-salt"] if d == "-e" else []),
                                             "-in", a, "-out", b, "-pass", "env:VOZ_SENHA"], check=True, env={**os.environ, "VOZ_SENHA": env["VOZ_SENHA"]})
# 1. abre a voz (a senha fica só dentro do programa)
for enc in [e for e in glob.glob(PASTA + "/**/parte-*.enc", recursive=True) if not e.endswith(".json.enc")]:
    cripta(enc, f"{PASTA}/p{re.search(r'parte-(\d+)\.enc', enc)[1]}.wav")
# legenda: o número aparece em algarismo (a voz diz por extenso)
TROCAS = [("cinquenta e seis bilhões de reais", "R$ 56 bilhões"), ("vinte por cento", "20%"), ("dois mil e vinte e sete", "2027"),
          ("quatro para dois bilhões de reais", "R$ 4 para R$ 2 bilhões"), ("décimo terceiro", "13º"), ("dois por cento", "2%"),
          ("cinco reais e noventa e um centavos", "R$ 5,91"), ("noventa e um dólares", "US$ 91"), ("dez bilhões e meio de reais", "R$ 10,5 bilhões"),
          ("vinte e quatro de novembro", "24/11"), ("sete de dezembro", "7/12"), ("primeiro a 7/12", "1º a 7/12"), ("um salário mínimo", "1 salário mínimo")]
RESP = 0.22
saida_nuvem = f"{P}/robo-voz/plantao/{DIA}"; os.makedirs(saida_nuvem, exist_ok=True)
for sh in SPEC["shorts"]:
    pub = f"{P}/render/public/plantao/{DIA}/{sh['id']}"; os.makedirs(pub, exist_ok=True)
    t, palavras, ini_linha, wavs = 0.35, [], [], []   # 0,35 s: o «alerta» do Plantão toca antes da voz
    for k, n in enumerate(sh["linhas"]):
        wav = f"{PASTA}/p{n}.wav"; d = dur(wav); wavs.append(wav); ini_linha.append([])
        ws = textos[n].split(); peso = [len(w) + 2 for w in ws]; tot = sum(peso); a = t + 0.06
        for w, p_ in zip(ws, peso):
            b = a + (d - 0.15) * p_ / tot; ini_linha[-1].append(a); palavras.append([round(a, 2), round(b, 2), w]); a = b
        t += d + RESP
    fim = t
    quando = lambda q: round(ini_linha[q["linha"]][min(q.get("palavra", 0), len(ini_linha[q["linha"]]) - 1)], 2)
    quadros = []
    for q in sh["quadros"]:
        q2 = {k: v for k, v in q.items() if k not in ("linha", "palavra")}; q2["ini"] = max(0, quando(q) - 0.15)
        if q.get("itens"):
            q2["itens"] = [{"t": it["t"], "ok": it["ok"], **({"em": round(max(0.3, quando(it) - q2["ini"]), 2)} if "linha" in it else {})} for it in q["itens"]]
        quadros.append(q2)
    # a legenda com os números em algarismo: junta as palavras de novo, troca, e reparte o tempo de cada trecho
    leg = []
    for k, n in enumerate(sh["linhas"]):
        pal = [w for w in palavras if True][sum(len(textos[m].split()) for m in sh["linhas"][:k]):][:len(textos[n].split())]
        frase = textos[n]
        for de, para in TROCAS: frase = frase.replace(de, para)
        ws = frase.split(); a, b = pal[0][0], pal[-1][1]; peso = [len(w) + 2 for w in ws]; tot = sum(peso); x = a
        for w, p_ in zip(ws, peso):
            y = x + (b - a) * p_ / tot; leg.append([round(x, 2), round(y, 2), w]); x = y
    # a voz deste Short: um respiro depois de cada fala
    filtro = "".join(f"[{k}:a]apad=pad_dur={RESP}[s{k}];" for k in range(len(wavs)))
    filtro += "".join(f"[s{k}]" for k in range(len(wavs))) + f"concat=n={len(wavs)}:v=0:a=1,adelay=350|350,loudnorm=I=-15:TP=-1.5[a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", w] for w in wavs), []), "-filter_complex", filtro, "-map", "[a]", "-ar", "48000",
                    f"{pub}/voz.wav"], check=True)
    props = {"voz": f"plantao/{DIA}/{sh['id']}/voz.wav", "musica": "musica/Interloper.mp3", "palavras": leg, "quadros": quadros, "fim": round(fim, 2),
             "data": SPEC["data"], "rotulo": "SEGUE", "faixa": "SEGUE O PLANTÃO DO TIÃO   •   TODO DIA, O QUE MUDA NO SEU BOLSO   •   DEIXA O SEU LIKE!   •   "}
    json.dump(props, open(f"{pub}/props.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.makedirs(f"{saida_nuvem}/{sh['id']}", exist_ok=True)
    shutil.copy(f"{pub}/props.json", f"{saida_nuvem}/{sh['id']}/props.json")
    cripta(f"{pub}/voz.wav", f"{saida_nuvem}/{sh['id']}/voz.enc", "-e")
    print(f"{sh['id']}: {fim:.1f} s, {len(quadros)} quadros")
if "--local" not in sys.argv:
    R = f"{P}/robo-voz"
    subprocess.run(["bash", f"{P}/fabrica/para-nuvem.sh"], check=True, cwd=P)
    subprocess.run(["git", "add", f"plantao/{DIA}"], check=True, cwd=R)
    subprocess.run(["git", "commit", "-qm", f"plantao {DIA}"], cwd=R); subprocess.run(["git", "push", "-q"], check=True, cwd=R)
    subprocess.run(["gh", "workflow", "run", "plantao.yml", "-R", "tiaopoupador/robo-voz", "-f", f"dia={DIA}"], check=True,
                   env={**os.environ, "GH_TOKEN": env["GITHUB_TIAO"]})
    print("a nuvem está gerando os vídeos: Drive > Tiao Poupador > robo > plantao >", DIA)
