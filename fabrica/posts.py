# Peca do robo: os 7 posts da semana da aba "Posts" do YouTube (modelo: FINMOOVI/blog-finmoovi/src/scripts/youtube/posts-semana.js).
# A API do YouTube NAO cria posts: o robo escreve, faz as imagens e manda para o Apexi Team; o Ed cola e AGENDA no Studio.
# Pedido do Ed (06/11/2026): «pode ser assim». Um post por dia, as 12h de Brasilia. Desde 20/11 os dias saem das DATAS da agenda
#   (plano()): video antes das 12h = «saiu hoje» + link + capa; depois das 12h = «hoje as HHh»; na vespera a tarde = «ontem» + link;
#   dia sem video = enquete (com imagem), quiz, comunidade ou dica. Dia ja passado nao entra; semana ja mandada nao se repete (--forcar).
# Travas (por codigo): sem "gratis", so numeros que estao no roteiro, sem link escrito pela IA, sem mandar fazer conta,
# sem travessao, cena da imagem sem letras. O que reprova volta para o Claude corrigir so o erro.
# Uso: python fabrica/posts.py [--ensaio] [--semana=AAAA-MM-DD (a segunda)]
import base64, datetime, json, os, re, sys, time, urllib.error, urllib.request, uuid
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import api, chaves
from fabrica import drive
from fabrica.drive import D
ENSAIO = "--ensaio" in sys.argv
MODELO = "claude-sonnet-5-5"
BR = datetime.timezone(datetime.timedelta(hours=-3))
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
LIMITE_TEXTO, LIMITE_OPCAO = 500, 65
LETRAS = "ABCD"
PROIBIDO_TAREFA = re.compile(r"\b(calcul\w*|fa[çc]a a conta|faz a conta|fa[çc]a as contas|somar|anot\w+|pegue o extrato|abra o extrato)", re.I)
GRATIS = re.compile(r"gr[aá]t[ií]s|de gra[çc]a|gratuit", re.I)
CENA_COM_LETRAS = re.compile(r"(escrit|texto|letreiro|placa|palavra|frase|legenda|t[ií]tulo|n[uú]mero|etiqueta|cartaz|r\$|\d|logo|marca)", re.I)
log = lambda *m: print(*m, flush=True)

# ---------------- a semana ----------------
def segunda():
    a = next((x.split("=")[1] for x in sys.argv if x.startswith("--semana=")), None)
    if a: return datetime.date.fromisoformat(a)
    hoje = datetime.datetime.now(BR).date(); return hoje - datetime.timedelta(days=hoje.weekday())
def calendario():
    from fabrica.agenda import ler; return ler().get("calendario", [])
def video(nn):
    """o que o robo sabe de um video: titulo, roteiro (para os numeros), id do YouTube e capa (se ja publicado)"""
    cal = next((c for c in calendario() if c["nn"] == nn), {"nn": nn, "titulo": "", "quando": ""})
    v = {"nn": nn, "titulo": cal["titulo"], "quando": cal["quando"], "roteiro": "", "id": None, "capa": None, "pergunta": ""}
    try:
        import importlib; C = importlib.import_module(f"fabrica.videos.v{nn}.cenas")
        v["titulo"] = C.TITULO; v["pergunta"] = getattr(C, "PERGUNTA", "")
    except Exception: pass
    r = next((f for f in sorted(os.listdir(f"{P}/roteiros")) if f.startswith(f"{nn}-") and f.endswith(".md") and "pedidos" not in f and "fontes" not in f), None)
    if r: v["roteiro"] = open(f"{P}/roteiros/{r}", encoding="utf-8").read()
    try:
        pasta = drive.achar(f"video-{nn}", drive.achar("robo", drive.achar("Tiao Poupador")))
        for f in drive.listar(pasta) if pasta else []:
            if f["name"] == "publicado.json": v["id"] = json.loads(api(f"{D}/{f['id']}?alt=media", bruto=True)).get("id")
            if f["name"] == "capa.jpg": v["capa"] = f["id"]
    except Exception as e: log("Drive:", e)
    return v

