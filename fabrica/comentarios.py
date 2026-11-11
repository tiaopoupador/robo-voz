# Peca do robo: os comentarios do YouTube do Tiao Poupador (modelo: FINMOOVI/blog-finmoovi/src/scripts/youtube/comentarios.js).
# Pedido do Ed (06/11/2026): respostas com a voz do Tiao (Claude, creditos CLAUDE_TIAO), esconder spam, primeira pessoa.
#
# O que faz, a cada rodada:
#   1. primeiro comentario do canal em cada video publico (a pergunta do video + o link). FIXAR e a mao no Studio:
#      a API do YouTube nao tem esse comando.
#   2. le os comentarios novos; o Claude decide para cada um: responder (voz do Tiao), link (pediu o app),
#      spam (vai para "em revisao", nada se apaga), humano (ofensa, politica, conselho de investimento: fica para o Ed), ignorar.
#   3. responde com calma (teto por rodada, pausa entre respostas).
#   4. uma vez por dia: resumo no Apexi Team (os melhores, o que precisa do Ed, pedidos de tema).
# Travas (iguais ao FinMoovi): nunca responder duas vezes, nunca responder a si mesmo, caderno de quem ja foi visto
# (no Drive: Tiao Poupador/robo/comentarios.json, para nao ficar no repositorio publico).
# Uso: python fabrica/comentarios.py [--ensaio] [--max=15]
import datetime, json, os, random, re, sys, time, urllib.error, urllib.parse
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import api, chaves
from fabrica import drive
from fabrica.drive import D
Y = "https://www.googleapis.com/youtube/v3"
ENSAIO = "--ensaio" in sys.argv
MAX = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--max=")), 8)   # 8 com pausas de gente cabem nos 30 min da nuvem
MODELO = "claude-sonnet-5-5"   # US$ 2 / 10 por milhao de tokens: uns US$ 0,003 por resposta
LINK = "https://finmoovi.com/?utm_source=youtube&utm_medium=tiao-poupador&utm_campaign={c}"
PERGUNTA_01 = "Na sua rua, você é o Tião ou já foi o Marcos?"
QUENTE_H = 48   # nas primeiras 48 h do video ele e olhado toda hora; depois, de 6 em 6 horas
log = lambda *m: print(*m, flush=True)

# ---------------- caderno (no Drive) ----------------
def _robo(): return drive.pasta("robo", drive.pasta("Tiao Poupador"))
def ler_caderno():
    for f in drive.listar(_robo()):
        if f["name"] == "comentarios.json": return json.loads(api(f"{D}/{f['id']}?alt=media", bruto=True))
    return {"vistos": {}, "primeiro": {}, "para_resumo": [], "ultimo_resumo": ""}
def gravar_caderno(c):
    arq = f"{P}/fabrica/saida/comentarios.json"; os.makedirs(os.path.dirname(arq), exist_ok=True)
    json.dump(c, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pai = _robo()
    for f in drive.listar(pai):
        if f["name"] == "comentarios.json": api(f"{D}/{f['id']}", metodo="DELETE", bruto=True)
    drive.subir(arq, pai)

# ---------------- YouTube ----------------
def yt(caminho, **q): return api(f"{Y}/{caminho}?" + urllib.parse.urlencode(q))
def canal():
    c = yt("channels", part="id,contentDetails", mine="true")["items"][0]
    return c["id"], c["contentDetails"]["relatedPlaylists"]["uploads"]
def videos_publicos(uploads):
    ids = [i["contentDetails"]["videoId"] for i in yt("playlistItems", part="contentDetails", playlistId=uploads, maxResults=50).get("items", [])]
    if not ids: return []
    vs = yt("videos", part="snippet,status", id=",".join(ids)).get("items", [])
    return [{"id": v["id"], "titulo": v["snippet"]["title"], "desc": v["snippet"].get("description", "")[:600],
             "quando": v["snippet"]["publishedAt"]} for v in vs if v["status"]["privacyStatus"] == "public"]
def conversas(vid):
    try: r = yt("commentThreads", part="snippet,replies", videoId=vid, maxResults=100, order="time", textFormat="plainText")
    except urllib.error.HTTPError as e:
        if e.code == 403: return []   # comentarios desligados
        raise
    return r.get("items", [])
def numero_do_video(v):
    """o numero (02, 03...) pelo publicado.json do Drive; o 01 foi subido a mao"""
    if v["id"] == "gC6RSDz8-3Q": return "01"
    try:
        robo = _robo()
        for p in drive.listar(robo):
            if p["name"].startswith("video-") and p["mimeType"].endswith("folder"):
                for f in drive.listar(p["id"]):
                    if f["name"] == "publicado.json" and json.loads(api(f"{D}/{f['id']}?alt=media", bruto=True)).get("id") == v["id"]: return p["name"][6:]
    except Exception: pass
    return None
def pergunta_do_video(nn):
    if nn == "01": return PERGUNTA_01
    try:
        import importlib; return importlib.import_module(f"fabrica.videos.v{nn}.cenas").PERGUNTA
    except Exception: return None
def primeiro_texto(nn):
    q = pergunta_do_video(nn) if nn else None
    return ((f"👇 {q}\n\n" if q else "") + "📲 O FinMoovi, o app que eu uso para não cair nessas, tem 7 dias de teste e abre no navegador:\n"
            + LINK.format(c=f"video{nn or ''}") + "\n\nToda semana tem história nova do Tião. Se inscreve no canal! 🙌")
def escrever_conversa(vid, texto):
    return api(f"{Y}/commentThreads?part=snippet", {"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": texto}}}})
