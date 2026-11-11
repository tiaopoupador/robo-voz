# Peca do robo: gera na Cloudflare (gratis, flux-2-klein-4b) as imagens "cf" de um video, na ordem em que aparecem.
# Uso: python fabrica/imagens.py 02 [nome ...]
# Conta os pontos gastos no dia e para em LIMITE (a cota gratis e 10.000 por dia, zera as 21h de Brasilia),
# para nunca passar do gratis. Rodar de novo depois das 21h continua de onde parou.
import base64, datetime, importlib, json, os, random, sys, time, urllib.error, urllib.request, uuid
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, P)
NN = sys.argv[1]; ARGS = [a for a in sys.argv[2:] if not a.startswith("--")]
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
SAI = f"{P}/fabrica/videos/v{NN}/img"; os.makedirs(SAI, exist_ok=True)
from fabrica.google import chaves
env = chaves()  # acessos.env no PC, segredos do GitHub na nuvem
NUVEM = "--drive" in sys.argv
REVISAR = "--sem-revisor" not in sys.argv and "--revisar" in sys.argv or (NUVEM and "--sem-revisor" not in sys.argv)
CUSTO_REV, RUINS = [0.0], {}
if REVISAR: from fabrica.revisor_imagens import revisar, contexto  # na nuvem: as imagens ficam no Drive (Tiao Poupador/robo/video-NN/img)
URL = f"https://api.cloudflare.com/client/v4/accounts/{env['CLOUDFLARE_TIAO_CONTA']}/ai/run/@cf/black-forest-labs/flux-2-klein-4b"
REF = {"T": "tiao-sem-caneca.jpg", "N": "marcos-neutro.jpg", "R": "sandra-neutra.jpg", "F": "tiao-ficha-oficial.jpg"}
# 07/11: o Tiao vai so com a referencia SEM caneca (a ficha de varias poses saiu do pedido da Cloudflare: dava 3a mao)
LIMITE = 9300  # de 10.000: folga para nao estourar
CONTA = f"{P}/fabrica/saida/cloudflare-cota.json"  # pontos gastos no "dia" da Cloudflare (que vira as 00:00 UTC)

# 07/11/2026 (Ed: «melhorar o prompt», gratis): o modelo pequeno (4B) obedece o comeco e ignora listas compridas de "nao".
# Por isso: pedido CURTO e positivo, enquadramento + o que cada MAO faz + a expressao, e a referencia do Tiao SEM caneca
# (as duas antigas tinham a caneca em todas as poses: ele punha a caneca e a cestinha, e saia uma 3a mao).
# Teste lado a lado em fabrica/saida/teste-prompt/comparar.jpg.
ESTILO = "Flat 2D cartoon illustration, clean black outlines, soft cel shading, warm colors, modern explainer animation, 16:9, Brazilian working-class setting. "
IGUAL = "Same face, hair, skin and clothes as the reference image, drawn once, in a natural pose that fits the action (three-quarter or profile view when it fits). "
QUEM = {
 "T": "Tiao is the man in the reference image: about 30, short and slightly chubby, round face, short messy black hair, a small neat black mustache (always visible), light brown skin, mustard yellow polo, black watch, denim shorts, black flip-flops. " + IGUAL + "His hands hold only what the scene says (no mug unless the scene asks). ",
 "N": IGUAL + "Marcos, the man from the reference image, drawn ONCE: tall slim man in his late 30s, gelled dark hair, light skin, white shirt with rolled sleeves, dark jeans, brown belt, big silver watch, clean-shaven (NO mustache). ",
 "F": "The LAST attached image is Tiao's official CHARACTER SHEET: the same man seen from many angles, poses and expressions. "
      "Use it ONLY to know how he looks from the side, from behind, bending, walking and with each expression. Do NOT copy the sheet layout: draw Tiao ONLY ONCE, inside the scene. "
      "Tiao is in a natural, dynamic pose that fits the action (walking, bending, turning, reaching, gesturing, seen in three-quarter or profile view), "
      "NEVER standing straight and stiff facing the camera like a reference photo. His mustache is ALWAYS a THIN pencil line, never thick or bushy. ",
 "R": IGUAL + "Sandra, the woman from the reference image, drawn ONCE: late 30s, long wavy brown hair, sunglasses on her head, gold hoop earrings, red blouse, blue jeans, brown handbag. ",
}
# o resto do elenco do bairro (fabrica/elenco.json, Ed 07/11): a referencia de cada um e a ficha dele (varias poses)
for _p in json.load(open(P + "/fabrica/elenco.json", encoding="utf-8"))["personagens"]:
    if _p["letra"] in REF or not os.path.exists(P + "/banco/referencia/" + _p["ref"]): continue
    REF[_p["letra"]] = _p["ref"]
    QUEM[_p["letra"]] = (f"One attached image is {_p['id'].capitalize()}'s CHARACTER SHEET (many angles, poses and expressions): use it only to know the character, "
                         "do NOT copy the sheet layout, draw this person ONCE, in a natural dynamic pose that fits the scene. " + IGUAL + _p["visual"] + " ")