# ---------------- o pedido ao Claude ----------------
HORA_POST = 12  # todo post vai as 12h de Brasilia
def plano(seg, cal, comunidade, desde=None):
    """um post por dia, as 12h, tirado das DATAS da agenda (Ed, 20/11: «reveja as datas corretas»):
    video que sai no dia antes das 12h -> «saiu hoje» com o link; video que sai depois das 12h -> «hoje as HHh»;
    video que saiu na vespera depois das 12h -> «ontem» com o link; dia sem video -> enquete, quiz, comunidade ou dica.
    Devolve (pl, vids): pl = [(dia, tipo, pedido, extra)], extra = {data, video (nn ou ""), cena (leva imagem?)}"""
    quando = lambda c: datetime.datetime.fromisoformat(c["quando"])
    por_dia = {}
    for c in cal:
        if c.get("titulo"): por_dia.setdefault(quando(c).date(), []).append(c)
    vids, pl, livres = {}, [], ["enquete", "quiz", "comunidade", "dica"]
    def v(c):
        if c["nn"] not in vids: vids[c["nn"]] = video(c["nn"])
        return vids[c["nn"]]
    for d in range(-1, 8):  # a vespera e o domingo seguinte entram no contexto
        for c in por_dia.get(seg + datetime.timedelta(days=d), []): v(c)
    for i in range(7):
        data = seg + datetime.timedelta(days=i); dia = DIAS[i]
        if desde and data < desde: continue
        hoje = por_dia.get(data, []); ontem = por_dia.get(data - datetime.timedelta(days=1), [])
        cedo = [c for c in hoje if quando(c).hour < HORA_POST]; tarde = [c for c in hoje if quando(c).hour >= HORA_POST]
        ontem_tarde = [c for c in ontem if quando(c).hour >= HORA_POST]
        if cedo:
            x = v(cedo[0]); pl.append((dia, "texto", f"O VÍDEO DE HOJE: saiu hoje, {dia}, às {quando(cedo[0]).hour}h, o vídeo novo: «{x['titulo']}». Conte em 2 ou 3 frases, na voz do Tião, o problema que o vídeo mostra, como quem já viu isso de perto, e termine convidando a assistir. NÃO escreva link.", {"data": data, "video": x["nn"], "cena": False}))
        elif tarde:
            x = v(tarde[0]); h = quando(tarde[0]).hour
            pl.append((dia, "texto", f"O AVISO DE HOJE: hoje, {dia}, às {h}h, estreia o vídeo novo: «{x['titulo']}». Desperte curiosidade pelo problema, sem entregar o final.", {"data": data, "video": "", "cena": True}))
        elif ontem_tarde:
            x = v(ontem_tarde[0]); pl.append((dia, "texto", f"O VÍDEO DE ONTEM: «{x['titulo']}». 2 ou 3 frases na voz do Tião sobre o problema, convidando a assistir. NÃO escreva link.", {"data": data, "video": x["nn"], "cena": False}))
        else:
            k = livres.pop(0) if livres else "dica"
            if k == "comunidade" and not comunidade: k = "dica"
            perto = [c for d in (-1, -2, -3, 1, 2) for c in por_dia.get(data + datetime.timedelta(days=d), [])]
            tema = f"«{v(perto[0])['titulo']}»" if perto else "dos vídeos da semana"
            if k == "enquete": pl.append((dia, "enquete", f"ENQUETE sobre o tema do vídeo {tema}: uma situação do dia a dia em que a pessoa se reconhece. 3 ou 4 opções curtas, todas plausíveis, nenhuma 'certa'.", {"data": data, "video": "", "cena": False}))
            elif k == "quiz": pl.append((dia, "quiz", "QUIZ: uma pergunta com UMA resposta certa, tirada de um fato dos vídeos da semana (só fatos que estão nos roteiros). 3 ou 4 opções curtas; diga qual é a certa em 'correta' (0 a 3) e escreva em 'explicacao' 1 frase curta que o YouTube mostra depois da resposta.", {"data": data, "video": "", "cena": False}))
            elif k == "comunidade": pl.append((dia, "texto", f"A COMUNIDADE: um de vocês contou isto nos comentários (NÃO diga o nome da pessoa): «{comunidade}». Comente como o Tião, com carinho e humor, e pergunte quem mais já passou por isso.", {"data": data, "video": "", "cena": True}))
            else: pl.append((dia, "texto", f"A DICA DO TIÃO: uma dica curta e concreta tirada do vídeo {tema}, que a pessoa pode usar hoje, contada como algo que o Tião faz na vida dele. Sem conta, sem lista longa.", {"data": data, "video": "", "cena": True}))
    return pl, vids
