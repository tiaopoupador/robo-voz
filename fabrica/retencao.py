# Peca do robo: onde o publico sai de cada video, e o que o Tiao estava falando nesse segundo (de graca).
# Ideia tirada do youtube-agent-skill (yt-retention, MIT), 23/11/2026, a pedido do Ed: «destile aquilo que daria pra
# ser usado pra melhorar todo nosso processo». Em vez do CSV baixado a mao do Studio, le a curva direto da API
# (YouTube Analytics, a permissao yt-analytics.readonly ja autorizada) e cruza com as palavras da voz (NN-palavras.json).
# Tres problemas diferentes:
#   VAZAMENTO DO GANCHO: quanto sai nos primeiros 30 s (saudavel: menos de 25%). Sempre se corrige no roteiro da abertura.
#   PENHASCOS: quedas fortes num ponto so (troca de assunto sem aviso, recado longo, explicacao comprida).
#   ESCORREGA: a perda lenta no meio = ritmo. Corrige-se cortando, nao reescrevendo.
# Uso: python fabrica/retencao.py 03        (ou: python fabrica/retencao.py todos)
import json, os, sys, urllib.parse
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import api
YA = "https://youtubeanalytics.googleapis.com/v2/reports?"
MINIMO = 100  # com menos visualizacoes a curva e barulho

def videos():
    """{data de publicacao: (id, titulo)} dos envios do canal"""
    up = api("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true")["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    r = api("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=50&playlistId=" + up)
    return {i["contentDetails"].get("videoPublishedAt", i["snippet"]["publishedAt"])[:10]: (i["contentDetails"]["videoId"], i["snippet"]["title"]) for i in r["items"]}

def relatorio(NN, vids):
    cal = {v["nn"]: v for v in json.load(open(f"{P}/fabrica/agenda.json", encoding="utf-8"))["calendario"]}
    # pela data da agenda; se a data mudou (o 02 saiu dia 15 e nao dia 11), o primeiro envio ate 7 dias depois
    from datetime import date, timedelta
    d0 = date.fromisoformat(cal[NN]["quando"][:10]) if NN in cal else None
    dia = next((str(d0 + timedelta(k)) for k in range(8) if d0 and str(d0 + timedelta(k)) in vids), None)
    if not dia: print(f"{NN}: ainda nao publicado"); return
    vid, titulo = vids[dia]
    base = {"ids": "channel==MINE", "startDate": "2026-01-01", "endDate": "2030-12-31", "filters": "video==" + vid}
    tot = api(YA + urllib.parse.urlencode({**base, "metrics": "views,averageViewDuration,averageViewPercentage"})).get("rows") or [[0, 0, 0]]
    views, media, pct = tot[0]
    print(f"\n{NN} {titulo}\n   {views} visualizacoes, ficam em media {media // 60}:{media % 60:02d} ({pct:.0f}% do video)")
    if views < MINIMO: print(f"   (com menos de {MINIMO} visualizacoes a curva ainda e barulho: ler com cuidado)")
    rows = api(YA + urllib.parse.urlencode({**base, "metrics": "audienceWatchRatio,relativeRetentionPerformance", "dimensions": "elapsedVideoTimeRatio"})).get("rows", [])
    if not rows: print("   o YouTube ainda nao tem a curva (leva 1 ou 2 dias)"); return
    pal = f"{P}/fabrica/saida/{NN}-palavras.json"
    pal = json.load(open(pal, encoding="utf-8")) if os.path.exists(pal) else []
    dur = pal[-1][1] if pal else media * 100 / max(pct, 1)
    def fala(t):  # o que se ouvia perto do segundo t (a voz; a vinheta desloca uns 5 s)
        return " ".join(w for a, b, w in pal if t - 4 <= a <= t + 4) if pal else ""
    def mmss(t): return f"{int(t) // 60}:{int(t) % 60:02d}"
    xs = [r[0] for r in rows]; ys = [r[1] * 100 for r in rows]
    i30 = next((i for i, x in enumerate(xs) if x * dur >= 30), 0)
    gancho = 100 - ys[i30]
    print(f"   VAZAMENTO DO GANCHO: saem {gancho:.0f}% nos primeiros 30 s " + ("(saudavel)" if gancho < 25 else "(ALTO: mexer na abertura)"))
    pen = sorted(((ys[i - 1] - ys[i], xs[i] * dur) for i in range(max(1, i30), len(ys)) if ys[i - 1] - ys[i] > 2.5), reverse=True)[:5]
    for perda, t in sorted(pen, key=lambda p: p[1]):
        print(f"   PENHASCO em {mmss(t)}: saem {perda:.1f}%  «{fala(t)}»")
    if not pen: print("   nenhum penhasco: a perda e toda escorregando")
    meio = [ys[i - 1] - ys[i] for i in range(len(ys) // 5, len(ys) * 4 // 5)]
    print(f"   ESCORREGA no meio: {sum(meio) / max(len(meio), 1):.2f}% por cada 1% do video")
    rel = sum(r[2] for r in rows) / len(rows)
    print(f"   contra videos do mesmo tamanho no YouTube: {rel:.2f} (0,5 = na media; mais alto = segura melhor)")

if __name__ == "__main__":
    vs = videos()
    alvo = sys.argv[1] if len(sys.argv) > 1 else "todos"
    cal = [v["nn"] for v in json.load(open(f"{P}/fabrica/agenda.json", encoding="utf-8"))["calendario"]]
    for nn in (cal if alvo == "todos" else [alvo]):
        if alvo != "todos" or any(c == nn for c in cal): relatorio(nn, vs)
