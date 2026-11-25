# 25/11/2026 (Ed: «eu queria noticia mais quente, mais atual! como poderiamos ter acesso pra modelarmos?»)

# As notícias quentes do dia, para os Shorts «Plantão do Tião: o que muda no seu bolso». Tudo grátis:

#  1. YouTube: os Shorts de economia e política das últimas 48 h que mais cresceram (visualizações por hora) = o que modelar;

#  2. Google Trends Brasil: o que o povo está buscando agora;

#  3. Agência Brasil (economia e política): a fonte pública para conferir o fato (regra do canal: fonte oficial antes de escrever).

# Uso: python pesquisa/quentes.py [horas=48]   ->   pesquisa/QUENTES-AAAA-MM-DD.md

import datetime as dt, html, json, os, re, sys, urllib.parse, urllib.request

P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)

from fabrica.google import api

H = int(sys.argv[1]) if len(sys.argv) > 1 else 48

agora = dt.datetime.now(dt.timezone.utc); desde = (agora - dt.timedelta(hours=H)).strftime("%Y-%m-%dT%H:%M:%SZ")

BUSCAS = ["o que muda no seu bolso", "salário mínimo 2027", "imposto de renda", "governo Lula dinheiro", "INSS aposentado",

          "dólar hoje", "conta de luz", "Bolsa Família", "gasolina preço", "Banco Central juros"]

def baixar(url):

    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")

out = [f"# Notícias quentes · {agora.astimezone(dt.timezone(dt.timedelta(hours=-3))):%d/%m/%Y %H:%M} (Brasília), últimas {H} h", ""]



# 1. YouTube: Shorts que estão explodindo

vistos = {}

for q in BUSCAS:

    r = api("https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode({"part": "id", "type": "video", "q": q, "maxResults": 25,

            "order": "viewCount", "publishedAfter": desde, "regionCode": "BR", "relevanceLanguage": "pt", "videoDuration": "short"}))

    for it in r.get("items", []): vistos.setdefault(it["id"]["videoId"], q)

ids = list(vistos); linhas = []

for i in range(0, len(ids), 50):

    for v in api("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=" + ",".join(ids[i:i + 50])).get("items", []):

        h = max(1, (agora - dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))).total_seconds() / 3600)

        vw = int(v["statistics"].get("viewCount", 0))

        lg = (v["snippet"].get("defaultAudioLanguage") or v["snippet"].get("defaultLanguage") or "pt").lower()

        tit = v["snippet"]["title"]

        if (not lg.startswith("pt") or re.search(r"[؀-ۿऀ-ॿ一-鿿]", tit)
                or re.search(r"\b(the|my|after|precio|hoy|pesos|petrol)\b", tit, re.I)):
            continue  # só o Brasil (fora inglês, espanhol, árabe, hindi)

        linhas.append((vw / h, vw, h, v["snippet"]["title"], v["snippet"]["channelTitle"], v["id"]))

linhas.sort(reverse=True)

out += ["## 1. Shorts que mais cresceram (visualizações por hora)", "", "| por hora | total | horas | título | canal |", "|---|---|---|---|---|"]

out += [f"| {int(a):,} | {b:,} | {int(c)} | [{html.unescape(t)}](https://youtube.com/shorts/{i}) | {ch} |".replace(",", ".") for a, b, c, t, ch, i in linhas[:25]]



# 2. Google Trends Brasil

try:

    x = baixar("https://trends.google.com/trending/rss?geo=BR")

    tt = re.findall(r"<item>\s*<title>([^<]*)</title>.*?<ht:approx_traffic>([^<]*)", x, re.S)

    out += ["", "## 2. O que o Brasil está buscando agora (Google Trends)", ""] + [f"- {html.unescape(a)} ({b} buscas)" for a, b in tt[:20]]

except Exception as e: out += ["", f"(Google Trends fora do ar: {e})"]



# 3. Agência Brasil: a fonte pública para conferir

for ed in ("economia", "politica"):

    try:

        x = baixar(f"https://agenciabrasil.ebc.com.br/rss/{ed}/feed.xml")

        it = re.findall(r"<item>.*?<title>([^<]*)</title>.*?<link>([^<]*)</link>", x, re.S)

        out += ["", f"## 3. Agência Brasil · {ed}", ""] + [f"- [{html.unescape(a).strip()}]({b.strip()})" for a, b in it[:12]]

    except Exception as e: out += ["", f"(Agência Brasil {ed} fora do ar: {e})"]

arq = f"{P}/pesquisa/QUENTES-{agora:%Y-%m-%d}.md"

open(arq, "w", encoding="utf-8").write("\n".join(out) + "\n"); print("\n".join(out)); print("\n->", arq)


# 25/11 (Ed: «Sim» ao buscador diário das 7h): na nuvem (quentes.yml), a lista vai para o Apexi Team, para o Ed ver no celular
if "--team" in sys.argv:
    from fabrica import team
    hoje = agora.astimezone(dt.timezone(dt.timedelta(hours=-3)))
    r = team.mandar({"chave_unica": f"tiao-plantao-quentes-{hoje:%Y-%m-%d}", "tipo": "pesquisa", "projeto": "Tião Poupador",
                     "titulo": f"Plantão do Tião · notícias quentes de {hoje:%d/%m}",
                     "descricao": "Só para ler, não precisa fazer nada. Daqui saem os 3 Shorts do dia (o que muda no seu bolso), "
                                  "sempre com a fonte oficial conferida antes.\n\n" + "\n".join(out),
                     "prazo": f"{hoje:%Y-%m-%d}T23:00:00-03:00", "links": [], "passos": []})
    print({k: r.get(k) for k in ("criada", "url")})
