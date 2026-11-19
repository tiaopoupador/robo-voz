# Peca do robo: monta o e-mail com os pedidos que o Ed gera a mao (meta.ai: as imagens principais; Flow: os clipes; a capa).
# Uso: python fabrica/pedidos.py 02 ["pasta onde salvar"] [--enviar] [--matheus]   -> fabrica/saida/02-pedidos.md (o e-mail.py manda este texto)
import importlib, os, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
_ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]  # as opcoes (--enviar, --matheus) nao contam como pasta
NN = _ARGS[0]; ONDE = _ARGS[1] if len(_ARGS) > 1 else f"Google Drive > Tiao Poupador > entrada > video-{NN}"
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
FIM4 = "Gere UMA imagem só, com total consistência com o personagem que está em referência."
FIM_DUAS = "Gere as 2 imagens e depois o GIF lento, com total consistência com o personagem que está em referência."
CONS = ("CHARACTER AND SCENERY CONSISTENCY ARE THE TOP PRIORITY. The characters must be IDENTICAL to the attached reference images, not similar: "
        "same face shape, eyes, eyebrows, nose, mouth, mustache, hairstyle, hair color, skin tone, body shape, height, age, clothes, clothing colors and accessories. "
        "Do not redesign, restyle, beautify, age, slim down or reinterpret them. A similar-looking character is NOT acceptable: match the attached images as closely as possible, in the exact same drawing style. "
        "Correct anatomy: exactly five fingers on each hand, two normal symmetrical eyes, no extra limbs, no faces inside objects. Pose and expression follow the scene, NOT the reference pose. ")
STYLE = "Flat 2D cartoon illustration, clean thin black outlines, soft cel shading, warm slightly desaturated colors, modern explainer animation style, 16:9 widescreen, Brazilian setting. "
QUEM = {
 "tiao": "One of the attached images is Tiao's character sheet (many angles and poses): use it only to know him from every side, draw him ONCE, in a natural pose that fits the action, never stiff facing the camera. Tiao: about 30 years old, SHORT and slightly CHUBBY, ROUND face, short messy black hair, a small THIN black pencil mustache (always present, never thick), light brown skin, mustard-yellow polo shirt, faded denim shorts, black flip-flops, black wristwatch, a short yellow carpenter pencil in the shirt pocket. ",
 "sandra": "Sandra: woman in her late 30s, long wavy brown hair, sunglasses pushed up on her head, gold hoop earrings, red blouse, blue jeans, brown handbag. ",
 "marcos": "Marcos: TALL slim man in his late 30s, gelled dark hair, light skin, white shirt with rolled sleeves, dark jeans, brown belt, big silver watch, clean-shaven (NO mustache). ",
}
import json  # o resto do elenco do bairro (fabrica/elenco.json, Ed 07/11): a referencia e a ficha (varias poses) de cada um
for _p in json.load(open(P + "/fabrica/elenco.json", encoding="utf-8"))["personagens"]:
    QUEM.setdefault(_p["id"], f"The attached {_p['ref']} is {_p['id'].capitalize()}'s character sheet: use it only to know the character, draw this person ONCE in a natural pose. " + _p["visual"] + " ")
NEG = " No text, no letters, no numbers, no readable writing, no logos, no brand names, no watermark."
def quem(refs): return "".join(v for k, v in QUEM.items() if k in refs)
# Ed, 10/11/2026: «tire as 4 cenas, vamos deixar apenas 2» (menos tempo no meta.ai)
# Ed, 19/11/2026 (mais tarde, mudou de ideia): «para cada pedido de imagem, vc deve colocar no prompt q deseja 2 versoes
# diferentes dessa imagem, ou seja, gerar duas imagens diferentes, mas que se complementam. E depois com essas duas imagens
# gerar um GIF lento entre as duas de 4 a 5 segundos!». Um prompt so por cena; dele saem a imagem 1, a 2 e o GIF.
DUAS = ("GENERATE 2 DIFFERENT IMAGES of this same scene that COMPLEMENT each other, like two moments of the same shot: "
        "image 1 = medium-wide view showing the place and the whole action; image 2 = closer view of the main detail (faces, hands and what they hold), "
        "a moment right after image 1. Same characters, same clothes, same place, same light in both. Each image 16:9. ")