def pedido(pl, vids, recados=()):
    ctx = "\n\n".join(f"═══ ROTEIRO DO VÍDEO «{v['titulo']}» ═══\n{v['roteiro'][:14000]}" for v in vids if v["roteiro"])
    if recados: ctx += "\n\n═══ O QUE O DONO DO CANAL ESCREVEU NAS TAREFAS ANTERIORES (siga isto, vale mais que o resto) ═══\n" + "\n".join(f"- {r}" for r in recados)
    return f"""Você escreve os posts da aba "Posts" do canal de YouTube Tião Poupador. Quem fala é o próprio Tião, na primeira pessoa: um brasileiro simples, uns 30 anos, porteiro de um prédio chique do centro, que aprendeu a cuidar do dinheiro no dia a dia (sem dívida, sem luxo). Público: famílias brasileiras de classe média e baixa.
Linguagem: português do Brasil, simples, conversa de vizinho, frases curtas, no máximo 1 ou 2 emojis por post, sem jargão.
FORMATO DO TEXTO (obrigatório): parágrafos curtos de 1 ou 2 frases, separados por UMA linha vazia. O título de um vídeo fica SOZINHO no seu parágrafo, entre «». Nunca um bloco corrido.

{ctx}

═══ OS {len(pl)} POSTS ═══
""" + "\n".join(f"{i + 1}. {d.upper()} ({t}): {p}" for i, (d, t, p, _) in enumerate(pl)) + f"""

═══ PROIBIDO (reprova) ═══
- Pedir para a pessoa fazer conta, somar, calcular, anotar ou ir buscar o extrato. Pergunte pelo que ela JÁ VIVEU.
- Dizer que o FinMoovi é grátis, de graça ou gratuito (ele tem 7 dias de teste). Nem precisa falar do app.
- Qualquer número que não esteja nos roteiros acima (as horas 10h, 17h e 18h podem).
- Escrever links ou endereços (o robô coloca depois).
- Travessão (o traço comprido). Use vírgula ou ponto.
- Mais de {LIMITE_TEXTO} caracteres por texto; opção de enquete ou quiz com mais de {LIMITE_OPCAO} caracteres.

═══ A IMAGEM ═══
Nos posts da lista COM IMAGEM (no fim), escreva também "cena": 1 ou 2 frases descrevendo UMA imagem quadrada com o Tião (o que ele faz, onde, com que objeto do dia a dia, a emoção), em inglês. A cena NÃO pode pedir palavra, número, valor, placa, etiqueta, cartaz, logotipo nem tela com texto. Nos outros posts, "cena" fica vazia (os do vídeo usam a capa; o quiz é só de texto).
COM IMAGEM: """ + ", ".join(d for d, _, _, x in pl if x["cena"]) + "."
ESQ = {"type": "object", "properties": {"posts": {"type": "array", "items": {"type": "object", "properties": {
    "dia": {"type": "string"}, "texto": {"type": "string"}, "opcoes": {"type": "array", "items": {"type": "string"}},
    "correta": {"type": "integer"}, "explicacao": {"type": "string"}, "cena": {"type": "string"}},
    "required": ["dia", "texto", "opcoes", "correta", "explicacao", "cena"], "additionalProperties": False}}},
    "required": ["posts"], "additionalProperties": False}
def numeros(vids):
    s = set(re.findall(r"\d+(?:[.,]\d+)?", " ".join(v["roteiro"] + " " + v["titulo"] for v in vids))); s |= {"7", "10", "12", "17", "18", "10h", "12h", "17h", "18h"}; return s
