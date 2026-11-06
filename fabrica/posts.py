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
     ("segunda", "texto", f"O VÍDEO DE ONTEM (domingo): «{dom['titulo']}». Conte em 2 ou 3 frases, na voz do Tião, o problema que o vídeo mostra, como quem já passou por isso, e termine convidando a assistir. NÃO escreva link."),
     ("terça", "enquete", f"ENQUETE sobre o tema do vídeo de domingo («{dom['titulo']}»): uma situação do dia a dia em que a pessoa se reconhece. 3 ou 4 opções curtas, todas plausíveis, nenhuma 'certa'."),
     ("quarta", "texto", f"O AVISO DE HOJE: hoje, quarta, às 18h, estreia o vídeo novo: «{qua['titulo']}». Desperte curiosidade pelo problema, sem entregar o final."),
     ("quinta", "texto", f"O VÍDEO DE ONTEM (quarta): «{qua['titulo']}». 2 ou 3 frases na voz do Tião sobre o problema, convidando a assistir. NÃO escreva link."),
     ("sexta", "quiz", "QUIZ: uma pergunta com UMA resposta certa, tirada de um fato dos vídeos da semana (só fatos que estão nos roteiros). 3 ou 4 opções curtas; diga qual é a certa em 'correta' (0 a 3) e escreva em 'explicacao' 1 frase curta que o YouTube mostra depois da resposta."),
     ("sábado", "texto", (f"A COMUNIDADE: um de vocês contou isto nos comentários (NÃO diga o nome da pessoa): «{comunidade}». Comente como o Tião, com carinho e humor, e pergunte quem mais já passou por isso."
                          if comunidade else "O CADERNO DO TIÃO: uma dica curta e concreta tirada dos vídeos da semana, que a pessoa pode usar hoje, contada como algo que o Tião faz na vida dele. Sem conta, sem lista longa.")),
     ("domingo", "texto", f"O AVISO DE HOJE: hoje, domingo, às 17h, estreia o vídeo novo: «{dom2['titulo'] or '(tema ainda não definido: diga só que hoje às 17h tem história nova do Tião)'}». Desperte curiosidade, sem entregar o final."),
    ]
