# 26/11/2026: o ESCRITOR dos Plantões do Tião (Ed escolheu a opção «b»: o robô escreve sozinho os 3 Shorts do dia, uns US$ 5 a 9
# por mês nos créditos da Anthropic do canal, chave CLAUDE_TIAO). Roda na nuvem (plantao-auto.yml) logo depois do buscador das 7h.
#  1. lê a lista do buscador (pesquisa/QUENTES-DIA.md): o que explode no YouTube, o que o Brasil busca e as notícias da Agência Brasil;
#  2. baixa o TEXTO de cada notícia da Agência Brasil (a fonte pública que vale como oficial quando cita o órgão: regra do canal);
#  3. o Claude escolhe 3 temas pelo bolso e escreve cada Short no molde aprovado pelo Ed (fabrica/plantao_exemplo.json);
#  4. o CÓDIGO confere, de graça, antes de aceitar: todo número da tela tem de estar no texto da fonte, sem palavra proibida, fim
#     que emenda no começo, tamanho certo. O Short que falhar volta UMA vez ao Claude com o erro; se falhar de novo, sai do dia;
#  5. escreve plantao-DIA.txt (a fala, 1 frase por linha), plantao/DIA/shorts.json (a tela), plantao/DIA/fontes.md e
#     plantao/fila-DIA.json (12h, 18h30 e 21h de Brasília) para o carteiro.
# Uso: python fabrica/plantao_escritor.py AAAA-MM-DD [--ensaio]   (--ensaio: não chama o Claude, só mostra o que mandaria e quanto custa)
import datetime as dt, glob, html, json, os, re, sys, urllib.request
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/.."); sys.path.insert(0, P)
DIA = sys.argv[1]; ENSAIO = "--ensaio" in sys.argv
MODELO = "claude-sonnet-5-5"   # US$ 2 / US$ 10 por milhão de tokens (o mesmo do posts.py e do idiomas.py)
HORAS = ["12:00", "18:30", "21:00"]  # Brasília (Ed aprovou a 25/11)
env = dict(os.environ)
if os.path.exists(P + "/acessos.env"):
    env.update({k: v for k, v in (l.strip().split("=", 1) for l in open(P + "/acessos.env", encoding="utf-8") if "=" in l and not l.startswith("#")) if k not in env})
# a fala vai na raiz do robo-voz (o gravador lê de lá); no PC, o robo-voz é uma pasta dentro do projeto
RV = P if os.path.exists(P + "/gerar.py") else P + "/robo-voz"

def baixar(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")

def texto_da_noticia(url):
    h = baixar(url)
    ps = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", p))).strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", h, re.S)]
    ps = [p for p in ps if len(p) > 50 and not re.search(r"cookie|Termos de Uso|Todos os direitos|Agência Brasil\s*$", p, re.I)]
    data = re.search(r'datetime="([^"]+)"', h) or re.search(r'"datePublished"\s*:\s*"([^"]+)"', h)
    return (data[1][:16] if data else ""), " ".join(ps)[:2200]

# o dia já escrito (ex.: escrito no PC para conferir) não se escreve de novo: não se paga duas vezes
RECONFERIR = "--reconferir" in sys.argv   # confere de novo as respostas já pagas (plantao/DIA/resposta-*.json), sem chamar o Claude
if os.path.exists(f"{P}/plantao/{DIA}/shorts.json") and "--de-novo" not in sys.argv and not RECONFERIR:
    n = len([l for l in open(f"{RV}/plantao-{DIA}.txt", encoding="utf-8").read().splitlines() if l.strip()])
    print(f"o dia {DIA} já está escrito ({n} falas): uso o que está lá")
    if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write(f"partes={json.dumps(list(range(n)))}\n")
    sys.exit()

# 1. a lista do buscador
arq = f"{P}/pesquisa/QUENTES-{DIA}.md"
quentes = open(arq, encoding="utf-8").read()
noticias = re.findall(r"- \[([^\]]+)\]\((https://agenciabrasil\.ebc\.com\.br/[^)]+)\)", quentes)
fontes = {}
for tit, url in noticias[:16]:
    try:
        quando, corpo = texto_da_noticia(url)
        if len(corpo) > 300: fontes[url] = {"titulo": tit, "quando": quando, "texto": corpo}
    except Exception as e: print("  não abriu:", url, e)
