# 25/11/2026: o carteiro do Tião. Entrega cada Short pronto às 6 redes, cada uma no seu minuto (Ed: «esses q ja estao prontos pode
# comecar hoje!»). Modelo: o carteiro do FinMoovi (FINMOOVI/blog-finmoovi/src/scripts/multipost/entregar.js), com o que lá foi MEDIDO:
#  - YouTube: direto pela API do canal (Ed: «o do youtube nao precisa passar pelo multipost»), agendado (privado + publishAt);
#  - as outras redes: API pública do Multipost (perfil Tião Poupador, chave MULTIPOST_TIAO, crua no Authorization), uma chamada por
#    rede porque a data vale para o pedido inteiro;
#  - Instagram: post_type «post» (o vídeo em pé vira Reel); Facebook: «post»;
#  - TikTok (via Zernio): title até 90, description com a legenda, DIRECT_POST (UPLOAD vira rascunho sem legenda), público,
#    brand_content desligado, video_made_with_ai true (a voz é sintetizada: é a declaração honesta);
#  - Pinterest: o quadro é PERGUNTADO ao servidor a cada vez (o número muda se a conta for reconectada); vídeo 1.º, capa depois;
#  - Bluesky: NÃO leva vídeo (defeito do Multipost, medido no FinMoovi): vai a capa com o texto e o link do Short no YouTube.
# Uso: python fabrica/carteiro.py plantao/fila-AAAA-MM-DD.json [--ensaio]
import datetime as dt, json, os, subprocess, sys, time, urllib.parse
import requests
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/.."); sys.path.insert(0, P)
from fabrica.google import token as yt_token
env = dict(l.strip().split("=", 1) for l in open(P + "/acessos.env", encoding="utf-8") if "=" in l and not l.startswith("#")) \
    if os.path.exists(P + "/acessos.env") else {}
K = os.environ.get("MULTIPOST_TIAO") or env["MULTIPOST_TIAO"]
API = "https://multipost.help4desk.com/api/public/v1"
BR = dt.timezone(dt.timedelta(hours=-3))
ENSAIO = "--ensaio" in sys.argv
FILA = json.load(open(sys.argv[1], encoding="utf-8"))
# minutos depois do YouTube em que cada rede sai (horas desiguais: tudo no mesmo minuto é a assinatura de um robô)
ATRASO = {"instagram": 2, "facebook": 5, "zernio-tiktok": 9, "pinterest": 13, "bluesky": 17}

def mp(metodo, caminho, **kw):
    r = requests.request(metodo, API + caminho, headers={"Authorization": K, **kw.pop("headers", {})}, timeout=600, **kw)
    if not r.ok: raise RuntimeError(f"Multipost {caminho}: {r.status_code} {r.text[:300]}")
    return r.json()