def pedido(pl, vids):
    ctx = "\n\n".join(f"═══ ROTEIRO DO VÍDEO «{v['titulo']}» ═══\n{v['roteiro'][:14000]}" for v in vids if v["roteiro"])
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
Nos posts de TEXTO de quarta, sábado e domingo, escreva também "cena": 1 ou 2 frases descrevendo UMA imagem quadrada com o Tião (o que ele faz, onde, com que objeto do dia a dia, a emoção), em inglês. A cena NÃO pode pedir palavra, número, valor, placa, etiqueta, cartaz, logotipo nem tela com texto. Nos outros posts, "cena" fica vazia (segunda e quinta usam a capa do vídeo)."""
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
        if dia in ("quarta", "sábado", "domingo"):
            if len(p["cena"]) < 30: erros.append(f"{r}: falta a 'cena' da imagem")
            elif m := CENA_COM_LETRAS.search(p["cena"]): erros.append(f"{r}: a cena pede «{m[0]}»; a imagem não pode ter letras nem números")
    return erros
def escrever(pl, vids):
    import anthropic
    cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"]); base = pedido(pl, vids); ok = numeros(vids); erros, versao, custo = [], None, 0.0
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
def imagem(cena, arq):
    e = chaves(); b = uuid.uuid4().hex; corpo = []
    def campo(k, v, nome=None):
        cab = f'--{b}\r\nContent-Disposition: form-data; name="{k}"' + (f'; filename="{nome}"\r\nContent-Type: image/jpeg' if nome else "") + "\r\n\r\n"
        corpo.append(cab.encode() + (v if isinstance(v, bytes) else v.encode()) + b"\r\n")
    pr = ("Flat 2D cartoon illustration, clean thin black outlines, soft cel shading, warm colors, square 1:1 social media post image, simple background. "
          "The character must be IDENTICAL to the reference images: Tiao, about 30, short and slightly chubby, round face, short messy black hair, a THIN black pencil mustache, "
          "light brown skin, mustard yellow polo shirt, faded denim shorts, black flip-flops, black wristwatch. The second reference is his character sheet: draw him ONCE, in a natural pose. "
          f"Scene: {cena} Correct anatomy, five fingers. ABSOLUTELY NO text, letters, numbers, signs, logos or screens with writing anywhere.")
    campo("prompt", pr); campo("width", "1024"); campo("height", "1024")
    for n, r in enumerate(("tiao-frente-sozinho.jpg", "tiao-ficha-oficial.jpg")): campo(f"input_image_{n}", open(f"{P}/banco/referencia/{r}", "rb").read(), f"r{n}.jpg")
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{e['CLOUDFLARE_TIAO_CONTA']}/ai/run/@cf/black-forest-labs/flux-2-klein-4b",
                                 data=b"".join(corpo) + f"--{b}--\r\n".encode(), method="POST", headers={"Authorization": "Bearer " + e["CLOUDFLARE_TIAO"], "Content-Type": "multipart/form-data; boundary=" + b})
    try: open(arq, "wb").write(base64.b64decode(json.load(urllib.request.urlopen(req, timeout=180))["result"]["image"])); return True
    except Exception as x: log("imagem não saiu (o Ed gera pela cena):", getattr(x, "code", x)); return False

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
    pl = plano(vd, vq, vd2, comunidade); posts, custo = escrever(pl, [v for v in (vd, vq, vd2) if v["roteiro"]])
    sai = f"{P}/fabrica/saida/posts-{semana}"; os.makedirs(sai, exist_ok=True)
    links = {"segunda": vd, "quinta": vq}
    pasta = None if ENSAIO else drive.pasta(semana, drive.pasta("posts", drive.pasta("Tiao Poupador")))
    passos, md = [], [f"# Tião Poupador · posts da semana {seg:%d/%m} a {seg + datetime.timedelta(days=6):%d/%m}", "",
                      "Cole cada um no YouTube Studio (Criar > Criar post), anexe a imagem e **agende para o dia e a hora indicados**.", ""]
    for i, (p, (dia, tipo, _)) in enumerate(zip(posts, pl)):
        data = seg + datetime.timedelta(days=i); cod = f"P{i + 1}"; txt = p["texto"].strip()
        v = links.get(dia)
        if v and v.get("id"): txt += f"\n\n▶️ https://youtu.be/{v['id']}"
        elif v: txt += "\n\n▶️ (o link do vídeo: cole o do vídeo de " + ("domingo" if dia == "segunda" else "quarta") + ")"
        arq_img, url_img = None, None
        if dia in ("quarta", "sábado", "domingo") and p["cena"]:
            arq_img = f"{sai}/{cod}-{dia}.jpg"
            if not ENSAIO and imagem(p["cena"], arq_img): url_img = f"https://drive.google.com/file/d/{drive.subir(arq_img, pasta)['id']}/view"
            time.sleep(5)
        elif v and v.get("capa"): url_img = f"https://drive.google.com/file/d/{v['capa']}/view"
        tit = {"texto": "📝 texto", "enquete": "📊 enquete", "quiz": "🧠 quiz"}[tipo]
        extra = ""
        if tipo in ("enquete", "quiz"):
            extra = "\nOpções (uma em cada campo):\n" + "\n".join(f"{'✅ ' if tipo == 'quiz' and k == p['correta'] else '- '}{o}" for k, o in enumerate(p["opcoes"]))
            if tipo == "quiz": extra += f"\nExplicação (aparece depois da resposta): {p['explicacao']}"
        quando_txt = f"{dia} {data:%d/%m}, agendar para as 12h (Brasília)"
        passos.append({"codigo": cod, "texto": f"{dia.capitalize()} {data:%d/%m} · {tit} · agendar 12h" + (" · enquete não leva imagem" if tipo != "texto" else ""),
                       "copiar": txt + extra, "links": [{"rotulo": "A imagem do post", "url": url_img}] if url_img else [], "ficheiro": f"{cod}-{dia}.jpg" if url_img else ""})
        md += [f"### {cod} · {quando_txt} · {tit}", "", "```", txt, "```"] + ([extra.strip(), ""] if extra else [""]) + \
              ([f"🖼️ **Imagem:** {url_img}", ""] if url_img else ([f"🎨 Cena para gerar (a Cloudflare não fez): {p['cena']}", ""] if p["cena"] else [""]))
    open(f"{sai}/posts.md", "w", encoding="utf-8").write("\n".join(md))
    log("\n".join(md))
    if ENSAIO: log(f"\n(ensaio: nada enviado) custo US$ {custo:.3f}"); return
    from fabrica import team, correio
    try:
        r = team.mandar({"chave_unica": f"tiao-posts-{semana}", "tipo": "posts-da-semana", "projeto": "Tião Poupador",
                         "titulo": f"Posts do YouTube da semana {seg:%d/%m} (7 para agendar)", "descricao": "Cole no YouTube Studio (Criar > Criar post) e agende cada um para o dia indicado, às 12h de Brasília.",
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