def responder(pai, texto):
    return api(f"{Y}/comments?part=snippet", {"snippet": {"parentId": pai, "textOriginal": texto}})
def segurar(cid):  # spam: fica "em revisao" no Studio, o Ed decide. Nada se apaga.
    return api(f"{Y}/comments/setModerationStatus?" + urllib.parse.urlencode({"id": cid, "moderationStatus": "heldForReview"}), b"", metodo="POST", tipo="application/x-www-form-urlencoded", bruto=True)

# ---------------- o Claude (a voz do Tiao) ----------------
SISTEMA = """Você é o Tião, o personagem do canal Tião Poupador no YouTube: um brasileiro simples, uns 30 anos, que aprendeu a cuidar do dinheiro no dia a dia (caderno, lista de compras, sem dívida). Você responde os comentários dos seus vídeos, em português do Brasil, na primeira pessoa.

Para cada comentário, decida a ação:
- "responder": comentário normal, história, opinião, elogio, dúvida simples sobre o vídeo. Escreva a resposta.
- "link": a pessoa pede o app, o nome do app ou o link. Responda curto e diga que o link está no primeiro comentário e na descrição (não escreva o link, o robô coloca).
- "spam": propaganda, link estranho, golpe, "me chama no zap", pirâmide, sorteio falso, perfil vendendo curso.
- "humano": ofensa pesada, política, religião, briga, assunto delicado (luto, doença, dívida grave, desespero), ou pedido de conselho de investimento pessoal ("onde ponho meu dinheiro", "vale a pena tal ação"). NÃO responda: o dono do canal vê.
- "ignorar": só emoji, texto sem sentido, ou algo que não pede resposta.

Como o Tião escreve (tem de parecer gente, nunca atendimento de empresa):
- Escreve como no celular: "vc", "pra", "tá", "né", "kkkk" quando é engraçado. Pode começar com letra minúscula. Pontuação simples, sem frase perfeitinha.
- Tamanho varia de verdade: às vezes 3 palavras ("kkkk é bem assim"), às vezes 1 frase, no máximo 2 frases e 220 caracteres.
- Responde ao detalhe que a pessoa contou, com uma reação sincera (ri, concorda, conta um pedacinho seu: o caderno, a lista do mercado, a Sandra, o Marcos, a rua).
- Em mais ou menos 1 de cada 3 respostas, devolve uma pergunta curta para a conversa continuar ("e aí, deu certo?", "qual foi o pior gasto?").
- Às vezes usa o primeiro nome da pessoa, quase sempre não.
- Emoji: na maioria das vezes nenhum, no máximo 1.
- Proibido: "Que legal", "Ótima pergunta", "Obrigado pelo comentário", "Fico feliz", "Com certeza!", "Excelente", "Seja bem-vindo", começar com "Opa" ou com o nome em toda resposta, e qualquer frase que sirva para qualquer comentário.
- Cada resposta começa de um jeito diferente das outras do lote E das respostas recentes que vêm na mensagem. Nunca repete uma frase.
- Nunca use travessão (o traço comprido); use vírgula ou ponto.
- Nunca prometa dinheiro, nunca dê recomendação de investimento, nunca diga que o FinMoovi é grátis (ele tem 7 dias de teste).
- Não mencione o FinMoovi, a não ser na ação "link". Na ação "link", escreva você mesmo, com palavras novas a cada vez, que o link está no primeiro comentário fixado e na descrição (sem escrever o link).
- Se perguntarem a sério se quem responde é robô ou IA, use a ação "humano": o dono do canal responde.

Se o comentário pedir um tema de vídeo novo ("faz um sobre X"), preencha "tema" com o tema curto. Marque "destaque" true se o comentário for muito bom (história forte, engraçado, gera conversa)."""
ESQUEMA = {"type": "object", "properties": {"itens": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"}, "acao": {"type": "string", "enum": ["responder", "link", "spam", "humano", "ignorar"]},
    "resposta": {"type": "string"}, "tema": {"type": "string"}, "destaque": {"type": "boolean"}},
    "required": ["id", "acao", "resposta", "tema", "destaque"], "additionalProperties": False}}},
    "required": ["itens"], "additionalProperties": False}