print(f"notícias da Agência Brasil lidas: {len(fontes)}")
# o que já saiu nos últimos dias (para não repetir o tema)
ja = []
for f in sorted(glob.glob(P + "/plantao/20*/shorts.json"))[-4:]:
    try: ja += [s.get("titulo", "") for s in json.load(open(f, encoding="utf-8"))["shorts"]]
    except Exception: pass
EXEMPLO = open(P + "/fabrica/plantao_exemplo.json", encoding="utf-8").read()

SISTEMA = """Você escreve os Shorts da série «Plantão do Tião: o que muda no seu bolso», de um canal brasileiro de finanças do dia a dia.
O Tião é porteiro de um prédio chique do centro e o poupador da rua: fala como um amigo na mesa da cozinha, frases curtas, português do Brasil.

REGRAS DO DONO DO CANAL (todas obrigatórias):
1. Fonte: SÓ os textos da Agência Brasil que vêm na mensagem. Todo número, data, nome e fato tem de estar escrito no texto da fonte que você usar. Nada de memória, nada de suposição. Sem opinião de partido: explica o efeito no bolso, nunca diz quem é bom ou mau.
2. Escolha 3 notícias DIFERENTES que mexem no bolso de gente comum (salário, INSS, imposto, conta de luz, gasolina, preços, juros, dólar, benefícios, emprego). Prefira o que está quente (aparece nos Shorts que explodem ou no Google Trends) e ainda é fresco. Não repita tema já usado nos últimos dias.
3. Cada Short tem de 5 a 7 falas e de 110 a 160 palavras no total (de 45 a 65 segundos): CONTE as palavras antes de responder, o costume é passar do limite. Cada fala tem no máximo 200 letras. A 1.ª fala é o gancho: o fato mais chocante já com a pergunta do bolso.
4. «fala» é o que a voz lê: números POR EXTENSO («cinquenta e seis bilhões de reais», «vinte por cento», «dois mil e vinte e sete»). «tela» é a mesma frase com os números em algarismos («R$ 56 bilhões», «20%», «2027»). Fora os números, fala e tela são iguais.
5. Pergunta leva «?» e espanto leva «!». Proibido: «hein», «Ih», «Eita», «Ué», «Uai», «Hum», travessão (— ou –), «está escrito» sem dizer onde, e sigla rara (diga o nome inteiro; INSS, PIX e FGTS podem).
6. A ÚLTIMA fala, nesta ordem: (a) pergunta de UMA palavra ligada ao assunto («Isso vai pesar no seu bolso? Comenta SIM ou NÃO!»); (b) «E se quiser saber <algo que a fonte permite responder>, comenta QUERO, que eu faço a parte dois.»; (c) «Se inscreve, que todo dia tem Plantão do Tião, e hoje a notícia é que» terminando SEM ponto: a frase emenda na 1.ª fala quando o vídeo volta ao começo (loop). Se a última fala passar de 200 letras, divida (a) numa fala e (b)+(c) na seguinte.
7. A tela: «quadros», cada um preso a uma fala («linha», contando do 0 dentro deste Short) e a uma palavra dela («palavra», contando do 0 nas palavras da FALA). O quadro entra quando a voz diz essa palavra. De 8 a 11 quadros por Short, em ordem de tempo, um a cada 3 a 7 segundos. Tipos:
   - manchete: {"tipo":"manchete","texto":"... *palavra forte* ...","emoji":"🚨"}  (o 1.º quadro é sempre uma manchete)
   - numero: {"tipo":"numero","ate":56,"antes":"até R$ ","depois":" bi","rotulo":"...","cor":"vermelho"|"verde","casas":0}
   - lista: {"tipo":"lista","titulo":"...","itens":[{"t":"...","ok":true,"linha":1,"palavra":5}]}  (até 4 itens; o mouse marca ✓ ou ✗)
   - compara: {"tipo":"compara","titulo":"...","de":"10%","para":"até 20%","rotuloDe":"...","rotuloPara":"...","ruim":true}
   - grafico: {"tipo":"grafico","titulo":"...","modo":"barras"|"linha","barras":[{"rotulo":"hoje","valor":4,"txt":"R$ 4 bi"}],"destaque":1,"nota":"frase curta do balão","cor":"vermelho"|"verde"}  (2 a 5 barras; o mouse clica na barra do destaque)
   - cards: {"tipo":"cards","titulo":"...","cards":[{"emoji":"🏭","t":"Empresas","valor":"+ imposto","ok":false,"linha":4,"palavra":3}]}  (2 a 4 cards; ok true = bom para o bolso, false = ruim, sem ok = neutro)
   - pergunta: {"tipo":"pergunta","texto":"Isso vai pesar no SEU bolso?","opcoes":["SIM","NÃO"],"emoji":"🤔"}  e a do QUERO: {"tipo":"pergunta","texto":"... Comenta QUERO!","opcoes":["QUERO"],"emoji":"🙋"}
   - inscrever: {"tipo":"inscrever"}  (na palavra «inscreve»)
   Todo Short tem pelo menos 1 grafico OU 1 cards, e pelo menos 1 lista, compara ou cards. Textos da tela curtos (até 45 letras). Nunca data na tela. Os números da tela também têm de estar na fonte.
8. Títulos: «titulo_yt» até 95 letras, com o termo que o povo busca no começo, mistério honesto, 1 emoji e « #shorts» no fim. «titulo_curto» até 60 letras sem emoji. «descricao_yt», «legenda», «legenda_curta» (até 250 letras) e «tags» no MESMO molde do exemplo, com a fonte citada («Fonte: Agência Brasil, com dados do <órgão>, <data>.») e o link do app igual ao do exemplo.
9. «fonte»: as URLs usadas e os trechos EXATOS (copiados letra por letra) que provam cada número.

Responda SÓ com um JSON: {"shorts":[ {três Shorts no formato do exemplo} ]}, o mais urgente primeiro (ele sai ao meio-dia)."""

