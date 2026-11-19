# Peca do robo: os 7 posts da semana da aba "Posts" do YouTube (modelo: FINMOOVI/blog-finmoovi/src/scripts/youtube/posts-semana.js).
# A API do YouTube NAO cria posts: o robo escreve, faz as imagens e manda para o Apexi Team; o Ed cola e AGENDA no Studio.
# Pedido do Ed (06/11/2026): «pode ser assim». Um post por dia, as 12h de Brasilia, em volta dos 2 videos da semana:
#   seg: o video de domingo (link + capa) · ter: enquete · qua: "hoje as 18h" · qui: o video de quarta (link + capa)
#   sex: quiz (resposta certa) · sab: a comunidade (melhor comentario, sem nome) ou o caderno do Tiao · dom: "hoje as 17h"
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
COM_CENA = ("terça", "quarta", "sábado", "domingo")  # a enquete de terça leva imagem; o quiz de sexta e so de texto (Ed, 18/11)
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
    r = next((f for f in os.listdir(f"{P}/roteiros") if f.startswith(f"{nn}-") and f.endswith(".md") and "pedidos" not in f), None)
    if r: v["roteiro"] = open(f"{P}/roteiros/{r}", encoding="utf-8").read()
    try:
        pasta = drive.achar(f"video-{nn}", drive.achar("robo", drive.achar("Tiao Poupador")))
        for f in drive.listar(pasta) if pasta else []:
            if f["name"] == "publicado.json": v["id"] = json.loads(api(f"{D}/{f['id']}?alt=media", bruto=True)).get("id")
            if f["name"] == "capa.jpg": v["capa"] = f["id"]
    except Exception as e: log("Drive:", e)
    return v

# ---------------- o pedido ao Claude ----------------
def plano(dom, qua, dom2, comunidade):
    return [
     ("segunda", "texto", f"O VÍDEO DE ONTEM (domingo): «{dom['titulo']}». Conte em 2 ou 3 frases, na voz do Tião, o problema que o vídeo mostra, como quem já passou por isso, e termine convidando a assistir. NÃO escreva link."
                          if dom["titulo"] else f"UMA CONVERSA DE SEGUNDA (ontem NÃO teve vídeo, não diga que teve): 2 ou 3 frases na voz do Tião sobre uma situação do dia a dia ligada ao vídeo de quarta («{qua['titulo']}»), e termine dizendo que quarta, às 18h, tem vídeo novo."),
     ("terça", "enquete", f"ENQUETE sobre o tema do vídeo de domingo («{dom['titulo']}»): uma situação do dia a dia em que a pessoa se reconhece. 3 ou 4 opções curtas, todas plausíveis, nenhuma 'certa'."),
     ("quarta", "texto", f"O AVISO DE HOJE: hoje, quarta, às 18h, estreia o vídeo novo: «{qua['titulo']}». Desperte curiosidade pelo problema, sem entregar o final."),
     ("quinta", "texto", f"O VÍDEO DE ONTEM (quarta): «{qua['titulo']}». 2 ou 3 frases na voz do Tião sobre o problema, convidando a assistir. NÃO escreva link."
                         if qua["titulo"] else "UMA CONVERSA DE QUINTA (ontem NÃO teve vídeo, não diga que teve): 2 ou 3 frases na voz do Tião sobre uma situação do dia a dia ligada aos vídeos da semana, terminando com uma pergunta para os comentários."),
     ("sexta", "quiz", "QUIZ: uma pergunta com UMA resposta certa, tirada de um fato dos vídeos da semana (só fatos que estão nos roteiros). 3 ou 4 opções curtas; diga qual é a certa em 'correta' (0 a 3) e escreva em 'explicacao' 1 frase curta que o YouTube mostra depois da resposta."),
     ("sábado", "texto", (f"A COMUNIDADE: um de vocês contou isto nos comentários (NÃO diga o nome da pessoa): «{comunidade}». Comente como o Tião, com carinho e humor, e pergunte quem mais já passou por isso."
                          if comunidade else "O CADERNO DO TIÃO: uma dica curta e concreta tirada dos vídeos da semana, que a pessoa pode usar hoje, contada como algo que o Tião faz na vida dele. Sem conta, sem lista longa.")),
     ("domingo", "texto", f"O AVISO DE HOJE: hoje, domingo, às 17h, estreia o vídeo novo: «{dom2['titulo'] or '(tema ainda não definido: diga só que hoje às 17h tem história nova do Tião)'}». Desperte curiosidade, sem entregar o final."),
    ]
