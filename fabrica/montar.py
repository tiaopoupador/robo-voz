# Peca do robo: monta os dados de QUALQUER video para o Remotion (render/src/nuvem.ts, composicao "Video").
# Uso: python fabrica/montar.py 02
# Entra: fabrica/videos/vNN/cenas.py, as imagens (img/ da Cloudflare e entrada/ do Ed), teste-vozes/NARRACAO-video-NN.mp3
#        e fabrica/saida/NN-palavras.json (tempo de cada palavra).
# Sai:   render/public/vNN/ (imagens, clipes, narracao, trilha) e render/public/vNN/props.json. Mais a lista de avisos.
import importlib, json, os, re, shutil, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
NN = sys.argv[1]
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
from fabrica.sincronia import alinhar, achar
V = f"{P}/fabrica/videos/v{NN}"; IMG_CF, ENT = V + "/img", V + "/entrada"
if "--sem-team" not in sys.argv:  # o que o Ed anexou no Apexi Team entra em entrada/ junto com o que veio do Drive
    try:
        from fabrica import team; team.baixar(NN, ENT)
    except Exception as e: print("Team: nao consegui baixar agora:", e)
PUB = f"{P}/render/public/v{NN}"; os.makedirs(PUB + "/img", exist_ok=True); os.makedirs(PUB + "/vid", exist_ok=True)
PASTA = f"v{NN}"
FM = os.environ.get("FINMOOVI_BROLL", "C:/Users/Ed Flávio/Desktop/CLAUDE-CODE/FINMOOVI/VIDEOS-BROLL/")
COD = json.load(open(f"{P}/fabrica/saida/{NN}-codigos.json")) if os.path.exists(f"{P}/fabrica/saida/{NN}-codigos.json") else {}
avisos, usados_ed, planoB = [], [], []

def dur_de(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
def copia(src, nome):
    d = f"{PUB}/{nome}"
    if not os.path.exists(d) or os.path.getsize(d) != os.path.getsize(src): shutil.copy(src, d)
    return f"{PASTA}/{nome}"
def do_ed(nome, ext):
    """o que o Ed salvou no Drive para este pedido (M01-a.jpg ... ou F01.mp4); None se nao chegou"""
    cod = COD.get(nome)
    if not cod or not os.path.isdir(ENT): return None
    achados = sorted(f for f in os.listdir(ENT) if f.upper().startswith(cod) and f.lower().endswith(ext))
    return f"{ENT}/{achados[0]}" if achados else None
def fonte(nome):
    """devolve (tipo, arquivo local): 'img' ou 'vid'"""
    if nome.startswith("banco:FM:"): return "vid", FM + nome[9:]
    if nome.startswith("banco:videos/"): return "vid", f"{P}/banco/{nome[6:]}"
    if nome.startswith("banco:"): return "img", f"{P}/banco/imagens/{nome[6:]}"
    q = C.IMG[nome]
    if q[0].startswith("banco:"): return "img", f"{P}/banco/imagens/{q[0][6:]}"
    if q[0] == "meta":
        g = do_ed(nome, (".gif",))  # o GIF animado do meta.ai (5 s) vira uma cena que se mexe
        if g:
            mp4 = os.path.splitext(g)[0] + "-gif.mp4"
            if not os.path.exists(mp4):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", g, "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p",
                                "-c:v", "libx264", "-crf", "18", "-an", mp4], check=True)
            usados_ed.append(nome); return "vid", mp4
        f = do_ed(nome, (".jpg", ".jpeg", ".png", ".webp"))
        if f: usados_ed.append(nome); return "img", f
        planoB.append(nome); return fonte(q[2][3:])
    if q[0] == "flow":
        f = do_ed(nome, (".mp4", ".mov"))
        if f: usados_ed.append(nome); return "vid", f
        planoB.append(nome); return fonte(q[2][3:])
    f = f"{IMG_CF}/{nome}.jpg"
    if not os.path.exists(f): avisos.append(f"FALTA a imagem {nome}"); return "img", None
    return "img", f
def publica(nome):
    tipo, f = fonte(nome)
    if f is None: return tipo, None
    base = re.sub(r"[^a-z0-9.-]", "-", os.path.basename(f).lower())
    return tipo, copia(f, ("vid/" if tipo == "vid" else "img/") + base)

# ---------------- tempos ----------------
ALIN = alinhar(NN)
for o in ALIN:  # na legenda o app e sempre FinMoovi
    o[2] = re.sub(r"Fin\s*M[óúuo]+vi", "FinMoovi", o[2], flags=re.I)
