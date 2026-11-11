# Peca do robo: ESCOLHE OS TEMAS sozinho (regra do Ed, 06/11/2026: «eu nao vou decidir novos temas nao»).
#   1. olha os canais vigiados (os mesmos do pesquisa/vigiar.py), so videos longos;
#   2. candidatos: os fora da curva (5x+ a mediana do canal) de 21 a 120 dias; depois os mais vistos de sempre (21+ dias);
#   3. reveza os canais (o proximo modelo vem de um canal diferente do ultimo) e nunca repete um modelo ja usado;
#   4. o Claude escolhe o melhor para o Tiao e MODELA E MELHORA: titulo nosso (nunca copiado), angulo da historia;
#   5. preenche o calendario (domingo 17h, quarta 18h) ate ter VAGAS_A_FRENTE videos marcados, e avisa o Ed (so aviso).
# Uso: python fabrica/temas.py [--ensaio]
import datetime, json, os, re, sys, urllib.parse
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import api, chaves
from fabrica import agenda
from fabrica.regras_titulo import REGRAS, revisar
ENSAIO = "--ensaio" in sys.argv
CANAIS = ["@tucoinveste", "@obastidordodinheiro", "@dinheirodescomplicadooficial", "@eduinvesteoficial", "@povinvestimento", "@darkledger13", "@CanalInvestidorSincero", "@ProsaqueRende"]
MIN_VIEWS, DIAS_MIN_COPIA, DIAS_MAX_COPIA, VAGAS_A_FRENTE = 20000, 21, 120, 4
Y = "https://www.googleapis.com/youtube/v3/"
log = lambda *m: print(*m, flush=True)
ELENCO = json.load(open(P + "/fabrica/elenco.json", encoding="utf-8"))  # a turma do bairro (Ed, 07/11)

def videos_do_canal(h):
    c = api(Y + "channels?part=snippet,contentDetails&forHandle=" + urllib.parse.quote(h))["items"][0]
    up = c["contentDetails"]["relatedPlaylists"]["uploads"]; ids, tk = [], ""
    while len(ids) < 150:
        r = api(Y + f"playlistItems?part=contentDetails&maxResults=50&playlistId={up}" + (f"&pageToken={tk}" if tk else ""))
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]; tk = r.get("nextPageToken")
        if not tk: break
    hoje = datetime.datetime.now(datetime.timezone.utc); out = []
    for i in range(0, len(ids), 50):
        for v in api(Y + "videos?part=snippet,statistics,contentDetails&id=" + ",".join(ids[i:i + 50]))["items"]:
            m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"]["duration"])
            if not m or int(m[1] or 0) * 3600 + int(m[2] or 0) * 60 + int(m[3] or 0) < 240: continue  # so longos (4 min ou mais)
            dias = max(1, (hoje - datetime.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))).days)
            vw = int(v["statistics"].get("viewCount", 0))
            out.append({"id": v["id"], "titulo": v["snippet"]["title"], "canal": h, "views": vw, "dias": dias, "por_dia": vw // dias,
                        "desc": v["snippet"].get("description", "")[:300]})
    return out

def proximas_vagas(cal, n):
    """as proximas datas livres (domingo 17h, quarta 18h) depois do ultimo video marcado"""
    ult = max((datetime.datetime.fromisoformat(c["quando"]) for c in cal), default=datetime.datetime.now())
    d, out = ult, []
    while len(out) < n:
        d += datetime.timedelta(days=1)
        if d.weekday() == 6: out.append(d.replace(hour=17, minute=0))
        elif d.weekday() == 2: out.append(d.replace(hour=18, minute=0))
    return out

ESQ = {"type": "object", "properties": {"escolhas": {"type": "array", "items": {"type": "object", "properties": {
    "modelo_id": {"type": "string"}, "familia": {"type": "string"}, "o_que_esconde": {"type": "string"}, "titulo": {"type": "string"}, "capa_texto": {"type": "string"}, "capa_cena": {"type": "string"}, "angulo": {"type": "string"}, "elenco": {"type": "array", "items": {"type": "string"}}, "por_que": {"type": "string"}},
    "required": ["modelo_id", "familia", "o_que_esconde", "titulo", "capa_texto", "capa_cena", "angulo", "elenco", "por_que"], "additionalProperties": False}}},
    "required": ["escolhas"], "additionalProperties": False}

