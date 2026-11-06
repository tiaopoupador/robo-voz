# Peca do robo: gera na Cloudflare (gratis, flux-2-klein-4b) as imagens "cf" de um video, na ordem em que aparecem.
# Uso: python fabrica/imagens.py 02 [nome ...]
# Conta os pontos gastos no dia e para em LIMITE (a cota gratis e 10.000 por dia, zera as 21h de Brasilia),
# para nunca passar do gratis. Rodar de novo depois das 21h continua de onde parou.
import base64, datetime, importlib, json, os, sys, time, urllib.error, urllib.request, uuid
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(0, P)
NN = sys.argv[1]; ARGS = [a for a in sys.argv[2:] if not a.startswith("--")]
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
SAI = f"{P}/fabrica/videos/v{NN}/img"; os.makedirs(SAI, exist_ok=True)
from fabrica.google import chaves
env = chaves()  # acessos.env no PC, segredos do GitHub na nuvem
NUVEM = "--drive" in sys.argv  # na nuvem: as imagens ficam no Drive (Tiao Poupador/robo/video-NN/img)
URL = f"https://api.cloudflare.com/client/v4/accounts/{env['CLOUDFLARE_TIAO_CONTA']}/ai/run/@cf/black-forest-labs/flux-2-klein-4b"
REF = {"T": "tiao-frente-sozinho.jpg", "N": "marcos-neutro.jpg", "R": "sandra-neutra.jpg", "F": "tiao-ficha-oficial.jpg"}
# com o Tiao vai tambem a ficha oficial (ele em varias poses e angulos), pedido do Ed a 06/11, para ele nao sair sempre de frente e parado
LIMITE = 9300  # de 10.000: folga para nao estourar
CONTA = f"{P}/fabrica/saida/cloudflare-cota.json"  # pontos gastos no "dia" da Cloudflare (que vira as 00:00 UTC)

ESTILO = ("Flat 2D cartoon illustration, clean thin black outlines, soft cel shading, warm slightly desaturated colors, "
          "modern explainer animation style, 16:9 widescreen, Brazilian working-class setting. ")
IGUAL = "The character must be IDENTICAL to the reference image, not similar: same face, eyes, hair, mustache, skin tone, body shape and clothes. Pose and framing follow the scene, NOT the reference pose. "
QUEM = {
 "T": IGUAL + "Tiao, the man from the reference image, drawn ONCE, as a single character: about 30 years old, short and slightly chubby, round face, short messy black hair, a small thin black pencil mustache (always present, a thin line, never thick), light brown skin, mustard yellow polo shirt, black wristwatch; when legs are visible: faded denim shorts and black flip-flops. ",
 "N": IGUAL + "Marcos, the man from the reference image, drawn ONCE: tall slim man in his late 30s, gelled dark hair, light skin, white shirt with rolled sleeves, dark jeans, brown belt, big silver watch, clean-shaven (NO mustache). ",
 "F": "The LAST attached image is Tiao's official CHARACTER SHEET: the same man seen from many angles, poses and expressions. "
      "Use it ONLY to know how he looks from the side, from behind, bending, walking and with each expression. Do NOT copy the sheet layout: draw Tiao ONLY ONCE, inside the scene. "
      "Tiao is in a natural, dynamic pose that fits the action (walking, bending, turning, reaching, gesturing, seen in three-quarter or profile view), "
      "NEVER standing straight and stiff facing the camera like a reference photo. His mustache is ALWAYS a THIN pencil line, never thick or bushy. ",
 "R": IGUAL + "Sandra, the woman from the reference image, drawn ONCE: late 30s, long wavy brown hair, sunglasses on her head, gold hoop earrings, red blouse, blue jeans, brown handbag. ",
}
ANATOMIA = (" Correct anatomy for EVERY person, including people in the background: exactly two well-formed, symmetrical eyes of the same size,"
            " a normal nose and mouth, two arms and two hands with five fingers each, no extra or missing limbs, no fused fingers,"
            " no deformed or melted faces, faces never inside or merged with objects (blinds, curtains, windows).")
FIM = ANATOMIA + (" ABSOLUTELY NO WRITING ANYWHERE: every sign, banner, store front, shelf label, price tag, package, paper, receipt, phone and screen"
       " shows only plain colors, simple shapes or wavy scribble lines, never letters or words (they always come out misspelled)."
       " No eyes or faces drawn on walls, doors, objects, speakers or devices. Exactly the number of people the scene asks for, each person appears only once.") + " No text, no letters, no numbers, no readable writing, no logos, no brand names, no watermark, no license plates."

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
    campo("prompt", ESTILO + "".join(QUEM[r] for r in refs) + desc + FIM); campo("width", "1024"); campo("height", "576")
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
        q = C.IMG[n]; refs = list(q[1]) + (["F"] if "T" in q[1] else []); c = custo(refs)
        if gasto()[1] + c > LIMITE: print(f"PAREI perto do limite gratis do dia ({gasto()[1]:.0f}). Continua depois das 21h.", flush=True); break
        r = gerar(n, refs, q[2])
        soma(c)  # a Cloudflare cobra mesmo quando a imagem sai ruim
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
    falta = [n for n in na_ordem() if n not in JA]
    print(f"feitas agora: {feitas} · faltam: {len(falta)}", flush=True)