GIF_LENTO = ("Then, with these 2 images, create a SLOW animated GIF of 4 to 5 seconds that goes smoothly from image 1 to image 2 "
             "(gentle crossfade and slow camera movement, no fast cuts), 16:9.")
UMA = "ONE single image, 16:9. "
R169 = "ASPECT RATIO 16:9, horizontal widescreen (1920x1080), never square, never vertical. "
SOM = " SILENT VIDEO: no sound, no audio, no music, no sound effects, no voices, no dialogue, no speech, no subtitles."
meta = [n for n, v in C.IMG.items() if v[0] == "meta"]; flow = [n for n, v in C.IMG.items() if v[0] == "flow"]
# os links do Drive: a pasta onde o Ed salva e cada foto de referencia (para abrir com um clique)
PASTA, REFS, PASTA_REF = ONDE, {}, ""
try:
    from fabrica import drive
    raiz = drive.achar("Tiao Poupador"); ref = drive.achar("referencia", raiz); ent = drive.achar("entrada", raiz)
    v = drive.achar(f"video-{NN}", ent) or drive.pasta(f"video-{NN}", ent)
    PASTA = f"https://drive.google.com/drive/folders/{v}"; PASTA_REF = f"https://drive.google.com/drive/folders/{ref}"
    REFS = {f["name"]: f"https://drive.google.com/file/d/{f['id']}/view" for f in drive.listar(ref)}
except Exception as e:
    print("sem Drive agora (links simples):", e)
def com_ficha(refs):  # com o Tiao vai so a ficha oficial (Ed, 19/11)
    if "nenhuma" in refs or not refs.strip(): return "nenhuma"  # Ed 19/11: Tiao e Marcos vao sempre com as DUAS referencias (team.REFERENCIAS)
    from fabrica.team import completar_refs
    return " + ".join(completar_refs([x.strip() for x in refs.split("+")]))
def anexar(refs):
    refs = com_ficha(refs)
    if "nenhuma" in refs: return ["📎 **Anexar:** Não é preciso anexar imagem de referência nenhuma!"]
    return ["📎 **Anexar** (clique para abrir e baixar):"] + [f"- {r}: {REFS.get(r, PASTA_REF)}" for r in [x.strip() for x in refs.split("+")]]
PASSOS = []  # os mesmos pedidos, um passo por arquivo, para a tarefa do Apexi Team
def bloco(cod, titulo, refs, nomes, prompt):
    refs = com_ficha(refs)
    lr = [] if "nenhuma" in refs else [{"rotulo": "Anexar junto ao Prompt - " + r, "url": REFS.get(r, PASTA_REF)} for r in [x.strip() for x in refs.split("+")] if REFS.get(r, PASTA_REF)]
    pasta = {"rotulo": f"Google Drive > Tiao Poupador > entrada > video-{NN}", "url": PASTA}
    if len(nomes) > 1:  # Ed, 19/11: «um prompt por imagem (...) 2 imagens e mais um gif (...) 3 botoes: imagem 1, imagem 2 e gif»
        rot = lambda k, nm: "Nome do GIF" if nm.endswith(".gif") else f"Nome da imagem {k + 1}"
        PASSOS.append({"codigo": cod, "texto": f"{cod} · {titulo}", "links": lr, "formato": "16:9", "tipo": "imagem", "onde": "meta.ai",
                       "o_que": f"{titulo} (2 imagens + GIF lento)", "pasta": pasta, "varios": True,
                       "copias": [{"rotulo": "Prompt", "texto": prompt}] + [{"rotulo": rot(k, nm), "texto": nm} for k, nm in enumerate(nomes)]})
    for nm in (nomes if len(nomes) == 1 else []):
        PASSOS.append({"codigo": nm.split("_")[0], "texto": f"{cod} · {titulo}", "copiar": prompt, "links": lr, "ficheiro": nm, "formato": "16:9",
                       "tipo": "video" if nm.endswith(".mp4") else "imagem", "onde": "Flow" if nm.endswith(".mp4") else "meta.ai",
                       "o_que": titulo, "pasta": pasta})
    return [f"### {cod} · {titulo}", "", f"📁 **Salvar na pasta:** {PASTA}", "",
            "📄 **Nome do arquivo** (toque 3 vezes no nome para selecionar e copiar):"] + [f"=> {n}" for n in nomes] + [""] + anexar(refs) + ["", "```", prompt, "```", ""]