def decidir(video, lote, recentes=()):
    import anthropic
    cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"])
    rec = ("Respostas recentes do Tião (não repita o começo nem as frases):\n" + "\n".join(f"- {r}" for r in recentes[-25:]) + "\n\n") if recentes else ""
    txt = rec + (f"Vídeo: {video['titulo']}\nSobre o vídeo: {video['desc']}\n\nComentários (responda todos, mesmo id):\n"
           + "\n".join(json.dumps({"id": c["id"], "autor": c["autor"], "texto": c["texto"][:800]}, ensure_ascii=False) for c in lote))
    r = cli.messages.create(model=MODELO, max_tokens=4000, system=SISTEMA, messages=[{"role": "user", "content": txt}],
                            output_config={"format": {"type": "json_schema", "schema": ESQUEMA}})
    custo = r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6
    itens = json.loads(next(b.text for b in r.content if b.type == "text"))["itens"]
    for i in itens: i["resposta"] = re.sub(r"\s*[—–]\s*", ", ", i["resposta"]).strip()  # sem travessao, nunca
    return itens, custo

LINK_RESP = ["Tá no primeiro comentário aqui em cima e na descrição! Tem 7 dias de teste pra você ver se combina com você 🙌",
             "Opa! O link tá fixado ali em cima e na descrição. Dá pra testar 7 dias antes de decidir.",
             "Coloquei lá no primeiro comentário e na descrição. Testa os 7 dias com calma e me conta!"]