def validar(posts, pl, ok_num):
    erros = []
    if len(posts) != len(pl): return [f"são {len(pl)} posts, vieram {len(posts)}"]
    for i, (p, (dia, tipo, _, x)) in enumerate(zip(posts, pl)):
        r = f"post {i + 1} ({dia})"; t = p["texto"].strip(); tudo = " ".join([t, *p["opcoes"], p["explicacao"]])
        if not t: erros.append(f"{r}: texto vazio"); continue
        if len(t) > LIMITE_TEXTO: erros.append(f"{r}: {len(t)} caracteres (máximo {LIMITE_TEXTO})")
        if re.search(r"https?://|www\.|\.com\b|youtu\.?be", tudo, re.I): erros.append(f"{r}: tem link, não escreva nenhum")
        if m := PROIBIDO_TAREFA.search(tudo): erros.append(f"{r}: «{m[0]}» manda fazer tarefa; pergunte pelo que a pessoa já viveu")
        if GRATIS.search(tudo): erros.append(f"{r}: o FinMoovi não é grátis; não fale de preço")
        if re.search(r"[—–]", tudo): erros.append(f"{r}: tem travessão; use vírgula ou ponto")
        for n in re.findall(r"\d+(?:[.,]\d+)?", tudo):
            if n not in ok_num: erros.append(f"{r}: o número «{n}» não está nos roteiros")
        if tipo in ("enquete", "quiz"):
            if not 2 <= len(p["opcoes"]) <= 4: erros.append(f"{r}: precisa de 2 a 4 opções")
            for o in p["opcoes"]:
                if len(o) > LIMITE_OPCAO: erros.append(f"{r}: opção com {len(o)} caracteres: «{o}»")
        if tipo == "quiz" and not (0 <= p["correta"] < len(p["opcoes"])): erros.append(f"{r}: 'correta' tem de apontar uma das opções")
        if x["cena"]:
            if len(p["cena"]) < 30: erros.append(f"{r}: falta a 'cena' da imagem")
            elif m := CENA_COM_LETRAS.search(p["cena"]): erros.append(f"{r}: a cena pede «{m[0]}»; a imagem não pode ter letras nem números")
    return erros
def escrever(pl, vids, recados=()):
    import anthropic
    cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"]); base = pedido(pl, vids, recados); ok = numeros(vids); erros, versao, custo = [], None, 0.0
    for tent in range(1, 5):
        msg = base + ("" if not erros else f"\n\n⚠️ A versão abaixo foi REPROVADA:\n{json.dumps(versao, ensure_ascii=False)}\n\nCorrija SÓ isto e deixe o resto igual:\n" + "\n".join(f"- {e}" for e in erros))
        r = cli.messages.create(model=MODELO, max_tokens=6000, messages=[{"role": "user", "content": msg}], output_config={"format": {"type": "json_schema", "schema": ESQ}})
        custo += r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6
        versao = json.loads(next(b.text for b in r.content if b.type == "text"))["posts"]
        erros = validar(versao, pl, ok)
        if not erros: log(f"✍️ posts aprovados na tentativa {tent} · custo US$ {custo:.3f}"); return versao, custo
        log(f"  ⚠ tentativa {tent} reprovada: " + " | ".join(erros))
    raise SystemExit("os posts não passaram nas travas: " + " | ".join(erros))

# ---------------- a imagem (Cloudflare gratis, quadrada, com o Tiao) ----------------
def prompt_imagem(cena):
    return ("Flat 2D cartoon illustration, clean thin black outlines, soft cel shading, warm colors, square 1:1 social media post image, simple background. "
            "The character must be IDENTICAL to the reference images: Tiao, about 30, short and slightly chubby, round face, short messy black hair, a THIN black pencil mustache, "
            "light brown skin, mustard yellow polo shirt, faded denim shorts, black flip-flops, black wristwatch. The second reference is his character sheet: draw him ONCE, in a natural pose. "
            f"Scene: {cena} Correct anatomy, five fingers. ABSOLUTELY NO text, letters, numbers, signs, logos or screens with writing anywhere.")
def imagem(cena, arq):
    e = chaves(); b = uuid.uuid4().hex; corpo = []
    def campo(k, v, nome=None):
        cab = f'--{b}\r\nContent-Disposition: form-data; name="{k}"' + (f'; filename="{nome}"\r\nContent-Type: image/jpeg' if nome else "") + "\r\n\r\n"
        corpo.append(cab.encode() + (v if isinstance(v, bytes) else v.encode()) + b"\r\n")
    campo("prompt", prompt_imagem(cena)); campo("width", "1024"); campo("height", "1024")
    for n, r in enumerate(("tiao-sem-caneca.jpg",)): campo(f"input_image_{n}", open(f"{P}/banco/referencia/{r}", "rb").read(), f"r{n}.jpg")
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{e['CLOUDFLARE_TIAO_CONTA']}/ai/run/@cf/black-forest-labs/flux-2-klein-4b",
                                 data=b"".join(corpo) + f"--{b}--\r\n".encode(), method="POST", headers={"Authorization": "Bearer " + e["CLOUDFLARE_TIAO"], "Content-Type": "multipart/form-data; boundary=" + b})
    try: open(arq, "wb").write(base64.b64decode(json.load(urllib.request.urlopen(req, timeout=180))["result"]["image"])); return True
    except Exception as x: log("imagem não saiu (o Ed gera pela cena):", getattr(x, "code", x)); return False