ANATOMIA = " Every person appears once, with a normal face, two eyes, two arms and two hands."
# 11/11 (teste FLUX 3 na kie): "linhas onduladas" vira letra inventada ("NERCE", "Hurt"). Pedir em POSITIVO, embalagem lisa, resolveu.
LISO = "in PLAIN SOLID-COLOR packaging with NO labels at all: every package, bag, bottle and can is one flat color with at most a simple round shape, never any letters, words or numbers"
FIM = ANATOMIA + " All signs, boards, papers and screens are blank colored shapes. Every package is plain solid color with no label, no letters, no numbers, no logos."
GENTE = ("people", "crowd", "queue", "line of", "customers", "cashier", "others", "neighbors", "family", "children", "kids", "couple")
def sozinho(refs, desc):  # 11/11 (Ed: «tratando melhor os prompts pra nao gerar com muitos erros»): gente de fundo e onde nasce o olho vesgo
    d = desc.lower()
    return "" if any(g in d for g in GENTE) or "nobody else" in d or len(refs) > 1 else " Nobody else in the scene: no other people, no faces in the background."

def tiles(w, h): return -(-w // 512) * -(-h // 512)
def custo(refs):
    from PIL import Image
    n = tiles(1024, 576) * 26.05
    for r in refs:
        w, h = Image.open(P + "/banco/referencia/" + REF[r]).size; n += tiles(w, h) * 5.37
    return n
def gasto():
    hoje = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    j = json.load(open(CONTA)) if os.path.exists(CONTA) else {}
    return hoje, (j.get("pontos", 0) if j.get("dia") == hoje else 0)
def soma(n):
    hoje, g = gasto(); json.dump({"dia": hoje, "pontos": round(g + n, 1)}, open(CONTA, "w"))

def gerar(nome, refs, desc):
    corpo = []; b = uuid.uuid4().hex
    def campo(k, v, arq=None):
        cab = f'--{b}\r\nContent-Disposition: form-data; name="{k}"' + (f'; filename="{arq}"\r\nContent-Type: image/jpeg' if arq else "") + "\r\n\r\n"
        corpo.append(cab.encode() + (v if isinstance(v, bytes) else v.encode()) + b"\r\n")
    bigode = " His small black mustache is clearly visible." if "T" in refs else ""  # 07/11: dito de novo no fim, senao o 4B esquece
    desc = desc.replace("whose labels have only wavy lines", LISO)
    campo("prompt", ESTILO + "".join(QUEM[r] for r in refs) + desc + bigode + sozinho(refs, desc) + FIM); campo("width", "1024"); campo("height", "576")
    campo("seed", str(random.randint(1, 10**9)))  # cada tentativa sai diferente (o revisor pode pedir outra)
    for n, r in enumerate(refs): campo(f"input_image_{n}", open(P + "/banco/referencia/" + REF[r], "rb").read(), f"ref{n}.jpg")
    dados = b"".join(corpo) + f"--{b}--\r\n".encode()
    req = urllib.request.Request(URL, data=dados, method="POST", headers={"Authorization": "Bearer " + env["CLOUDFLARE_TIAO"], "Content-Type": "multipart/form-data; boundary=" + b})
    for tent in range(3):
        try:
            j = json.load(urllib.request.urlopen(req, timeout=180)); break
        except urllib.error.HTTPError as e:
            txt = e.read()[:300].decode(errors="ignore")
            if e.code == 429 or "allocation" in txt.lower() or "neuron" in txt.lower(): print("COTA", nome, flush=True); return "cota"
            print("ERRO", nome, e.code, txt[:160], flush=True)
            if "flagged" in txt.lower() and tent < 2: time.sleep(2); continue
            return "erro"
        except Exception as e:
            print("ERRO", nome, e, flush=True); time.sleep(3)
    else: return "erro"
    img = j.get("result", {}).get("image")
    if not img: print("ERRO", nome, str(j)[:200], flush=True); return "erro"
    open(f"{SAI}/{nome}.jpg", "wb").write(base64.b64decode(img)); return "ok"

def na_ordem():
    vistos = []
    for k in sorted(C.L):
        for g, tipo, cont in C.L[k]:
            nome = cont[0] if isinstance(cont, tuple) else cont
            if isinstance(nome, str) and nome in C.IMG: vistos.append(nome)
            if isinstance(cont, dict) and cont.get("k") == "montagem": vistos += cont["imgs"]
    # o plano B de cada pedido do Ed tambem e gerado (o video nunca atrasa)
    for n in list(vistos):
        q = C.IMG[n]
        if q[0] in ("meta", "flow") and q[2].startswith("cf:"): vistos.append(q[2][3:])
    return [n for n in dict.fromkeys(vistos) if C.IMG[n][0] == "cf"]

ROTEIRO = open(f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
def fala_de(nome):
    """o que a narracao diz quando a imagem aparece (Ed, 08/11: a fala dizia «parada» e a imagem mostrava ela andando)"""
    usos = []
    for k in sorted(C.L):
        for g, tipo, cont in C.L[k]:
            n = cont[0] if isinstance(cont, tuple) else cont
            alvo = [n] + ([C.IMG[n][2][3:]] if isinstance(n, str) and n in C.IMG and str(C.IMG[n][2]).startswith("cf:") else [])
            planos = [x for x, q in C.IMG.items() if str(q[2]) == "cf:" + nome]
            if nome in alvo or n in planos:
                t = ROTEIRO[k] if k < len(ROTEIRO) else ""
                i = t.lower().find(g.lower()) if g != "^" else 0
                usos.append(t[max(0, i):][:260])
    return " | ".join(usos)[:500] or None

def no_drive():
    from fabrica import drive
    raiz = drive.pasta("Tiao Poupador"); robo = drive.pasta("robo", raiz); v = drive.pasta(f"video-{NN}", robo); img = drive.pasta("img", v)
    return img, {f["name"][:-4] for f in drive.listar(img)}

if __name__ == "__main__":
    if NUVEM: PASTA_DRIVE, JA = no_drive()
    else: JA = {f[:-4] for f in os.listdir(SAI)}
    alvo = ARGS or [n for n in na_ordem() if n not in JA]
    hoje, g = gasto()
    print(f"{len(alvo)} imagens para gerar · ja gastos hoje {g:.0f} de {LIMITE}", flush=True)
    feitas = 0
    for n in alvo:
        q = C.IMG[n]; refs = list(q[1]); c = custo(refs)  # 07/11: sem a ficha de varias poses (caneca em todas): dava a 3a mao e a pose dura
        if gasto()[1] + c > LIMITE: print(f"PAREI perto do limite gratis do dia ({gasto()[1]:.0f}). Continua depois das 21h.", flush=True); break
        for tent in range(3 if REVISAR else 1):  # 07/11: o revisor (Claude) olha e pede outra se tiver defeito que se nota
            r = gerar(n, refs, q[2])
            soma(c)  # a Cloudflare cobra mesmo quando a imagem sai ruim
            if r != "ok" or not REVISAR: break
            try:
                ok, prob, cu = revisar(f"{SAI}/{n}.jpg", refs, q[2], fala_de(n), contexto(NN, C, n)[1]); CUSTO_REV[0] += cu
            except Exception as e: print("revisor falhou, fica a imagem:", e, flush=True); break
            if ok: break
            print(f"  revisor: {n} tentativa {tent + 1} ruim: {'; '.join(prob)[:220]}", flush=True)
            if tent == 2: RUINS[n] = prob
            elif gasto()[1] + c > LIMITE: RUINS[n] = prob; break
            time.sleep(5)
        if r == "cota": print("PAREI: a Cloudflare disse que a cota acabou.", flush=True); soma(LIMITE); break
        if r == "ok":
            feitas += 1; JA.add(n); print(f"OK {n} ({gasto()[1]:.0f})", flush=True)
            if NUVEM:
                from fabrica import drive
                for t in range(5):  # o Drive as vezes da erro passageiro (502): espera e tenta de novo
                    try: drive.subir(f"{SAI}/{n}.jpg", PASTA_DRIVE); break
                    except Exception as e: print("Drive falhou, tento de novo:", e, flush=True); time.sleep(10 * (t + 1))
                else: print("NAO SUBIU", n, flush=True); JA.discard(n)
        time.sleep(20)  # com calma: uma imagem a cada ~30 s (pedido do Ed, 06/11)
    if REVISAR:
        print(f"revisor: US$ {CUSTO_REV[0]:.3f} · ficaram com defeito: {len(RUINS)}", flush=True)
        if RUINS: json.dump(RUINS, open(f"{P}/fabrica/saida/{NN}-imagens-ruins.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    falta = [n for n in na_ordem() if n not in JA]
    print(f"feitas agora: {feitas} · faltam: {len(falta)}", flush=True)