def escolher(pools, seq, ja, n, ultimo_canal, historico=""):
    import anthropic
    cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"])
    txt = f"""Você escolhe os temas do canal de YouTube "Tião Poupador": vídeos longos (20 a 25 min) em desenho 2D, finanças pessoais para famílias brasileiras de classe média e baixa, contados como HISTÓRIA do Tião (um brasileiro simples que cuida do dinheiro com caderno, lista e a caneca velha) e da turma do bairro dele.

A turma do bairro (escolha quem combina com cada tema):
""" + chr(10).join(f"- {p['nome']} ({p['idade']}): {p['papel']} Temas: {', '.join(p['temas'])}." for p in ELENCO["personagens"]) + """
Regras do elenco:
""" + chr(10).join("- " + r for r in ELENCO["regras"]) + f"""
Elenco dos últimos vídeos (para revezar): {historico or '(nenhum)'}. O app FinMoovi entra só no fim.

Já temos (não repetir o assunto):
{chr(10).join('- ' + t for t in ja)}

Candidatos de dois tipos (vídeos que deram muitas views nos canais que vigiamos):
""" + "\n\n".join(f"═══ {k.upper()} ({'fora da curva (5x+ a média do canal) com 3 semanas a 4 meses: a hora certa de refazer, ordenados por vezes a média' if k == 'recente' else 'os mais vistos de sempre desses canais'}) ═══\n" + "\n".join(json.dumps({x: c[x] for x in ('id', 'titulo', 'canal', 'views', 'dias', 'por_dia', 'vezes_a_media')}, ensure_ascii=False) for c in pools[k]) for k in pools if pools[k]) + f"""

Escolha {n} temas, UM POR VAGA, nesta ordem de tipos (é obrigatório: a escolha da vaga 1 vem da lista do tipo 1, e assim por diante): {", ".join(f"vaga {i + 1} = {t.upper()}" for i, t in enumerate(seq))}.
MODELE E MELHORE cada um para o Tião:
- dentro de cada lista, prefira os que mais views fazem; reveze os canais (o primeiro NÃO pode ser do canal {ultimo_canal or '(nenhum)'}, e não use dois do mesmo canal seguidos);
- só temas de dinheiro do dia a dia (gasto, dívida, cartão, compra, golpe, salário, aposentadoria, hábito). NÃO: cripto, ação específica, política, notícia que envelhece;
- "familia": qual das famílias de título abaixo você usou (de preferência a mesma do modelo);
- "o_que_esconde": em 1 frase, a resposta que o vídeo revela e que o título NÃO pode contar;
- PREFIRA o modelo com mais "vezes_a_media"; um campeão em INGLÊS que ainda não tem versão brasileira nesses canais vale ouro (o "How Banks Treat You at Every Level" fez 1,18 mi e ninguém refez em português). Evite tema que um canal brasileiro já refez nas últimas 3 semanas;
- "titulo": NOSSO, nunca a frase do modelo, até 60 caracteres, sem travessão. Escreva 5 na cabeça e fique com o que deixa a pergunta mais forte;
- "capa_texto": 2 a 4 palavras da capa que completam o título sem repetir (veredito, provocação ou pergunta com número);
- "capa_cena": 1 frase com a cena da capa (quem aparece, com que emoção, a seta, as etiquetas com números), sem mostrar o final;

""" + REGRAS + """

- "angulo": 1 ou 2 frases com a história que o vídeo vai contar (o Tião e os protagonistas escolhidos), com um número concreto em reais;
- "elenco": os nomes de quem entra (sempre "Tião"; 1 ou 2 protagonistas do problema; e "Valéria" quando ela fizer a participação de novela). Reveze: nada de repetir os mesmos protagonistas dos últimos 2 vídeos;
- "por_que": 1 frase com o motivo (ex.: "92 mil views em 12 dias no Tuco")."""
    r = cli.messages.create(model="claude-sonnet-5-5", max_tokens=3000, messages=[{"role": "user", "content": txt}],
                            output_config={"format": {"type": "json_schema", "schema": ESQ}})
    custo = r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6
    esc = json.loads(next(b.text for b in r.content if b.type == "text"))["escolhas"]
    for e in esc: e["modelo"] = next((c["titulo"] for k in pools for c in pools[k] if c["id"] == e["modelo_id"]), "")
    esc, c2, notas = revisar(cli, esc)  # o diretor chato: nota de 1 a 10, reescreve o que nao passar de 8
    for i, e in enumerate(esc): e["notas"] = notas.get(i, {})
    return esc, custo + c2