# ---------------- montar os passos (manual da porta, secao 3b; padrao novo do Ed, 17 e 18/11) ----------------
# Um post = um passo (codigo post-AAAA-MM-DD). O texto do passo diz o tipo, o dia e a hora; cada coisa a colar vai em
# "copias", com o seu botao. Links e ficheiro ficam no passo que leva imagem. Modelo: blog-finmoovi 3885be3d.
NOME_DIA = {"segunda": "Segunda", "terça": "Terça", "quarta": "Quarta", "quinta": "Quinta", "sexta": "Sexta", "sábado": "Sábado", "domingo": "Domingo"}
SIGLA = {"segunda": "seg", "terça": "ter", "quarta": "qua", "quinta": "qui", "sexta": "sex", "sábado": "sab", "domingo": "dom"}
STUDIO = {"rotulo": "🎬 Abrir o YouTube Studio", "url": "https://studio.youtube.com/"}
META_AI = {"rotulo": "🎨 Abrir o Meta AI", "url": "https://www.meta.ai/"}
def frase(o):  # a explicacao do quiz com ponto final
    o = o.strip(); return o if o[-1:] in ".?!" else o + "."
def tem_img(it): return bool(it.get("url_img") or it.get("cena"))
def formato(it):
    if it["tipo"] == "enquete": return "📊 ENQUETE COM IMAGEM" if tem_img(it) else "📊 ENQUETE SÓ DE TEXTO"
    if it["tipo"] == "quiz": return "🧠 QUIZ (só de texto)"
    return "📝 POST DE TEXTO"
def arejar(t):
    """o texto em blocos curtos, com linha vazia entre eles, e o titulo «...» sozinho no seu paragrafo (mesmo que o Claude esqueca)"""
    t = re.sub(r"[ \t]*(«[^»]{8,}»[.!?]?)[ \t]*", r"\n\n\1\n\n", t.strip())
    blocos = []
    for b in re.split(r"\n\s*\n", t):
        b = " ".join(b.split())
        if not b: continue
        if b.startswith("«") or b.startswith("▶") or len(b) < 140: blocos.append(b); continue
        frases = re.findall(r"[^.!?]+[.!?]+[^\w«]*|[^.!?]+$", b); g = []
        for f in frases:
            g.append(f.strip())
            if len(g) == 2: blocos.append(" ".join(g)); g = []
        if g: blocos.append(" ".join(g))
    return "\n\n".join(blocos)
def copias(it):
    """cada coisa a colar, pela ordem em que se cola no Studio"""
    if it["tipo"] == "texto": c = [{"rotulo": "Texto do post", "texto": arejar(it["texto"])}]
    else: c = [{"rotulo": "Pergunta", "texto": it["texto"]}] + [{"rotulo": f"Opção {LETRAS[k]}", "texto": o.strip()} for k, o in enumerate(it["opcoes"])]
    if it["tipo"] == "quiz": c.append({"rotulo": "Explicação (depois da resposta)", "texto": frase(it["explicacao"])})
    if it.get("img_caminho"): c.append({"rotulo": "🖼️ Imagem do post (no seu PC)", "texto": it["img_caminho"]})
    if it.get("cena") and not it.get("capa"):
        c.append({"rotulo": "Prompt da imagem (Meta AI, só se não gostar da do robô)", "texto": prompt_imagem(it["cena"])})
        c.append({"rotulo": "📎 Anexar junto ao Prompt", "texto": FICHA})
    return c
