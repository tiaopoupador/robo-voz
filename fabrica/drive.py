# Peca do robo: as pastas do Google Drive do canal.
#   Tiao Poupador/referencia   (as fotos dos personagens para o Ed anexar)
#   Tiao Poupador/entrada/video-NN   (onde o Ed salva o que gerou a mao)
# Uso: python fabrica/drive.py preparar NN      -> cria as pastas e sobe as referencias que faltam; diz o link
#      python fabrica/drive.py baixar NN        -> baixa o que o Ed salvou para fabrica/videos/vNN/entrada/
import json, mimetypes, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
from fabrica.google import api, P
D = "https://www.googleapis.com/drive/v3/files"
def achar(nome, pai=None, pasta=True):
    q = f"name = '{nome}' and trashed = false" + (" and mimeType = 'application/vnd.google-apps.folder'" if pasta else "") + (f" and '{pai}' in parents" if pai else " and 'root' in parents")
    r = api(D + "?" + urllib.parse.urlencode({"q": q, "fields": "files(id,name)"}))["files"]
    return r[0]["id"] if r else None
def pasta(nome, pai=None):
    return achar(nome, pai) or api(D, {"name": nome, "mimeType": "application/vnd.google-apps.folder", **({"parents": [pai]} if pai else {})})["id"]
def listar(pai):
    r = api(D + "?" + urllib.parse.urlencode({"q": f"'{pai}' in parents and trashed = false", "fields": "files(id,name,size,mimeType)", "pageSize": 1000}))
    return r["files"]
def subir(arq, pai):
    meta = {"name": os.path.basename(arq), "parents": [pai]}; b = "fronteira-tiao"
    tipo = mimetypes.guess_type(arq)[0] or "application/octet-stream"
    corpo = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n--{b}\r\nContent-Type: {tipo}\r\n\r\n").encode() + open(arq, "rb").read() + f"\r\n--{b}--".encode()
    return api("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", corpo, tipo="multipart/related; boundary=" + b)
def preparar(NN):
    raiz = pasta("Tiao Poupador"); ref = pasta("referencia", raiz); ent = pasta("entrada", raiz); v = pasta(f"video-{NN}", ent)
    ja = {f["name"] for f in listar(ref)}
    for f in sorted(os.listdir(P + "/banco/referencia")):
        if f not in ja and f.lower().endswith((".jpg", ".png")): subir(P + "/banco/referencia/" + f, ref); print("subiu", f)
    link = f"https://drive.google.com/drive/folders/{v}"; print("pasta do video:", link)
    return link, f"https://drive.google.com/drive/folders/{ref}"
def baixar(NN):
    raiz = achar("Tiao Poupador"); ent = achar("entrada", raiz); v = achar(f"video-{NN}", ent)
    sai = f"{P}/fabrica/videos/v{NN}/entrada"; os.makedirs(sai, exist_ok=True); n = 0
    for f in listar(v):
        dst = f"{sai}/{f['name']}"
        if os.path.exists(dst) and os.path.getsize(dst) == int(f.get("size", -1)): continue
        open(dst, "wb").write(api(f"{D}/{f['id']}?alt=media", bruto=True)); n += 1
    print(f"baixados {n} arquivos para {sai}"); return sai
if __name__ == "__main__":
    {"preparar": preparar, "baixar": baixar}[sys.argv[1]](sys.argv[2])
