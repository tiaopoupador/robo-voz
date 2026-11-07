# Peca do robo: as FICHAS dos personagens do bairro (fabrica/elenco.json), que o Ed gera no meta.ai.
# A ficha e a referencia oficial de cada um (varias poses e expressoes), como a do Tiao.
#   python fabrica/fichas.py            -> mostra os pedidos (fabrica/saida/fichas-pedidos.md)
#   python fabrica/fichas.py --enviar   -> manda a tarefa ao Apexi Team (uma vez) e o e-mail de reserva
#   python fabrica/fichas.py --baixar   -> traz as fichas (Team ou Drive > referencia) para banco/referencia
#                                          (depois: bash fabrica/para-nuvem.sh, que refaz o cofre da nuvem)
import json, os, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
EL = json.load(open(P + "/fabrica/elenco.json", encoding="utf-8"))["personagens"]
NOVOS = [p for p in EL if p.get("ficha") and p["id"] != "tiao"]
CHAVE = "tiao-elenco-fichas"
REFD = P + "/banco/referencia"

PEDIDO = ("Using the attached image ONLY as a STYLE reference (same flat 2D cartoon drawing style, same thin black outlines, same soft cel shading, "
          "same warm slightly desaturated colors, same proportions style and same sheet layout), create the OFFICIAL CHARACTER SHEET of a NEW character "
          "(NOT the man in the reference, a different person): {visual} "
          "The sheet, on a plain light background: a full-body turnaround (front, three-quarter, side profile and back), "
          "6 facial expressions in close-up ({expr}), and 4 action poses ({poses}). "
          "The character is IDENTICAL in every drawing: same face, hair, skin tone, body shape, clothes, colors and accessories. "
          "Correct anatomy: two symmetrical eyes, five fingers on each hand. ASPECT RATIO 16:9, horizontal. "
          "No text, no letters, no names, no labels, no logos, no brand names, no watermark.\n"
          "Generate 4 different versions so I can pick the best one.")
JEITO = {
 "valeria": ("bored and snobbish, disgusted, fake polite smile, secretly smiling with a blush, surprised, angry",
             "walking while filming a selfie video, holding the handbag with her nose up, looking over her sunglasses with disdain, peeking secretly from behind a curtain"),
 "cida":    ("warm smile, worried, suspicious looking over her glasses, shocked, laughing, teaching with a raised finger",
             "leaning on the window sill, holding an old phone far from her eyes, counting coins from the purse, sweeping the sidewalk"),
 "jessica": ("excited, anxious, shocked looking at the phone, crying, embarrassed, proud",
             "scrolling the phone on the sofa, celebrating with arms up, walking with earbuds, holding a paycheck"),
 "rafa":    ("big laugh, cocky, worried, shocked, sad, thinking",
             "driving with one hand on the wheel, leaning on his car, showing the phone with a ride app, throwing money in the air"),
 "lourival": ("friendly smile, tired, worried doing math, angry, surprised, laughing",
              "behind the counter writing in a notebook, carrying a box of groceries, wiping the counter, scratching his bald head"),
 "patricia": ("calm smile, tired after a shift, focused doing math, proud, worried, laughing",
              "writing a budget in a notebook at the kitchen table, walking with the tote bag, hugging her 8 year old son, pushing a shopping cart"),
}

def links():
    pasta, ficha_tiao = "Google Drive > Tiao Poupador > referencia", ""
    try:
        from fabrica import drive
        ref = drive.achar("referencia", drive.achar("Tiao Poupador"))
        pasta = f"https://drive.google.com/drive/folders/{ref}"
        ficha_tiao = next((f"https://drive.google.com/file/d/{f['id']}/view" for f in drive.listar(ref) if f["name"] == "tiao-ficha-oficial.jpg"), pasta)
    except Exception as e: print("sem Drive agora:", e)
    return pasta, ficha_tiao