PC = "G:\\Meu Drive\\Tiao Poupador"  # o Drive do canal no PC do Ed (o link http abre na conta errada: Ed, 21/11)
FICHA = PC + "\\referencia\\tiao-ficha-oficial.jpg"
def refs_tiao():  # as fotos do Tiao no Drive, para anexar quando o Ed gera a imagem a mao
    try:
        ref = drive.achar("referencia", drive.achar("Tiao Poupador"))
        return [{"rotulo": "Anexar junto ao Prompt - " + f["name"], "url": f"https://drive.google.com/file/d/{f['id']}/view"}
                for f in drive.listar(ref) if f["name"] == "tiao-ficha-oficial.jpg"]  # so a ficha oficial do Tiao (Ed 19/11)
    except Exception: return []
DESCRICAO = "\n".join([
    "Post de texto: copie o texto (já vem com os parágrafos); a imagem está no seu PC, no caminho do passo. No YouTube Studio: Criar > Criar post, cole o texto, Imagem, seta ao lado de Postar > Agendar.",
    "Enquete (só de texto): Criar > Criar post > Enquete com texto. A pergunta vai no 1º campo e cada opção no seu.",
    "Quiz (só de texto): Criar > Criar post > Quiz. Pergunta, opções, marque a certa (vem no título do passo) e cole a explicação.",
    "O YouTube não deixa robô publicar posts, por isso vêm para agendar à mão."])
def montar(seg, itens):
    """itens: dia, tipo, texto (ja com o link), opcoes, correta, explicacao, cena, url_img, capa, video, falta_link -> (passos do Team, texto do e-mail)"""
    passos, md, refs = [], [f"# Tião Poupador · posts de {itens[0]['data']:%d/%m} a {itens[-1]['data']:%d/%m}", "",
                            "Cole cada um no YouTube Studio (Criar > Criar post) e **agende para o dia e a hora indicados**.", ""], None
    for i, it in enumerate(itens):
        data = it["data"]; dia = it["dia"]; fmt = formato(it)
        texto = f"{fmt} · {NOME_DIA[dia]} {data:%d/%m} · agendar para as 12h"
        if it["tipo"] == "quiz": texto += f" · resposta certa: Opção {LETRAS[it['correta']]}"
        if it.get("falta_link"): texto += f" · ⚠️ falta o link do vídeo {it['nn']}: junte-o no fim do texto"
        p = {"codigo": f"post-{data.isoformat()}", "texto": texto, "copias": copias(it), "links": [STUDIO]}
        # o video ja vai no fim do texto, e a imagem e um CAMINHO no PC (o link do Drive abre noutra conta: Ed, 21/11)
        if it.get("cena") and not it.get("capa"):
            p["links"].append(META_AI)
            if not it.get("img_caminho"): p["ficheiro"] = f"post-{data.isoformat()}-{SIGLA[dia]}.jpg"; p["formato"] = "1:1"
        passos.append(p)
        md += [f"### {texto}", ""]
        for c in p["copias"]: md += [f"**{c['rotulo']}**", "```", c["texto"], "```", ""]
    return passos, md