def bonito(n): return n.split("-", 1)[1].replace("-", " ").capitalize()
o = [f"# Tião Poupador · vídeo {NN}: o que gerar à mão", "",
     f"**Vídeo:** {C.TITULO}  ", f"**Vai ao ar:** {C.PUBLICA_TXT}  ", f"**Prazo:** {C.PRAZO}  ", "",
     f"📁 **Pasta onde salvar tudo:** {PASTA}", "",
     "**Como fazer cada pedido:** abra o link de cada imagem em «Anexar», baixe e anexe no meta.ai (ou no Flow); copie o texto da caixa cinza; gere; salve com o nome indicado, na pasta indicada.",
     "Se algum pedido não ficar bom ou faltar tempo, não tem problema: o robô usa a imagem dele no lugar e o vídeo sai do mesmo jeito.", ""]
CAPAS = [C.CAPA] + list(getattr(C, "CAPAS_TESTE", []))  # o YouTube testa ate 3 capas (Test & compare)
o += [f"## 1. As capas (meta.ai) · {len(CAPAS)} versões, as mais importantes", "", "No meta.ai, escolha o formato **16:9** (horizontal). De cada versão, salve só a melhor das 2. O YouTube testa as versões e fica com a que mais prende.", ""]
NOMES = getattr(C, "NOMES", {})
def arq(cod, n, ext): return f"{cod}_{NOMES[n]}{ext}" if n in NOMES else f"{cod}{ext}"  # o robo acha pelo codigo do comeco
for j, cp in enumerate(CAPAS):
    cc = "CAPA" if j == 0 else f"CAPA-{'ABCDE'[j]}"
    o += bloco(cc, "a capa principal" if j == 0 else f"capa para o teste, versão {'ABCDE'[j]}", cp[0],
               [f"{cc}_{cp[2]}.jpg" if len(cp) > 2 else arq(cc, "capa", ".jpg")],
               UMA + R169 + CONS + "Bold YouTube thumbnail, flat 2D cartoon illustration with thick clean black outlines, very saturated warm colors, cinematic lighting, high contrast, 16:9. " + quem(cp[0]) + cp[1] + " No logos, no brand names.\n" + FIM4)
o += [f"## 2. Imagens principais (meta.ai) · {len(meta)} pedidos", "", "No meta.ai, escolha o formato **16:9** (horizontal). Cada pedido gera 2 imagens que se completam e depois um GIF lento de 4 a 5 segundos entre as duas: salve as 3, cada uma com o seu nome.", ""]
IDS = [x["id"] for x in json.load(open(P + "/fabrica/elenco.json", encoding="utf-8"))["personagens"]]
def grupo(i_n):  # Ed, 06/11: gerar todos de um personagem seguidos (cada um sozinho na ordem do elenco, depois os juntos, depois sem ninguem)
    r = C.IMG[i_n[1]][1]; tem = [k for k, x in enumerate(IDS) if x in r]
    return (tem[0] if len(tem) == 1 else len(IDS) + tem[0] if tem else 2 * len(IDS), r, i_n[0])
o += ["Os pedidos vêm agrupados por personagem (cada personagem sozinho, um de cada vez, e depois as cenas com mais de um): gere na ordem, que a IA mantém o rosto mais igual.", ""]
for i, n in sorted(enumerate(meta, 1), key=grupo):
    refs = C.IMG[n][1]; c = f"M{i:02d}"
    o += bloco(c, bonito(n), refs, [arq(f"{c}-{x}", n, ".jpg") for x in "ab"] + [arq(f"{c}-gif", n, ".gif")],
               DUAS + R169 + CONS + STYLE + quem(refs) + "Scene: " + C.PEDIDO[n] + NEG + "\n" + GIF_LENTO + "\n" + FIM_DUAS)