def pedir(msg):
    import anthropic
    cli = anthropic.Anthropic(api_key=env["CLAUDE_TIAO"])
    # 26/11: sem «pensar» (between_tools). Com o pensar ligado, o Sonnet 5.5 gastou os 16 mil tokens só pensando e não escreveu nada (US$ 0,24 perdidos)
    r = cli.messages.create(model=MODELO, max_tokens=16000, system=SISTEMA, messages=[{"role": "user", "content": msg}], thinking={"type": "between_tools"})
    custo = r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6
    print(f"  Claude: {r.usage.input_tokens} tokens de entrada, {r.usage.output_tokens} de saída = US$ {custo:.3f}")
    t = "".join(b.text for b in r.content if b.type == "text")
    if r.stop_reason != "end_turn": raise SystemExit(f"o Claude parou por «{r.stop_reason}» (gasto US$ {custo:.3f})")
    return json.loads(t[t.index("{"):t.rindex("}") + 1]), custo

# ---- a conferência do código (grátis) ----
PROIBIDO = re.compile(r"\b(hein|ih|eita|ué|uai|hum)\b|[—–]", re.I)
def numeros(s): return re.findall(r"\d+(?:[.,]\d+)*", s)
# só o que APARECE na tela (não os números internos: linha, palavra, destaque...); número solto vira escrita brasileira (2.12 -> 2,12)
INTERNO = {"linha", "palavra", "destaque", "casas", "em", "passo", "ok", "tipo", "cor", "modo", "emoji", "ruim"}
def textos_da_tela(x):
    if isinstance(x, dict): return [t for k, v in x.items() if k not in INTERNO for t in textos_da_tela(v)]
    if isinstance(x, list): return [t for v in x for t in textos_da_tela(v)]
    if isinstance(x, bool): return []
    if isinstance(x, (int, float)): return [f"{x:,.2f}".rstrip("0").rstrip(".").replace(",", "X").replace(".", ",").replace("X", ".")]
    return [str(x)]