# ---------------- montar e mandar ----------------
def main():
    seg = segunda(); semana = f"{seg.isocalendar()[0]}-w{seg.isocalendar()[1]:02d}"
    cal = calendario()
    desde = None if ENSAIO else datetime.datetime.now(BR).date() + datetime.timedelta(days=1)  # dia que ja passou (ou hoje) nao se agenda
    a = next((x.split("=")[1] for x in sys.argv if x.startswith("--desde=")), None)
    if a: desde = datetime.date.fromisoformat(a)
    # a mesma semana nao se escreve duas vezes (o robo de segunda e o comando a mao): gastaria credito a toa
    raiz = drive.achar("posts", drive.achar("Tiao Poupador"))
    feita = drive.achar(semana, raiz) if raiz else None
    if feita and not ENSAIO and "--forcar" not in sys.argv and any(f["name"] == "itens.json" for f in drive.listar(feita)):
        log(f"a semana {semana} já foi escrita e mandada ao Team (use --forcar para refazer)"); return
    comunidade = ""
    try:
        from fabrica.comentarios import ler_caderno
        d = [i for i in ler_caderno().get("semana", []) if i.get("tipo") == "destaque"]
        if d: comunidade = d[-1]["texto"]
    except Exception: pass
    # antes da tarefa nova: o que o Ed escreveu nas anteriores (notas dos passos e conversa), manual secao 3
    from fabrica import team
    ant = [f"tiao-posts-{(seg - datetime.timedelta(weeks=k)).isocalendar()[0]}-w{(seg - datetime.timedelta(weeks=k)).isocalendar()[1]:02d}" for k in (1, 2)]
    rec = []
    try: rec = team.recados(ant)
    except Exception as e: log("recados do Team não vieram:", e)
    log("📝 recados do Ed nas tarefas anteriores:" + ("".join(f"\n  {r}" for r in rec) if rec else " nenhum"))
    pl, vids = plano(seg, cal, comunidade, desde)
    if not pl: log("nenhum dia por agendar nesta semana"); return
    log(f"📅 semana {seg:%d/%m}: " + " · ".join(f"{d} {x['data']:%d/%m} {t}" + (f" (vídeo {x['video']})" if x['video'] else "") for d, t, _, x in pl))
    posts, custo = escrever(pl, [v for v in vids.values() if v["roteiro"]], rec)
    sai = f"{P}/fabrica/saida/posts-{semana}"; os.makedirs(sai, exist_ok=True)
    pasta = None if ENSAIO else drive.pasta(semana, drive.pasta("posts", drive.pasta("Tiao Poupador")))
    itens = []
    for i, (p, (dia, tipo, _, x)) in enumerate(zip(posts, pl)):
        cod = f"P{i + 1}"; txt = p["texto"].strip(); v = vids.get(x["video"]) if x["video"] else None
        url_v = f"https://youtu.be/{v['id']}" if v and v.get("id") else ""  # sem o id, o passo avisa (nada de texto provisorio a colar)
        if url_v: txt += f"\n\n▶️ {url_v}"
        url_img, cena, capa, img_cam = None, "", False, ""
        if x["cena"] and p["cena"]:
            cena = p["cena"]; arq_img = f"{sai}/{cod}-{dia}.jpg"
            if not ENSAIO and imagem(cena, arq_img):
                url_img = f"https://drive.google.com/file/d/{drive.subir(arq_img, pasta)['id']}/view"
                img_cam = "\\".join([PC, "posts", semana, os.path.basename(arq_img)])
            time.sleep(5)
        elif v and v.get("capa"): url_img, capa, img_cam = f"https://drive.google.com/file/d/{v['capa']}/view", True, "\\".join([PC, "robo", f"video-{v['nn']}", "capa.jpg"])
        itens.append({"data": x["data"], "nn": x["video"], "dia": dia, "tipo": tipo, "texto": txt, "opcoes": p["opcoes"], "correta": p["correta"], "explicacao": p["explicacao"],
                      "cena": cena, "url_img": url_img, "capa": capa, "img_caminho": img_cam, "video": url_v, "falta_link": bool(v and not url_v)})
    passos, md = montar(seg, itens)
    for p in passos:  # a pasta onde salvar a imagem (regra do Team, Ed 19/11)
        if p.get("ficheiro") and pasta: p["pasta"] = {"rotulo": f"Google Drive > Tiao Poupador > posts > {semana}", "url": f"https://drive.google.com/drive/folders/{pasta}"}
    json.dump(itens, open(f"{sai}/itens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    open(f"{sai}/posts.md", "w", encoding="utf-8").write("\n".join(md))
    log("\n".join(md))
    if ENSAIO: log(f"\n(ensaio: nada enviado) custo US$ {custo:.3f}"); return
    from fabrica import correio
    try:
        r = team.mandar({"chave_unica": f"tiao-posts-{semana}", "tipo": "posts-da-semana", "projeto": "Tião Poupador",
                         "titulo": f"Posts do YouTube de {itens[0]['data']:%d/%m} a {itens[-1]['data']:%d/%m} ({len(passos)} para agendar)", "descricao": DESCRICAO,
                         "prazo": f"{itens[0]['data'].isoformat()}T12:00:00-03:00", "passos": passos})
        drive.subir(f"{sai}/itens.json", pasta)  # marca da semana feita
        log("Team:", r.get("criada"), r.get("url"))
    except Exception as e: log("Team recusou (vai só o e-mail):", e)
    if datetime.date.today().isoformat() <= "2026-11-20": correio.enviar(f"Tião Poupador · posts do YouTube da semana {seg:%d/%m} (7 para agendar)", "\n".join(md))
    try:  # o destaque usado sai da fila
        from fabrica.comentarios import ler_caderno, gravar_caderno
        c = ler_caderno(); c["semana"] = []; gravar_caderno(c)
    except Exception: pass

if __name__ == "__main__":
    main()