o += [f"## 3. Clipes animados (Flow) · {len(flow)} pedidos", "", "No Google Flow: modo **Ingredients to Video**, formato **16:9**, e **sem som** (se aparecer a opção de áudio, desligue).", ""]
for i, n in sorted(enumerate(flow, 1), key=grupo):
    refs = C.IMG[n][1]; c = f"F{i:02d}"
    o += bloco(c, bonito(n), refs, [arq(c, n, ".mp4")], R169 + CONS + STYLE + quem(refs) + "Scene: " + C.PEDIDO[n] + SOM + NEG)
codigos = {**{n: f"M{i:02d}" for i, n in enumerate(meta, 1)}, **{n: f"F{i:02d}" for i, n in enumerate(flow, 1)}}
open(f"{P}/fabrica/saida/{NN}-pedidos.md", "w", encoding="utf-8").write("\n".join(o))
import json; json.dump(codigos, open(f"{P}/fabrica/saida/{NN}-codigos.json", "w"), indent=1)
print(f"{len(meta)} meta, {len(flow)} flow -> fabrica/saida/{NN}-pedidos.md")

# --enviar: manda a tarefa para o Apexi Team (uma vez: se ja existe, nao mexe, para nao apagar o que o Ed marcou)
# e o e-mail de reserva junto (ate RESERVA_ATE). Se o Team recusar, o e-mail sai de qualquer jeito.
RESERVA_ATE = "2026-11-20"
# --matheus: a tarefa vai com um tipo proprio; no Team (Projetos > o espaco > Robos) o Ed escolhe uma vez que esse tipo e do Matheus (Ed, 18/11)
TIPO = "imagens-do-video-matheus" if "--matheus" in sys.argv else "imagens-do-video"
if "--enviar" in sys.argv:
    import datetime
    from fabrica import team, correio
    ok, ja = False, False
    try:  # antes da tarefa nova: o que o Ed escreveu nas do video anterior (manual da porta, secao 3, Ed 13/11)
        ant = f"{int(NN) - 1:02d}"; rec = team.recados([team.chave_unica(ant), team.chave_unica(ant) + "-extras", team.chave_unica(ant) + "-refazer", f"tiao-v{ant}-capas"])
        print("📝 recados do Ed no vídeo anterior:" + ("".join(f"\n  {r}" for r in rec) + "\n  ⚠️ conferir se algum muda estes pedidos antes de mandar" if rec else " nenhum"))
    except Exception as e: print("recados do Team não vieram:", e)
    try:
        ja = team.ver(NN) is not None
        if ja: print("Team: a tarefa ja existe, nao mando de novo")
        else:
            r = team.mandar({"chave_unica": team.chave_unica(NN), "tipo": TIPO, "projeto": "Tião Poupador",
                             "titulo": f"Vídeo {NN}: o que gerar à mão ({len(PASSOS)} arquivos)",
                             "descricao": f"{C.TITULO}. Vai ao ar: {C.PUBLICA_TXT}. Anexe cada arquivo no seu passo (ou salve na pasta do Drive). "
                                          "Se faltar algum, o robô usa a imagem dele no lugar.",
                             **({"prazo": C.PRAZO_ISO} if getattr(C, "PRAZO_ISO", None) else {}),
                             "links": [{"rotulo": "Pasta do Drive do vídeo", "url": PASTA}] + ([{"rotulo": "Fotos de referência", "url": PASTA_REF}] if PASTA_REF else []),
                             "passos": PASSOS})
            ok = True; print("Team: tarefa", "criada" if r.get("criada") else "atualizada", r.get("url", ""))
    except Exception as e:
        print("Team recusou (vai so o e-mail):", getattr(e, "code", ""), str(e)[:200])
    if not ja and (not ok or datetime.date.today().isoformat() <= RESERVA_ATE):
        correio.enviar(f"Tião Poupador · vídeo {NN}: o que gerar à mão", "\n".join(o))