def main():
    a = agenda.ler(); cal = a.setdefault("calendario", []); usados = a.setdefault("modelos_usados", [])
    agora = datetime.datetime.now()
    futuros = [c for c in cal if datetime.datetime.fromisoformat(c["quando"]) > agora]
    falta = VAGAS_A_FRENTE - len(futuros)
    log(f"📅 vídeos marcados à frente: {len(futuros)} · faltam {max(0, falta)} temas")
    if falta <= 0 and "--forcar" not in sys.argv: return
    falta = max(falta, 1)
    todos = []
    for h in CANAIS:
        try: todos += videos_do_canal(h)
        except Exception as e: log("canal", h, "falhou:", e)
    novos = [v for v in todos if v["id"] not in {u["id"] for u in usados}]
    # Ed, 06/11: MESCLAR os que estao subindo agora (30 dias, 20 mil+) com os mais vistos de sempre, alternando
    # Ed, 07/11 («copie esses videos que dao bom»): o estudo dos 20 campeoes mostrou que a copia do TEMA funciona
    # quando o original tem 3 semanas a 4 meses (Tuco 555 mil, POV 504 mil, Edu 499 mil) e falha quando e feita poucos
    # dias depois (Edu 305 e 193 views). Candidato = "fora da curva": 5x ou mais a mediana do proprio canal.
    med = {}
    for h in CANAIS:
        vs = sorted(v["views"] for v in todos if v["canal"] == h)
        if vs: med[h] = max(1, vs[len(vs) // 2])
    for v in novos: v["vezes_a_media"] = round(v["views"] / med.get(v["canal"], 1), 1)
    fora = [v for v in novos if v["vezes_a_media"] >= 5 and v["views"] >= MIN_VIEWS]
    rec = sorted([v for v in fora if DIAS_MIN_COPIA <= v["dias"] <= DIAS_MAX_COPIA], key=lambda v: -v["vezes_a_media"])[:15]
    ger = sorted([v for v in fora if v not in rec and v["dias"] >= DIAS_MIN_COPIA], key=lambda v: -v["views"])[:15]
    pools = {"recente": rec, "geral": ger}
    prox = "geral" if a.get("ultima_fonte") == "recente" else "recente"
    seq = []
    for _ in range(falta):
        seq.append(prox if pools[prox] else ("geral" if prox == "recente" else "recente")); prox = "geral" if seq[-1] == "recente" else "recente"
    cands = rec + ger
    log(f"🔎 {len(todos)} vídeos longos vistos · recentes 20 mil+: {len(rec)} · mais vistos de sempre: {len(ger)} · ordem: {seq}")
    ultimo = usados[-1]["canal"] if usados else None
    escolhas, custo = escolher(pools, seq, [c["titulo"] for c in cal], falta, ultimo, "; ".join(f"{c['nn']}: {', '.join(c['elenco'])}" for c in cal[-4:] if c.get("elenco")))
    porid = {c["id"]: c for c in cands}; vagas = proximas_vagas(cal, falta); nn = max(int(c["nn"]) for c in cal) if cal else 1
    msg = []
    for e, quando, fonte in zip(escolhas, vagas, seq):
        m = porid.get(e["modelo_id"])
        if not m: continue
        a["ultima_fonte"] = fonte
        nn += 1; tit = re.sub(r"\s*[—–]\s*", ", ", e["titulo"])
        cal.append({"nn": f"{nn:02d}", "quando": quando.strftime("%Y-%m-%d %H:%M"), "titulo": tit, "angulo": e["angulo"], "elenco": e["elenco"], "esconde": e["o_que_esconde"],
                    "capa": {"texto": e["capa_texto"], "cena": e["capa_cena"]}, "familia": e["familia"],
                    "fonte": fonte, "modelo": {"id": m["id"], "titulo": m["titulo"], "canal": m["canal"], "views": m["views"], "dias": m["dias"]}})
        usados.append({"id": m["id"], "canal": m["canal"]})
        vw = f"{m['views']:,}".replace(",", ".")
        msg.append(f"- **Vídeo {nn:02d} · {quando:%d/%m %Hh}** · {tit}\n  Modelo ({'subindo agora' if fonte == 'recente' else 'dos mais vistos de sempre'}): «{m['titulo']}» ({m['canal']}, {vw} views em {m['dias']} dias) https://youtu.be/{m['id']}\n  Capa: «{e['capa_texto']}» ({e['capa_cena']})\n  Família do título: {e['familia']} · diretor: {(('reescreveu (a versão anterior tinha ' + str(min(v for k, v in e['notas'].items() if k in ('misterio', 'emocao', 'vida_da_pessoa', 'clareza', 'longe_do_modelo'))) + '/10: ' + e['notas']['problema'] + ')') if e['notas'].get('reescrito') else ('aprovou, nota mínima ' + str(min(v for k, v in e['notas'].items() if k in ('misterio', 'emocao', 'vida_da_pessoa', 'clareza', 'longe_do_modelo'))) + '/10')) if e['notas'] else '?'}\n  Quem entra: {', '.join(e['elenco'])}\n  História: {e['angulo']}\n  Por quê: {e['por_que']}")
    log("\n".join(msg) + f"\n💲 custo do Claude: US$ {custo:.3f}")
    if ENSAIO or not msg: return
    agenda.gravar(a)
    from fabrica import correio
    correio.enviar("Tião Poupador · temas novos escolhidos pelo robô", "# Temas novos (só aviso, não precisa fazer nada)\n\nEscolhidos pelo que mais deu views nos canais que vigiamos.\n\n" + "\n".join(msg))

if __name__ == "__main__":
    main()