linhas = sorted(C.L); N_LIN = len(open(f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines())
ini_lin = {k: next((o[0] for o in ALIN if o[3] == k), None) for k in range(N_LIN)}
FIM = round(max(o[1] for o in ALIN) + 0.6, 2)
cenas = []; movs = ["entra", "dir", "sai", "esq"]; nmov = 0
for k in linhas:
    t0 = ini_lin.get(k)
    if t0 is None: avisos.append(f"linha {k}: sem fala"); continue
    for j, (g, tipo, cont) in enumerate(C.L[k]):
        t = t0 if g == "^" else achar(ALIN, k, g)
        if t is None: avisos.append(f"linha {k} cena {j}: nao achei '{g}'"); t = t0 + 2 * j
        s = round(max(t0, t - 0.12), 2); chave = f"{k}-{j}"; mv = movs[nmov % 4]; nmov += 1
        if tipo == "M":
            spec = dict(cont); spec.update(ini=s, chave=chave)
            if spec["k"] == "montagem":
                spec["imgs"] = [x for x in (publica(n)[1] for n in spec["imgs"]) if x]
                if len(spec["imgs"]) < 3: spec = {"k": "frase", "texto": "", "ini": s, "chave": chave}; avisos.append(f"{chave}: montagem rapida sem imagens")
            cenas.append(spec); continue
        nome, ov = (cont if isinstance(cont, tuple) else (cont, []))
        tp, src = publica(nome)
        if src is None: cenas.append({"ini": s, "k": "frase", "texto": "", "chave": chave}); continue
        if tp == "vid": cenas.append({"ini": s, "k": "vid", "src": src, "mov": mv, "de": 0, "chave": chave, "clip": round(dur_de(f"{P}/render/public/{src}"), 2), "ov": ov})
        else: cenas.append({"ini": s, "k": "hib" if ov else "img", "src": src, "mov": mv, "ov": ov, "chave": chave, "sil": tipo == "SIL"})
cenas.sort(key=lambda c: c["ini"])
# prova de mesa: cada motion com o que ele precisa (um campo vazio derruba a geracao do video inteiro)
PRECISA = {"graf": ["series"], "barras": ["itens"], "icones": ["itens"], "linha": ["marcos"], "conta": ["linhas"], "torre": ["itens"],
           "cal": ["marcados"], "montagem": ["imgs"], "cita": ["nome", "achado"], "frase": [], "num": ["valor"], "grade": ["total"]}
erros = []
for c in cenas:
    for campo in PRECISA.get(c["k"], []):
        if not c.get(campo): erros.append(f"{c['chave']} ({c['k']}): falta '{campo}'")
    if c["k"] == "graf" and any(not s_.get("pts") for s_ in c["series"]): erros.append(f"{c['chave']} (graf): serie sem pontos")
    if c["k"] == "graf" and c.get("eixo") is not None and any(len(s_["pts"]) != len(c["eixo"]) for s_ in c["series"]) and c["eixo"]: erros.append(f"{c['chave']} (graf): eixo e pontos de tamanhos diferentes")
if erros: raise SystemExit("PROVA DE MESA FALHOU: " + " | ".join(erros))
# o que vai por cima entra na palavra (gatilho "g"), se tiver
for c in cenas:
    for o in c.get("ov", []) or []:
        if o.get("g"):
            t = achar(ALIN, int(c["chave"].split("-")[0]), o["g"])
            if t is not None: o["ini"] = round(max(0.3, t - c["ini"]), 2)
TELA = 10.0
cenas.append({"ini": FIM, "k": "final", "chave": "final"})
for i in range(len(cenas) - 1):
    d = cenas[i + 1]["ini"] - cenas[i]["ini"]
    if d < 1.2: avisos.append(f"cena curta {cenas[i]['chave']} {d:.2f}s")
    if d > 10: avisos.append(f"cena longa {cenas[i]['chave']} {d:.2f}s")

# ---------------- trilha de filme: um clima por trecho (CLIMA em cenas.py) ----------------
MUS = P + "/render/public/musica/"
FAIXAS = {"calma": ["Wallpaper", "Dreamer", "Life-of-Riley"], "tensao": ["Investigations", "Hitman", "Dark-Times"],
          "triste": ["Heartbreaking", "Sad-Trio"], "curiosa": ["Thinking-Music", "Local-Forecast---Elevator"], "humor": ["Sneaky-Snitch"],
          "montagem": ["Impending-Boom"], "reflexiva": ["Lasting-Hope", "Touching-Moments-Two---Higher"], "virada": ["Inspired"],
          "final": ["Inspired"], "drama": ["Long-Note-Two"]}
uso = {}; partes = []
pontos = sorted((ini_lin[k], cl) for k, cl in C.CLIMA.items() if ini_lin.get(k) is not None)
TOTAL = FIM + TELA
for i, (a, cl) in enumerate(pontos):
    b = pontos[i + 1][0] if i + 1 < len(pontos) else TOTAL
    if cl == "silencio": partes.append((a, b, None)); continue
    lista = FAIXAS[cl]; f = lista[uso.get(cl, 0) % len(lista)]; uso[cl] = uso.get(cl, 0) + 1
    partes.append((a, b, f))
if partes and partes[0][0] > 0: partes[0] = (0, partes[0][1], partes[0][2])
X = 2.0; ent, filt = [], []
for i, (a, b, f) in enumerate(partes):
    d = b - a + (X if i < len(partes) - 1 else 0)
    if f: ent += ["-stream_loop", "-1", "-i", MUS + f + ".mp3"]
    else: ent += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    norm = ",loudnorm=I=-30:TP=-6:LRA=7" if f else ""
    filt.append(f"[{i}:a]atrim=0:{d:.2f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo{norm}[m{i}]")
cad = "[m0]"
for i in range(1, len(partes)):
    xd = 0.4 if (partes[i][2] is None or partes[i - 1][2] is None) else X  # o silencio entra em CORTE (Ed: "cai o volume")
    filt.append(f"{cad}[m{i}]acrossfade=d={xd}:c1=tri:c2=tri[x{i}]"); cad = f"[x{i}]"
filt.append(f"{cad}volume='if(gte(t,{FIM}),1.0+1.6*min(1,(t-{FIM})/1.5),1.0)':eval=frame,afade=t=in:d=2,afade=t=out:st={TOTAL - 2.5:.2f}:d=2.5[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ent, "-filter_complex", ";".join(filt), "-map", "[o]", "-t", f"{TOTAL:.2f}", "-c:a", "libmp3lame", "-q:a", "3", PUB + "/trilha.mp3"], check=True)
musicas = sorted({f for _, _, f in partes if f})

# ---------------- sons de cena (AMB em cenas.py) ----------------
AMB = P + "/render/public/amb"
def gera(nome, expr, dur, extra=""):
    out = f"{AMB}/{nome}.wav"
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={dur}" + (f",{extra}" if extra else ""), "-ac", "1", out], check=True)
gera("bip", "0.45*sin(2*PI*2300*t)*lt(mod(t,0.55),0.11)", 8, "")
efeitos = []
for som, lin, g, dur, vol in getattr(C, "AMB", []):
    t = ini_lin.get(lin) if g == "^" else achar(ALIN, lin, g)
    if t is None: avisos.append(f"som {som} linha {lin}: nao achei '{g}'"); continue
    efeitos.append({"src": f"amb/{som}.wav", "ini": round(t, 2), "dur": dur, "vol": vol, "fi": 0.6, "fo": 1.2})
# montagem rapida: coracao junto
for c in cenas:
    if c["k"] == "montagem":
        prox = next(x["ini"] for x in cenas if x["ini"] > c["ini"])
        efeitos.append({"src": "amb/coracao.wav", "ini": c["ini"], "dur": round(prox - c["ini"], 2), "vol": 0.7, "fi": 0.2, "fo": 0.3})

# ---------------- legendas: texto do roteiro, 2 a 4 palavras, numeros e palavras-chave em amarelo ----------------
FORTES = {"tião", "marcos", "sandra", "finmoovi", "like"} | set(getattr(C, "FORTES", set()))
motion = [(c["ini"], c["k"]) for c in cenas]
def em_motion(t):
    k = None
    for s0, kk in motion:
        if s0 <= t: k = kk
        else: break
    return k not in ("img", "vid", "hib")
leg = []; grupo = []
for i, (s0, e0, w, lin) in enumerate(ALIN):
    grupo.append((s0, e0, w))
    prox = ALIN[i + 1][0] if i + 1 < len(ALIN) else 1e9
    quebra = len(grupo) >= 4 or re.search(r"[.,!?;:]$", w) or prox - e0 > 0.35 or sum(len(x[2]) for x in grupo) > 20 or (i + 1 < len(ALIN) and ALIN[i + 1][3] != lin)
    if quebra:
        forte = lambda x: re.search(r"\d", x) or re.sub(r"[^\wÀ-ú]", "", x).lower() in FORTES
        texto = " ".join("*" + x[2] + "*" if forte(x[2]) else x[2] for x in grupo).replace("* *", " ").replace('"', "")
        leg.append([round(grupo[0][0], 2), round(grupo[-1][1] + 0.15, 2), texto]); grupo = []
leg = [l for l in leg if not em_motion(l[0] + 0.05)]

copia(f"{P}/teste-vozes/NARRACAO-video-{NN}.mp3", "narracao.mp3")
props = {"pasta": PASTA, "fim": FIM, "tela": TELA, "cenas": cenas, "legendas": leg, "efeitos": efeitos}
json.dump(props, open(PUB + "/props.json", "w", encoding="utf-8"), ensure_ascii=False)
relato = {"cenas": len(cenas), "fim": FIM, "musicas": musicas, "do_ed": usados_ed, "plano_b": planoB, "avisos": avisos}
json.dump(relato, open(f"{P}/fabrica/saida/{NN}-montagem.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(cenas), "cenas", dict(Counter(c["k"] for c in cenas)), len(leg), "legendas, fim", FIM)
print("do Ed:", len(usados_ed), "· plano B:", len(planoB), "· musicas:", musicas)
print("\n".join(avisos[:40]) or "sem avisos")
