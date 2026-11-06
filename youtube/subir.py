# Sobe um video do canal Tiao Poupador ja AGENDADO, com titulo, descricao, tags e capa.
# Uso: python youtube/subir.py video-01 [--ensaio]
# Le capas/<video>/YOUTUBE.md (titulo, descricao, tags, data) e capas/<video>/capa.jpg. O video vem de videos-prontos/.
# Sem capa, NAO sobe (regra igual a dos longos do FinMoovi). Grava o id em capas/<video>/publicado.json.
import json, os, re, sys, urllib.parse, urllib.request, datetime
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
video = sys.argv[1]; ensaio = "--ensaio" in sys.argv
sys.path.insert(0, P)
from fabrica.google import chaves
env = chaves()  # acessos.env no PC, segredos do GitHub na nuvem
D = f"{P}/capas/{video}"
md = open(f"{D}/YOUTUBE.md", encoding="utf-8").read()
titulo = re.search(r"## Título[^\n]*\n(.+)", md).group(1).strip()
desc = re.search(r"## Descrição\n```\n(.*?)\n```", md, re.S).group(1).strip()
tags = [t.strip() for t in re.search(r"## Tags\n(.+)", md).group(1).split(",")]
m = re.search(r"agendar para \*\*\w+, (\d\d)/(\d\d)/(\d{4}), (\d\d):(\d\d)\*\*", md)
quando = datetime.datetime(int(m[3]), int(m[2]), int(m[1]), int(m[4]), int(m[5]), tzinfo=datetime.timezone(datetime.timedelta(hours=-3)))
arq = re.search(r"\*\*Arquivo do vídeo:\*\* `([^`]+)`", md).group(1)
capa = f"{D}/capa.jpg"
assert len(titulo) <= 100, "titulo grande demais"
if not os.path.exists(capa): raise SystemExit("SEM CAPA: o video nao sobe sem capa. Ponha a imagem em banco/_entrada e rode capas/preparar-capa.py")
if quando < datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30): raise SystemExit("a data de publicacao ja passou ou esta perto demais")
print("titulo:", titulo); print("publica em:", quando.isoformat()); print("video:", arq, os.path.getsize(P + "/" + arq) // 2**20, "MB"); print("tags:", len(tags))
if ensaio: raise SystemExit("ensaio: nada foi enviado")

def token():
    d = urllib.parse.urlencode({"client_id": env["YT_ID"], "client_secret": env["YT_SEGREDO"],
                                "refresh_token": env["YT_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=d)))["access_token"]
tok = token()
meta = {"snippet": {"title": titulo, "description": desc, "tags": tags, "categoryId": "27", "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"},
        "status": {"privacyStatus": "private", "publishAt": quando.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True},
        "paidProductPlacementDetails": {"hasPaidProductPlacement": False}}
tam = os.path.getsize(P + "/" + arq)
ini = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status,paidProductPlacementDetails",
    data=json.dumps(meta).encode(), method="POST", headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json; charset=UTF-8",
    "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)})
local = urllib.request.urlopen(ini).headers["Location"]
# envio em pedacos de 64 MB (retoma se cair)
PED = 64 * 2**20; ok = None; pos = 0
with open(P + "/" + arq, "rb") as f:
    while pos < tam:
        f.seek(pos); bloco = f.read(PED); fim = pos + len(bloco) - 1
        req = urllib.request.Request(local, data=bloco, method="PUT", headers={"Authorization": "Bearer " + tok, "Content-Length": str(len(bloco)), "Content-Range": f"bytes {pos}-{fim}/{tam}"})
        try:
            ok = json.load(urllib.request.urlopen(req, timeout=600)); pos = tam
        except urllib.error.HTTPError as e:
            if e.code != 308: raise
            rng = e.headers.get("Range"); pos = int(rng.split("-")[1]) + 1 if rng else 0
            print(f"  enviado {pos * 100 // tam}%", flush=True)
vid = ok["id"]; print("video enviado:", vid)
with open(capa, "rb") as f:
    urllib.request.urlopen(urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", data=f.read(), method="POST",
                           headers={"Authorization": "Bearer " + tok, "Content-Type": "image/jpeg"}))
print("capa posta")
json.dump({"id": vid, "url": f"https://youtu.be/{vid}", "publica_em": quando.isoformat(), "titulo": titulo}, open(f"{D}/publicado.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"PRONTO: https://youtu.be/{vid} (agendado para {quando.strftime('%d/%m %H:%M')})")