def pedido(pl, vids, recados=()):
    ctx = "\n\n".join(f"═══ ROTEIRO DO VÍDEO «{v['titulo']}» ═══\n{v['roteiro'][:14000]}" for v in vids if v["roteiro"])
    if recados: ctx += "\n\n═══ O QUE O DONO DO CANAL ESCREVEU NAS TAREFAS ANTERIORES (siga isto, vale mais que o resto) ═══\n" + "\n".join(f"- {r}" for r in recados)
    return f"""Você escreve os posts da aba "Posts" do canal de YouTube Tião Poupador. Quem fala é o próprio Tião, na primeira pessoa: um brasileiro simples, uns 30 anos, que aprendeu a cuidar do dinheiro no dia a dia (caderno, lista, sem dívida). Público: famílias brasileiras de classe média e baixa.
Linguagem: português do Brasil, simples, conversa de vizinho, frases curtas, no máximo 1 ou 2 emojis por post, sem jargão.

{ctx}

═══ OS 7 POSTS ═══
""" + "\n".join(f"{i + 1}. {d.upper()} ({t}): {p}" for i, (d, t, p) in enumerate(pl)) + f"""

═══ PROIBIDO (reprova) ═══
- Pedir para a pessoa fazer conta, somar, calcular, anotar ou ir buscar o extrato. Pergunte pelo que ela JÁ VIVEU.
- Dizer que o FinMoovi é grátis, de graça ou gratuito (ele tem 7 dias de teste). Nem precisa falar do app.
- Qualquer número que não esteja nos roteiros acima (as horas 17h e 18h podem).
- Escrever links ou endereços (o robô coloca depois).
- Travessão (o traço comprido). Use vírgula ou ponto.
- Mais de {LIMITE_TEXTO} caracteres por texto; opção de enquete ou quiz com mais de {LIMITE_OPCAO} caracteres.

═══ A IMAGEM ═══
Na ENQUETE de terça e nos posts de TEXTO de quarta, sábado e domingo, escreva também "cena": 1 ou 2 frases descrevendo UMA imagem quadrada com o Tião (o que ele faz, onde, com que objeto do dia a dia, a emoção), em inglês. A cena NÃO pode pedir palavra, número, valor, placa, etiqueta, cartaz, logotipo nem tela com texto. Nos outros posts, "cena" fica vazia (segunda e quinta usam a capa do vídeo; o quiz de sexta é só de texto)."""
ESQ = {"type": "object", "properties": {"posts": {"type": "array", "items": {"type": "object", "properties": {
    "dia": {"type": "string"}, "texto": {"type": "string"}, "opcoes": {"type": "array", "items": {"type": "string"}},
    "correta": {"type": "integer"}, "explicacao": {"type": "string"}, "cena": {"type": "string"}},
    "required": ["dia", "texto", "opcoes", "correta", "explicacao", "cena"], "additionalProperties": False}}},
    "required": ["posts"], "additionalProperties": False}
def numeros(vids):
    s = set(re.findall(r"\d+(?:[.,]\d+)?", " ".join(v["roteiro"] + " " + v["titulo"] for v in vids))); s |= {"7", "17", "18", "17h", "18h"}; return s
def validar(posts, pl, ok_num):
    erros = []
    if len(posts) != len(pl): return [f"são {len(pl)} posts, vieram {len(posts)}"]
    for i, (p, (dia, tipo, _)) in enumerate(zip(posts, pl)):
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
        if dia in COM_CENA:
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
def copias(it):
    """cada coisa a colar, pela ordem em que se cola no Studio"""
    if it["tipo"] == "texto": c = [{"rotulo": "Texto do post", "texto": it["texto"]}]
    else: c = [{"rotulo": "Pergunta", "texto": it["texto"]}] + [{"rotulo": f"Opção {LETRAS[k]}", "texto": o.strip()} for k, o in enumerate(it["opcoes"])]
    if it["tipo"] == "quiz": c.append({"rotulo": "Explicação (depois da resposta)", "texto": frase(it["explicacao"])})
    if it.get("cena"): c.append({"rotulo": "Prompt da imagem (Meta AI)", "texto": prompt_imagem(it["cena"])})
    return c