def subir_youtube(s, quando):
    tok = yt_token(); tam = os.path.getsize(s["video"])
    meta = {"snippet": {"title": s["titulo_yt"], "description": s["descricao_yt"], "tags": s.get("tags", []), "categoryId": "27",
                        "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"},
            "status": {"privacyStatus": "private", "publishAt": quando.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True}}
    ini = requests.post("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", json=meta,
                        headers={"Authorization": "Bearer " + tok, "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)}, timeout=120)
    if not ini.ok: raise RuntimeError(f"YouTube: {ini.status_code} {ini.text[:300]}")
    with open(s["video"], "rb") as f:
        r = requests.put(ini.headers["Location"], data=f, headers={"Authorization": "Bearer " + tok, "Content-Type": "video/mp4"}, timeout=1800)
    if not r.ok: raise RuntimeError(f"YouTube envio: {r.status_code} {r.text[:300]}")
    return r.json()["id"]

def capa_de(video):
    """a capa em pé: um quadro do próprio Short (o 1.º segundo já tem a manchete)"""
    c = os.path.splitext(video)[0] + "-capa.jpg"
    if not os.path.exists(c):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.2", "-i", video, "-frames:v", "1", "-q:v", "3", c], check=True)
    return c

def subir_midia(arq, tipo):
    with open(arq, "rb") as f:
        return mp("POST", "/upload", files={"file": (os.path.basename(arq), f, tipo)})

canais = {c["identifier"] if "identifier" in c else c.get("providerIdentifier"): c for c in mp("GET", "/integrations")}
relatorio = []
for s in FILA["shorts"]:
    quando = dt.datetime.fromisoformat(s["quando"]).replace(tzinfo=BR)
    print(f"\n== {s['id']} · {quando:%d/%m %H:%M} (Brasília)")
    if ENSAIO: print("  ensaio: nada enviado"); continue
    linha = {"id": s["id"], "quando": quando.isoformat(), "redes": {}}
    # 1. YouTube
    try:
        vid = s.get("youtube_id") or subir_youtube(s, quando); s["youtube_id"] = vid
        linha["redes"]["youtube"] = f"https://youtube.com/shorts/{vid}"; print("  YouTube:", linha["redes"]["youtube"])
    except Exception as e:
        linha["redes"]["youtube"] = f"FALHOU: {e}"; print("  YouTube FALHOU:", e)
    link_short = linha["redes"]["youtube"] if linha["redes"]["youtube"].startswith("http") else s.get("link", "https://www.youtube.com/@tiaopoupador")
    # 2. as outras redes, pelo Multipost
    try:
        video = subir_midia(s["video"], "video/mp4"); capa = subir_midia(capa_de(s["video"]), "image/jpeg")
    except Exception as e:
        print("  Multipost: o envio do arquivo falhou:", e); linha["redes"]["multipost"] = f"FALHOU: {e}"; relatorio.append(linha); continue
    for rede, atraso in ATRASO.items():
        c = canais.get(rede)
        if not c: linha["redes"][rede] = "sem canal"; continue
        legenda = s["legenda"]
        midias = [video]
        if rede == "instagram": cfg = {"__type": "instagram", "post_type": "post"}
        elif rede == "facebook": cfg = {"__type": "facebook", "post_type": "post"}
        elif rede == "zernio-tiktok":
            cfg = {"__type": rede, "title": s["titulo_curto"][:90], "description": legenda, "content": legenda, "privacy_level": "PUBLIC_TO_EVERYONE",
                   "duet": False, "stitch": False, "comment": True, "autoAddMusic": "no", "brand_content_toggle": False, "brand_organic_toggle": False,
                   "video_made_with_ai": True, "content_posting_method": "DIRECT_POST"}
        elif rede == "pinterest":
            quadros = mp("POST", f"/integration-trigger/{c['id']}", json={"methodName": "boards", "data": {}}).get("output", [])
            q = next((b for b in quadros if s.get("quadro", "").lower()[:12] in b["name"].lower()), quadros[0] if quadros else None)
            if not q: linha["redes"][rede] = "FALHOU: sem quadro"; continue
            cfg = {"__type": "pinterest", "board": q["id"], "title": s["titulo_curto"][:95], "link": s.get("link_pin", link_short)}
            midias = [video, capa]   # vídeo 1.º, capa depois (medido no FinMoovi)
        elif rede == "bluesky":
            cfg = {"__type": "bluesky"}; midias = [capa]; legenda = s["legenda_curta"] + "\n\n▶️ " + link_short   # Bluesky não publica vídeo
        else: continue
        conteudo = "".join(f"<p>{l}</p>" if l else "<p></p>" for l in legenda.split("\n"))
        corpo = {"type": "schedule", "date": (quando + dt.timedelta(minutes=atraso)).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                 "shortLink": False, "tags": [],
                 "posts": [{"integration": {"id": c["id"]}, "value": [{"content": conteudo, "image": [{"id": m["id"], "path": m["path"]} for m in midias]}], "settings": cfg}]}
        try:
            mp("POST", "/posts", json=corpo); linha["redes"][rede] = f"agendado {quando + dt.timedelta(minutes=atraso):%H:%M}"
        except Exception as e:
            linha["redes"][rede] = f"FALHOU: {e}"
        print(f"  {rede}: {linha['redes'][rede]}")
        time.sleep(1)
    relatorio.append(linha)
json.dump(FILA, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # guarda o youtube_id (não sobe duas vezes)
out = os.path.splitext(sys.argv[1])[0] + "-entregue.json"
json.dump(relatorio, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("\nrelatório:", out)