def main():
    hora = datetime.datetime.now(datetime.timezone.utc)
    log(f"\n💬 Comentários do Tião{' (ENSAIO: não escreve nada)' if ENSAIO else ''} · {hora:%d/%m %H:%M} UTC")
    cad = ler_caderno(); eu, uploads = canal(); vs = videos_publicos(uploads)
    log(f"🎬 vídeos públicos: {len(vs)} · já vistos: {len(cad['vistos'])}")
    feitas, custo_total, pendentes = 0, 0.0, []
    for v in vs:
        idade = (hora - datetime.datetime.fromisoformat(v["quando"].replace("Z", "+00:00"))).total_seconds() / 3600
        if idade > QUENTE_H and hora.hour % 6 != 0 and "--todos" not in sys.argv: continue
        th = conversas(v["id"]); nn = numero_do_video(v)
        # 1) o primeiro comentario do canal
        if not any(t["snippet"]["topLevelComment"]["snippet"].get("authorChannelId", {}).get("value") == eu for t in th) and not cad["primeiro"].get(v["id"]):
            t = primeiro_texto(nn); log(f"   📌 {v['titulo'][:50]}: sem o nosso primeiro comentário" + ("" if not ENSAIO else f"\n{t}"))
            if not ENSAIO:
                try: escrever_conversa(v["id"], t); cad["primeiro"][v["id"]] = hora.isoformat()
                except Exception as e: log("      não consegui comentar (falta a permissão force-ssl? rodar youtube/autorizar.py):", e)
        # 2) os comentarios novos de outras pessoas, que ainda nao tem resposta nossa
        for t in th:
            c = t["snippet"]["topLevelComment"]; s = c["snippet"]
            if s.get("authorChannelId", {}).get("value") == eu or c["id"] in cad["vistos"]: continue
            if any(r["snippet"].get("authorChannelId", {}).get("value") == eu for r in t.get("replies", {}).get("comments", [])):
                cad["vistos"][c["id"]] = "ja-respondido"; continue
            idade_c = (hora - datetime.datetime.fromisoformat(s["publishedAt"].replace("Z", "+00:00"))).total_seconds() / 60
            if idade_c < 15 + (int(c["id"].encode().hex()[-4:], 16) % 76) and "--todos" not in sys.argv: continue  # gente nao responde no mesmo minuto
            pendentes.append((v, {"id": c["id"], "autor": s.get("authorDisplayName", ""), "texto": s.get("textOriginal", "")}))
    log(f"📝 comentários novos: {len(pendentes)}")
    porvideo = {}
    for v, c in pendentes: porvideo.setdefault(v["id"], (v, []))[1].append(c)
    for vid, (v, lote) in porvideo.items():
        lote = lote[: max(0, MAX - feitas) + 10]
        if not lote: break
        itens, custo = decidir(v, lote, cad.get("recentes", [])); custo_total += custo
        textos = {c["id"]: c for c in lote}
        for i in itens:
            c = textos.get(i["id"])
            if not c: continue
            if i["tema"]: cad["para_resumo"].append({"tipo": "tema", "texto": i["tema"], "video": v["titulo"]})
            if i["destaque"]:
                d = {"tipo": "destaque", "texto": c["texto"][:300], "autor": c["autor"], "video": v["titulo"]}
                cad["para_resumo"].append(d); cad.setdefault("semana", []).append(d)  # o robo dos posts usa o melhor da semana
            if i["acao"] in ("responder", "link"):
                if feitas >= MAX: continue   # fica para a proxima rodada (nao marca como visto)
                resp = i["resposta"] or random.choice(LINK_RESP)
                log(f"   💬 {c['autor']}: {c['texto'][:90]!r}\n      ↳ Tião: {resp}")
                if not ENSAIO:
                    try: responder(c["id"], resp); time.sleep(random.randint(45, 150))  # ritmo de gente, nao de maquina
                    except Exception as e: log("      não consegui responder:", e); continue  # fica para a proxima rodada
                feitas += 1; cad["recentes"] = (cad.get("recentes", []) + [resp])[-40:]
            elif i["acao"] == "spam":
                log(f"   🚫 spam (vai para revisão): {c['autor']}: {c['texto'][:90]!r}")
                if not ENSAIO:
                    try: segurar(c["id"])
                    except Exception as e: log("      não consegui segurar:", e)
            elif i["acao"] == "humano":
                log(f"   🙋 para o Ed: {c['autor']}: {c['texto'][:90]!r}")
                cad["para_resumo"].append({"tipo": "humano", "texto": c["texto"][:300], "autor": c["autor"], "video": v["titulo"],
                                           "link": f"https://www.youtube.com/watch?v={v['id']}&lc={c['id']}"})
            else: log(f"   · ignorado: {c['texto'][:60]!r}")
            cad["vistos"][c["id"]] = i["acao"]
    sobra = sum(1 for _, c in pendentes if c["id"] not in cad["vistos"])
    log(f"\n✅ respostas: {feitas} · custo do Claude nesta rodada: US$ {custo_total:.4f}" + (f" · ficam para a próxima: {sobra}" if sobra else ""))
    # 3) o resumo do dia no Apexi Team (uma vez por dia, so se tiver algo)
    hoje = hora.strftime("%Y-%m-%d")
    if cad["para_resumo"] and cad.get("ultimo_resumo") != hoje and hora.hour >= 11 and not ENSAIO:
        try: resumo(cad["para_resumo"], hoje); cad["para_resumo"], cad["ultimo_resumo"] = [], hoje
        except Exception as e: log("resumo no Team falhou:", e)
    if not ENSAIO: gravar_caderno(cad)

def resumo(itens, hoje):
    from fabrica import team
    h = [i for i in itens if i["tipo"] == "humano"]; d = [i for i in itens if i["tipo"] == "destaque"][:3]; t = [i for i in itens if i["tipo"] == "tema"]
    passos = [{"codigo": f"H{k + 1:02d}", "texto": f"Responder você: {i['autor']} em «{i['video'][:40]}»: {i['texto'][:200]}", "copiar": "", "links": [{"rotulo": "Abrir o comentário", "url": i["link"]}], "ficheiro": ""} for k, i in enumerate(h)]
    desc = ("Os melhores: " + " | ".join(f"{i['autor']}: {i['texto'][:120]}" for i in d) if d else "") + \
           ("\nPedidos de tema: " + "; ".join(sorted({i["texto"] for i in t})) if t else "")
    team.mandar({"chave_unica": f"tiao-comentarios-{hoje}", "tipo": "comentarios-do-dia", "projeto": "Tião Poupador",
                 "titulo": f"Comentários do dia {hoje[8:]}/{hoje[5:7]}: {len(h)} para você", "descricao": desc or "Nada que precise de você.", "passos": passos})
    log("📋 resumo do dia no Team")

if __name__ == "__main__":
    main()