def conferir(sh):
    erros = []; falas = sh.get("falas", [])
    base = " ".join(fontes.get(u, {}).get("texto", "") + " " + fontes.get(u, {}).get("titulo", "") for u in sh.get("fonte", {}).get("urls", []))
    if not base.strip(): erros.append("a fonte não é nenhuma das URLs da Agência Brasil que mandei")
    pal = sum(len(f["fala"].split()) for f in falas)
    if not 5 <= len(falas) <= 8: erros.append(f"tem {len(falas)} falas (o certo é de 5 a 7)")
    if not 90 <= pal <= 175: erros.append(f"tem {pal} palavras (o certo é de 110 a 160)")
    for i, f in enumerate(falas):
        if len(f["fala"]) > 215: erros.append(f"a fala {i} tem {len(f['fala'])} letras (máximo 200)")
        if PROIBIDO.search(f["fala"] + f["tela"]): erros.append(f"a fala {i} tem palavra proibida ou travessão")
        if re.search(r"\d", f["fala"]): erros.append(f"a fala {i} tem algarismo: na fala o número vai por extenso")
    if falas and re.search(r"[.!?]\s*$", falas[-1]["fala"]): erros.append("a última fala tem de terminar sem ponto (emenda na primeira)")
    if falas and "QUERO" not in " ".join(f["fala"] for f in falas[-2:]): erros.append("falta o «comenta QUERO» no fim")
    tela = " ".join(f["tela"] for f in falas) + " " + " ".join(textos_da_tela(sh.get("quadros", [])))
    for n in set(numeros(tela)):
        v = n.replace(".", "").replace(",", ".")
        if float(v) <= 3 and len(n) == 1: continue   # «parte 2», «1º», «2 a 4 cards»...
        if not re.search(r"(?<![\d.,])" + re.escape(n) + r"(?![\d])", base): erros.append(f"o número {n} não está no texto da fonte")
    qs = sh.get("quadros", []); tipos = [q.get("tipo") for q in qs]
    if not qs or tipos[0] != "manchete": erros.append("o 1.º quadro tem de ser uma manchete")
    if "grafico" not in tipos and "cards" not in tipos: erros.append("falta 1 gráfico ou 1 cards")
    for q in qs:
        if not (0 <= q.get("linha", -1) < len(falas)) or q.get("palavra", 0) >= len(falas[q["linha"]]["fala"].split()): erros.append(f"o quadro {q.get('tipo')} aponta para fala ou palavra que não existe")
    return erros

# 2. o pedido
noticias_txt = "\n\n".join(f"### {f['titulo']}\nURL: {u}\nPublicada: {f['quando']}\n{f['texto']}" for u, f in fontes.items())
calor = quentes.split("## 3.")[0][:5000]
msg = (f"Hoje é {DIA}. O que está quente (Shorts que mais cresceram e buscas do Google):\n{calor}\n\n"
       f"Temas já usados nos últimos dias (não repetir): {ja or 'nenhum'}\n\n"
       f"O EXEMPLO aprovado pelo dono (um Short completo, no formato que você deve devolver):\n{EXEMPLO}\n\n"
       f"AS FONTES (os únicos textos que valem):\n{noticias_txt}")
if ENSAIO:
    import anthropic; n = anthropic.Anthropic(api_key=env["CLAUDE_TIAO"]).messages.count_tokens(model=MODELO, system=SISTEMA, messages=[{"role": "user", "content": msg}]).input_tokens
    print(f"ensaio: {n} tokens de entrada (medido, grátis); com uns 8 mil de resposta, uns US$ {n * 2e-6 + 8000 * 10e-6:.2f}"); sys.exit()
if RECONFERIR:
    resp, gasto = json.load(open(f"{P}/plantao/{DIA}/resposta-1.json", encoding="utf-8")), 0.0
else:
    resp, gasto = pedir(msg)