def refs_tiao():  # as fotos do Tiao no Drive, para anexar quando o Ed gera a imagem a mao
    try:
        ref = drive.achar("referencia", drive.achar("Tiao Poupador"))
        return [{"rotulo": "📎 Anexar no Meta AI: " + f["name"], "url": f"https://drive.google.com/file/d/{f['id']}/view"}
                for f in drive.listar(ref) if f["name"] in ("tiao-sem-caneca.jpg", "tiao-ficha-oficial.jpg")]
    except Exception: return []
DESCRICAO = "\n".join([
    "Post de texto: copie o texto; a imagem vem no link (capa do vídeo ou a que o robô fez) ou gere no Meta AI com o prompt e as fotos do Tião. No YouTube Studio: Criar > Criar post, cole o texto, junte a imagem, seta ao lado de Publicar > Agendar.",
    "Enquete (terça, com imagem): Criar > Criar post > Enquete. A pergunta vai no 1º campo e cada opção no seu, junte a imagem.",
    "Quiz (sexta, só de texto): Criar > Criar post > Quiz. Pergunta, opções, marque a certa (vem no título do passo) e cole a explicação.",
    "O YouTube não deixa robô publicar posts, por isso vêm para agendar à mão."])
def montar(seg, itens):
    """itens: dia, tipo, texto (ja com o link), opcoes, correta, explicacao, cena, url_img, capa, video, falta_link -> (passos do Team, texto do e-mail)"""
    passos, md, refs = [], [f"# Tião Poupador · posts da semana {seg:%d/%m} a {seg + datetime.timedelta(days=6):%d/%m}", "",
                            "Cole cada um no YouTube Studio (Criar > Criar post) e **agende para o dia e a hora indicados**.", ""], None
    for i, it in enumerate(itens):
        data = seg + datetime.timedelta(days=i); dia = it["dia"]; fmt = formato(it)
        texto = f"{fmt} · {NOME_DIA[dia]} {data:%d/%m} · agendar para as 12h"
        if it["tipo"] == "quiz": texto += f" · resposta certa: Opção {LETRAS[it['correta']]}"
        if it.get("falta_link"): texto += f" · ⚠️ falta o link do vídeo de {'domingo' if dia == 'segunda' else 'quarta'}: junte-o no fim do texto"
        p = {"codigo": f"post-{data.isoformat()}", "texto": texto, "copias": copias(it), "links": [STUDIO]}
        if it.get("video"): p["links"].append({"rotulo": "▶️ O vídeo deste post", "url": it["video"]})
        if tem_img(it):
            if it.get("capa"): p["links"].append({"rotulo": "🖼️ A imagem: a capa do vídeo (baixar)", "url": it["url_img"]})
            else:
                if it.get("url_img"): p["links"].append({"rotulo": "🖼️ A imagem que o robô já fez (se não gostar, gere no Meta AI)", "url": it["url_img"]})
                if refs is None: refs = [] if ENSAIO else refs_tiao()
                p["links"] += [META_AI] + refs
            p["ficheiro"] = f"post-{data.isoformat()}-{SIGLA[dia]}.jpg"; p["formato"] = "1:1"
        passos.append(p)
        md += [f"### {texto}", ""] + [l for l in (f"🖼️ {x['rotulo']}: {x['url']}" for x in p["links"][1:])] + [""]
        for c in p["copias"]: md += [f"**{c['rotulo']}**", "```", c["texto"], "```", ""]
    return passos, md

