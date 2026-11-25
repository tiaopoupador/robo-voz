# 25/11/2026: confere se o que o carteiro agendou SAIU mesmo (o agendamento é aceito na hora; o erro só aparece na hora de publicar).
# Lê o relatório do carteiro (plantao/fila-DIA-entregue.json), pergunta ao YouTube o estado de cada Short e ao Multipost o estado de
# cada post do perfil do Tião (QUEUE, PUBLISHED, ERROR). Grátis. Uso: python fabrica/conferir_posts.py 2026-11-25
import collections, datetime as dt, json, os, sys
import requests
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/.."); sys.path.insert(0, P)
from fabrica.google import api
DIA = sys.argv[1]
env = dict(l.strip().split("=", 1) for l in open(P + "/acessos.env", encoding="utf-8") if "=" in l and not l.startswith("#"))
fila = json.load(open(f"{P}/plantao/fila-{DIA}.json", encoding="utf-8"))
agora = dt.datetime.now(dt.timezone.utc)
print(f"== YouTube ({len(fila['shorts'])} Shorts)")
ids = [s["youtube_id"] for s in fila["shorts"] if s.get("youtube_id")]
if ids:
    for v in api("https://www.googleapis.com/youtube/v3/videos?part=status,statistics,snippet&id=" + ",".join(ids)).get("items", []):
        st = v["status"]; pub = st.get("publishAt")
        estado = "NO AR" if st["privacyStatus"] == "public" else (f"agendado {pub}" if pub else st["privacyStatus"])
        print(f"  {estado:32} {v['statistics'].get('viewCount', '0'):>6} views · {v['snippet']['title'][:60]}")
print("\n== Multipost (perfil Tião Poupador)")
d0 = dt.datetime.fromisoformat(DIA).replace(tzinfo=dt.timezone.utc)
r = requests.get("https://multipost.help4desk.com/api/public/v1/posts", headers={"Authorization": env["MULTIPOST_TIAO"]}, timeout=60,
                 params={"startDate": (d0 - dt.timedelta(hours=3)).isoformat(), "endDate": (d0 + dt.timedelta(hours=36)).isoformat()})
posts = r.json(); posts = posts.get("posts", posts) if isinstance(posts, dict) else posts
cont = collections.Counter(); erros = []
for p in posts:
    rede = p.get("integration", {}).get("providerIdentifier"); est = p.get("state")
    quando = dt.datetime.fromisoformat((p.get("publishDate") or p.get("date")).replace("Z", "+00:00"))
    if est == "QUEUE" and quando < agora - dt.timedelta(minutes=20): est = "ATRASADO (devia ter saído)"
    cont[(rede, est)] += 1
    if est not in ("PUBLISHED", "QUEUE"): erros.append(f"  ❌ {rede} {quando.astimezone(dt.timezone(dt.timedelta(hours=-3))):%d/%m %H:%M} BR · {est} · {(p.get('error') or '')[:150]}")
for (rede, est), n in sorted(cont.items()): print(f"  {rede:15} {est:28} {n}")
if erros:
    print("\nproblemas:"); print("\n".join(erros))
    try:
        notas = requests.get("https://multipost.help4desk.com/api/public/v1/notifications", headers={"Authorization": env["MULTIPOST_TIAO"]}, timeout=60).json()
        for n in (notas if isinstance(notas, list) else notas.get("notifications", []))[:8]: print("  aviso:", str(n.get("content") or n)[:200])
    except Exception: pass
else: print("\n✅ nada com erro")