def montar():
    pasta, ft = links(); passos = []
    o = ["# Tião Poupador · as fichas dos personagens novos do bairro", "",
         "A ficha é a foto oficial de cada personagem, como a do Tião: ele em várias poses e caras. Gera-se **uma vez só**. Depois disso, o robô usa a ficha sozinho em todas as imagens.", "",
         "**Como fazer:** no meta.ai, formato **16:9**. Anexe a ficha do Tião (só para copiar o jeito do desenho), cole o texto da caixa cinza, gere e salve **a melhor das 4** com o nome indicado.",
         "Se algum não ficar bom, gere de novo: o rosto que você escolher é o rosto que vai valer para sempre.", "",
         f"📁 **Salvar na pasta:** {pasta}", ""]
    for i, p in enumerate(NOVOS, 1):
        ex, po = JEITO[p["id"]]; txt = PEDIDO.format(visual=p["visual"], expr=ex, poses=po)
        o += [f"### P{i:02d} · {p['nome']}, {p['idade']} anos", "", f"_{p['papel']}_", "",
              f"📁 **Salvar na pasta:** {pasta}", "", "📄 **Nome do arquivo** (toque 3 vezes no nome para selecionar e copiar):", f"=> {p['ficha']}", "",
              "📎 **Anexar** (clique para abrir e baixar):", f"- tiao-ficha-oficial.jpg (só o estilo do desenho): {ft}", "", "```", txt, "```", ""]
        passos.append({"codigo": f"P{i:02d}", "texto": f"Ficha de {p['nome']} ({p['idade']} anos): salve a melhor das 4", "copiar": txt,
                       "links": [{"rotulo": "Anexar: tiao-ficha-oficial.jpg (só o estilo)", "url": ft}], "ficheiro": p["ficha"]})
    os.makedirs(P + "/fabrica/saida", exist_ok=True)
    open(P + "/fabrica/saida/fichas-pedidos.md", "w", encoding="utf-8").write("\n".join(o))
    return o, passos, pasta

def enviar():
    from fabrica import team, correio
    o, passos, pasta = montar(); ok = ja = False
    try:
        ja = team._pedir(f"/tarefas/{CHAVE}") is not None
        print("Team: a tarefa já existe, não mando de novo")
    except Exception as e:
        if getattr(e, "code", 0) != 404: print("Team:", e)
    if not ja:
        try:
            r = team.mandar({"chave_unica": CHAVE, "tipo": "fichas-de-personagem", "projeto": "Tião Poupador",
                             "titulo": f"As fichas dos {len(passos)} personagens novos do bairro (uma vez só)",
                             "descricao": "No meta.ai, 16:9. Anexe a ficha do Tião só para o estilo, gere, e anexe aqui a melhor das 4 de cada personagem (ou salve na pasta referencia do Drive).",
                             "prazo": "2026-11-10T20:00:00-03:00", "links": [{"rotulo": "Pasta referencia no Drive", "url": pasta}], "passos": passos})
            ok = True; print("Team:", r.get("url", "ok"))
        except Exception as e: print("Team recusou (vai só o e-mail):", e)
        correio.enviar("Tião Poupador · as fichas dos personagens novos", "\n".join(o)); print("e-mail enviado")

def baixar():
    from fabrica import team, drive
    n = 0
    try:
        for a in team._pedir(f"/tarefas/{CHAVE}").get("anexos", []):
            p = next((x for x in NOVOS if a.get("codigo") == f"P{NOVOS.index(x) + 1:02d}"), None)
            if p and not os.path.exists(f"{REFD}/{p['ficha']}"):
                open(f"{REFD}/{p['ficha']}", "wb").write(team._pedir(f"/anexos/{a['id']}", bruto=True)); n += 1; print("Team:", p["ficha"])
    except Exception as e: print("Team:", e)
    ref = drive.achar("referencia", drive.achar("Tiao Poupador")); nomes = {p["ficha"] for p in NOVOS}
    for f in drive.listar(ref):
        if f["name"] in nomes and not os.path.exists(f"{REFD}/{f['name']}"):
            from fabrica.google import api
            open(f"{REFD}/{f['name']}", "wb").write(api(f"https://www.googleapis.com/drive/v3/files/{f['id']}?alt=media", bruto=True)); n += 1; print("Drive:", f["name"])
    falta = [p["nome"] for p in NOVOS if not os.path.exists(f"{REFD}/{p['ficha']}")]
    print(f"{n} fichas novas · faltam: {', '.join(falta) or 'nenhuma'}")

if __name__ == "__main__":
    if "--enviar" in sys.argv: enviar()
    elif "--baixar" in sys.argv: baixar()
    else: montar(); print(open(P + "/fabrica/saida/fichas-pedidos.md", encoding="utf-8").read()[:1500])