# ---------------- montar e mandar ----------------
def main():
    seg = segunda(); semana = f"{seg.isocalendar()[0]}-w{seg.isocalendar()[1]:02d}"
    cal = calendario(); quando = lambda c: datetime.datetime.fromisoformat(c["quando"]).date()
    dom = next((c for c in cal if quando(c) == seg - datetime.timedelta(days=1)), None)
    qua = next((c for c in cal if quando(c) == seg + datetime.timedelta(days=2)), None)
    dom2 = next((c for c in cal if quando(c) == seg + datetime.timedelta(days=6)), None)
    vazio = {"nn": "", "titulo": "", "roteiro": "", "id": None, "capa": None}
    vd, vq, vd2 = [video(c["nn"]) if c else dict(vazio) for c in (dom, qua, dom2)]
    log(f"📅 semana {seg:%d/%m}: domingo «{vd['titulo']}» · quarta «{vq['titulo']}» · domingo que vem «{vd2['titulo']}»")
    if not vd["titulo"] and not vq["titulo"]: log("sem vídeos nesta semana, nada a escrever"); return
    comunidade = ""
    try:
        from fabrica.comentarios import ler_caderno
        d = [i for i in ler_caderno().get("semana", []) if i.get("tipo") == "destaque"]
        if d: comunidade = d[-1]["texto"]
    except Exception: pass
    # antes da tarefa nova: o que o Ed escreveu nas anteriores (notas dos passos e conversa), manual secao 3
    from fabrica import team
    ant = [f"tiao-posts-{(seg - datetime.timedelta(weeks=k)).isocalendar()[0]}-w{(seg - datetime.timedelta(weeks=k)).isocalendar()[1]:02d}" for k in (1, 2)]
    ant += [team.chave_unica(v["nn"]) for v in (vd, vq) if v["nn"]]
    rec = []
    try: rec = team.recados(ant)
    except Exception as e: log("recados do Team não vieram:", e)
    log("📝 recados do Ed nas tarefas anteriores:" + ("".join(f"\n  {r}" for r in rec) if rec else " nenhum"))
    pl = plano(vd, vq, vd2, comunidade); posts, custo = escrever(pl, [v for v in (vd, vq, vd2) if v["roteiro"]], rec)
    sai = f"{P}/fabrica/saida/posts-{semana}"; os.makedirs(sai, exist_ok=True)
    links = {"segunda": vd, "quinta": vq}
    pasta = None if ENSAIO else drive.pasta(semana, drive.pasta("posts", drive.pasta("Tiao Poupador")))
    itens = []
    for i, (p, (dia, tipo, _)) in enumerate(zip(posts, pl)):
        cod = f"P{i + 1}"; txt = p["texto"].strip(); v = links.get(dia) if (links.get(dia) or {}).get("titulo") else None
        url_v = f"https://youtu.be/{v['id']}" if v and v.get("id") else ""  # sem o id, o passo avisa (nada de texto provisorio a colar)
        if url_v: txt += f"\n\n▶️ {url_v}"
        url_img, cena, capa = None, "", False
        if dia in COM_CENA and p["cena"]:
            cena = p["cena"]; arq_img = f"{sai}/{cod}-{dia}.jpg"
            if not ENSAIO and imagem(cena, arq_img): url_img = f"https://drive.google.com/file/d/{drive.subir(arq_img, pasta)['id']}/view"
            time.sleep(5)
        elif v and v.get("capa"): url_img, capa = f"https://drive.google.com/file/d/{v['capa']}/view", True
        itens.append({"dia": dia, "tipo": tipo, "texto": txt, "opcoes": p["opcoes"], "correta": p["correta"], "explicacao": p["explicacao"],
                      "cena": cena, "url_img": url_img, "capa": capa, "video": url_v, "falta_link": bool(v and not url_v)})
    passos, md = montar(seg, itens)
    for p in passos:  # a pasta onde salvar a imagem (regra do Team, Ed 19/11)
        if p.get("ficheiro") and pasta: p["pasta"] = {"rotulo": f"Google Drive > Tiao Poupador > posts > {semana}", "url": f"https://drive.google.com/drive/folders/{pasta}"}
    json.dump(itens, open(f"{sai}/itens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(f"{sai}/posts.md", "w", encoding="utf-8").write("\n".join(md))
    log("\n".join(md))
    if ENSAIO: log(f"\n(ensaio: nada enviado) custo US$ {custo:.3f}"); return
    from fabrica import correio
    try:
        r = team.mandar({"chave_unica": f"tiao-posts-{semana}", "tipo": "posts-da-semana", "projeto": "Tião Poupador",
                         "titulo": f"Posts do YouTube da semana {seg:%d/%m} (7 para agendar)", "descricao": DESCRICAO,
                         "prazo": f"{seg.isoformat()}T12:00:00-03:00", "passos": passos})
        log("Team:", r.get("criada"), r.get("url"))
    except Exception as e: log("Team recusou (vai só o e-mail):", e)
    if datetime.date.today().isoformat() <= "2026-11-20": correio.enviar(f"Tião Poupador · posts do YouTube da semana {seg:%d/%m} (7 para agendar)", "\n".join(md))
    try:  # o destaque usado sai da fila
        from fabrica.comentarios import ler_caderno, gravar_caderno
        c = ler_caderno(); c["semana"] = []; gravar_caderno(c)
    except Exception: pass

if __name__ == "__main__":
    main()