os.makedirs(f"{P}/plantao/{DIA}", exist_ok=True); json.dump(resp, open(f"{P}/plantao/{DIA}/resposta-1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
bons, ruins = [], []
for sh in resp.get("shorts", []):
    e = conferir(sh); (ruins if e else bons).append((sh, e))
if ruins and RECONFERIR and os.path.exists(f"{P}/plantao/{DIA}/resposta-2.json"):
    for sh in json.load(open(f"{P}/plantao/{DIA}/resposta-2.json", encoding="utf-8")).get("shorts", []):
        e = conferir(sh)
        if e: print("  saiu do dia:", sh.get("id"), e)
        else: bons.append((sh, []))
    ruins = []
if ruins:   # uma volta só, com os erros
    print("  voltando ao Claude:", {s.get("id"): e for s, e in ruins})
    fix, g2 = pedir(msg + "\n\nVocê já escreveu estes Shorts, mas o conferidor achou erros. Devolva SÓ estes, corrigidos, no mesmo formato {\"shorts\":[...]}:\n"
                    + json.dumps([{"short": s, "erros": e} for s, e in ruins], ensure_ascii=False))
    gasto += g2; json.dump(fix, open(f"{P}/plantao/{DIA}/resposta-2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for sh in fix.get("shorts", []):
        e = conferir(sh)
        if e: print("  saiu do dia:", sh.get("id"), e)
        else: bons.append((sh, []))
bons = [s for s, _ in bons][:3]
print(f"Shorts aprovados pelo conferidor: {len(bons)} · gasto no Claude: US$ {gasto:.3f}")
if not RECONFERIR: open(P + "/plantao/gasto-escritor.csv", "a", encoding="utf-8").write(f"{DIA},{gasto:.4f},{len(bons)}\n")
if not bons: sys.exit("nenhum Short passou na conferência: hoje não sai Plantão")

# 3. os arquivos do dia
os.makedirs(f"{P}/plantao/{DIA}", exist_ok=True)
falas, telas, spec, fila, fichas = [], [], [], [], [f"# Plantão do Tião · {DIA} · fontes (lidas pelo robô na Agência Brasil)", ""]
for k, sh in enumerate(bons):
    base = len(falas); sid = f"{k + 1:02d}-" + re.sub(r"[^a-z0-9]+", "-", sh["id"].split("-", 1)[-1].lower()).strip("-")[:30]
    falas += [f["fala"] for f in sh["falas"]]; telas += [f["tela"] for f in sh["falas"]]
    spec.append({"id": sid, "titulo": sh["titulo_yt"], "linhas": list(range(base, len(falas))), "quadros": sh["quadros"], "loop": True})
    fila.append({"id": f"plantao-{sid}", "quando": f"{DIA}T{HORAS[k]}", "video": f"render/out/PLANTAO-{DIA}-{sid}.mp4", "quadro": "Plantão do Tião",
                 **{c: sh[c] for c in ("titulo_yt", "titulo_curto", "descricao_yt", "legenda", "legenda_curta", "tags")}})
    fichas += [f"## {sid}"] + [f"- {u}" for u in sh["fonte"]["urls"]] + [f"  - «{t}»" for t in sh["fonte"].get("trechos", [])] + [""]
open(f"{RV}/plantao-{DIA}.txt", "w", encoding="utf-8").write("\n".join(falas) + "\n")
json.dump({"data": DIA, "texto": f"plantao-{DIA}.txt", "tela": telas, "fontes": f"plantao/{DIA}/fontes.md", "shorts": spec},
          open(f"{P}/plantao/{DIA}/shorts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(f"{P}/plantao/{DIA}/fontes.md", "w", encoding="utf-8").write("\n".join(fichas))
json.dump({"dia": DIA, "shorts": fila}, open(f"{P}/plantao/fila-{DIA}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"falas: {len(falas)} -> plantao-{DIA}.txt")
if os.environ.get("GITHUB_OUTPUT"):
    open(os.environ["GITHUB_OUTPUT"], "a").write(f"partes={json.dumps(list(range(len(falas))))}\n")
