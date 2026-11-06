# Prepara a capa (thumbnail) de um video: pega a imagem que o Ed pos em banco/_entrada, aumenta a qualidade com o
# Real-ESRGAN (o mesmo programinha gratis do GoApexi, modelo para desenho) e salva no tamanho do YouTube.
# Uso: python capas/preparar-capa.py video-01            (pega a imagem mais nova de banco/_entrada)
#      python capas/preparar-capa.py video-01 arquivo.jpg
# Sai em capas/<video>/: capa.jpg (1280x720, menos de 2 MB, o que sobe no YouTube), capa-hd.jpg (1920x1080) e capa-original.*
# Pedido do Ed (05/11/2026): "assim como no GoApexi que usa um programinha pra dar mais qualidade nas imagens,
# preciso que voce faca isso automaticamente para todas as thumbs a partir de agora".
import os, shutil, subprocess, sys, tempfile
from PIL import Image, ImageFilter
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
R = os.path.expanduser("~/.claude/ferramentas/realesrgan/realesrgan-ncnn-vulkan.exe")
if not os.path.exists(R): R = shutil.which("realesrgan-ncnn-vulkan") or ""  # na nuvem (Linux)
video = sys.argv[1]
ENT = P + "/banco/_entrada"
if len(sys.argv) > 2: src = sys.argv[2]
else:
    fs = [os.path.join(ENT, f) for f in os.listdir(ENT) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    if not fs: raise SystemExit("nenhuma imagem em banco/_entrada")
    src = max(fs, key=os.path.getmtime)
OUT = f"{P}/capas/{video}"; os.makedirs(OUT, exist_ok=True)
ext = os.path.splitext(src)[1].lower()
# guarda a original (e a capa anterior, se houver, vai para "anteriores")
if os.path.exists(f"{OUT}/capa.jpg"):
    os.makedirs(f"{OUT}/anteriores", exist_ok=True); n = len(os.listdir(f"{OUT}/anteriores")) + 1
    shutil.move(f"{OUT}/capa.jpg", f"{OUT}/anteriores/capa-{n}.jpg")
shutil.copy(src, f"{OUT}/capa-original{ext}")
tmp = tempfile.mkdtemp(); ent = os.path.join(tmp, "in.png"); sai = os.path.join(tmp, "out.png")
Image.open(src).convert("RGB").save(ent)
try:
    subprocess.run([R, "-i", ent, "-o", sai, "-n", "realesrgan-x4plus-anime", "-s", "4"], check=True, capture_output=True, timeout=1800)
    big = Image.open(sai).convert("RGB")
except Exception as e:  # sem o programa (nuvem sem placa de video): aumenta com o metodo normal e afia
    print("Real-ESRGAN nao rodou, uso o aumento normal:", str(e)[:120])
    o = Image.open(ent).convert("RGB"); big = o.resize((o.width * 2, o.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
# recorta para 16:9 exato (sem distorcer)
w, h = big.size; alvo = 16 / 9
if abs(w / h - alvo) > 0.01:
    if w / h > alvo: nw = int(h * alvo); big = big.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / alvo); big = big.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
hd = big.resize((1920, 1080), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
hd.save(f"{OUT}/capa-hd.jpg", quality=93)
yt = big.resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=2))
q = 92
while True:
    yt.save(f"{OUT}/capa.jpg", quality=q)
    if os.path.getsize(f"{OUT}/capa.jpg") < 1_900_000 or q < 60: break
    q -= 5
os.remove(src)
print(f"capa pronta: capas/{video}/capa.jpg ({os.path.getsize(f'{OUT}/capa.jpg') // 1024} KB) e capa-hd.jpg; original guardada")
