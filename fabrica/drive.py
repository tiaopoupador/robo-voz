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
def baixar_pasta(pid, sai):
    os.makedirs(sai, exist_ok=True); n = 0
    for f in listar(pid):
        if f["mimeType"].endswith("folder"): continue
        dst = f"{sai}/{f['name']}"
        if os.path.exists(dst) and os.path.getsize(dst) == int(f.get("size", -1)): continue
        open(dst, "wb").write(api(f"{D}/{f['id']}?alt=media", bruto=True)); n += 1
    return n
def baixar_tudo(NN):
    """na nuvem, no dia da montagem: imagens do robo, o que o Ed salvou, a narracao e os tempos das palavras"""
    raiz = achar("Tiao Poupador"); robo = achar("robo", raiz); v = achar(f"video-{NN}", robo)
    print("imagens do robo:", baixar_pasta(achar("img", v), f"{P}/fabrica/videos/v{NN}/img"))
    tmp = f"{P}/fabrica/saida/_drive"; baixar_pasta(v, tmp); os.makedirs(P + "/teste-vozes", exist_ok=True)
    for a, b in ((f"NARRACAO-video-{NN}.mp3", f"{P}/teste-vozes/NARRACAO-video-{NN}.mp3"), (f"{NN}-palavras.json", f"{P}/fabrica/saida/{NN}-palavras.json")):
        if os.path.exists(f"{tmp}/{a}"): os.replace(f"{tmp}/{a}", b); print("ok", a)
        else: print("FALTA", a)
    e = achar(f"video-{NN}", achar("entrada", raiz))
    print("do Ed:", baixar_pasta(e, f"{P}/fabrica/videos/v{NN}/entrada") if e else 0)
def guardar(NN, arq):
    """sobe primeiro e so depois apaga o antigo com o mesmo nome (se o envio cair, o antigo fica)"""
    raiz = pasta("Tiao Poupador"); v = pasta(f"video-{NN}", pasta("robo", raiz))
    antigos = [f for f in listar(v) if f["name"] == os.path.basename(arq)]
    r = subir_grande(arq, v)
    for f in antigos: api(f"{D}/{f['id']}", metodo="DELETE", bruto=True)
    return f"https://drive.google.com/file/d/{r['id']}/view"
def subir_grande(arq, pai, parte=32 * 2**20):
    """envio retomavel em pedacos de 32 MB; se a conexao cair, pergunta onde parou e continua (ate 8 vezes)"""
    import time, urllib.request, urllib.error
    from fabrica.google import token
    tipo = mimetypes.guess_type(arq)[0] or "application/octet-stream"; tam = os.path.getsize(arq)
    ini = urllib.request.Request("https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable", method="POST",
        data=json.dumps({"name": os.path.basename(arq), "parents": [pai]}).encode(),
        headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Type": tipo, "X-Upload-Content-Length": str(tam)})
    url = urllib.request.urlopen(ini).headers["Location"]; pos, falhas = 0, 0
    with open(arq, "rb") as f:
        while True:
            f.seek(pos); dados = f.read(parte); fim = pos + len(dados) - 1
            try:
                r = urllib.request.urlopen(urllib.request.Request(url, data=dados, method="PUT", headers={
                    "Content-Length": str(len(dados)), "Content-Range": f"bytes {pos}-{fim}/{tam}"}), timeout=600)
                return json.loads(r.read())
            except urllib.error.HTTPError as e:
                if e.code != 308: raise
                g = e.headers.get("Range"); pos = int(g.split("-")[1]) + 1 if g else 0; falhas = 0
            except (urllib.error.URLError, OSError, TimeoutError):
                falhas += 1
                if falhas > 8: raise
                time.sleep(5 * falhas)
                try:
                    urllib.request.urlopen(urllib.request.Request(url, data=b"", method="PUT", headers={"Content-Length": "0", "Content-Range": f"bytes */{tam}"}), timeout=60)
                except urllib.error.HTTPError as e:
                    if e.code != 308: raise
                    g = e.headers.get("Range"); pos = int(g.split("-")[1]) + 1 if g else 0
if __name__ == "__main__":
    {"preparar": preparar, "baixar": baixar, "baixar-tudo": baixar_tudo}[sys.argv[1]](sys.argv[2])
