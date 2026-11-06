# Peca do robo: monta o e-mail com os pedidos que o Ed gera a mao (meta.ai: as imagens principais; Flow: os clipes; a capa).
# Uso: python fabrica/pedidos.py 02 ["pasta onde salvar"]   -> fabrica/saida/02-pedidos.md (o e-mail.py manda este texto)
import importlib, os, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
NN = sys.argv[1]; ONDE = sys.argv[2] if len(sys.argv) > 2 else f"Google Drive > Tiao Poupador > entrada > video-{NN}"
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
FIM4 = "Gere a imagem em 4 ângulos diferentes e com total consistência com o personagem que está em referência:"
CONS = ("CHARACTER AND SCENERY CONSISTENCY ARE THE TOP PRIORITY. The characters must be IDENTICAL to the attached reference images, not similar: "
        "same face shape, eyes, eyebrows, nose, mouth, mustache, hairstyle, hair color, skin tone, body shape, height, age, clothes, clothing colors and accessories. "
        "Do not redesign, restyle, beautify, age, slim down or reinterpret them. A similar-looking character is NOT acceptable: match the attached images as closely as possible, in the exact same drawing style. "
        "Correct anatomy: exactly five fingers on each hand, two normal symmetrical eyes, no extra limbs, no faces inside objects. Pose and expression follow the scene, NOT the reference pose. ")
STYLE = "Flat 2D cartoon illustration, clean thin black outlines, soft cel shading, warm slightly desaturated colors, modern explainer animation style, 16:9 widescreen, Brazilian setting. "
QUEM = {
 "tiao": "Tiao: about 30 years old, SHORT and slightly CHUBBY, ROUND face, short messy black hair, a small THIN black pencil mustache (always present, never thick), light brown skin, mustard-yellow polo shirt, faded denim shorts, black flip-flops, black wristwatch, a short yellow carpenter pencil in the shirt pocket. ",
 "sandra": "Sandra: woman in her late 30s, long wavy brown hair, sunglasses pushed up on her head, gold hoop earrings, red blouse, blue jeans, brown handbag. ",
 "marcos": "Marcos: TALL slim man in his late 30s, gelled dark hair, light skin, white shirt with rolled sleeves, dark jeans, brown belt, big silver watch, clean-shaven (NO mustache). ",
}
NEG = " No text, no letters, no numbers, no readable writing, no logos, no brand names, no watermark."
def quem(refs): return "".join(v for k, v in QUEM.items() if k in refs)
QUATRO = ("GENERATE 4 SEPARATE IMAGES AT ONCE: the SAME scene shown from 4 DIFFERENT CAMERA ANGLES, one per image: "
          "1) wide shot showing the whole place, 2) medium shot, 3) close-up on the faces and hands, 4) low angle or over-the-shoulder. "
          "Same characters, same clothes, same place and same moment in all 4 images. ")
QUATRO_FIM = "Remember: 4 separate images, 4 different camera angles, each one 16:9."
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
def anexar(refs):
    return ["📎 **Anexar** (clique para abrir e baixar):"] + [f"- {r}: {REFS.get(r, PASTA_REF)}" for r in [x.strip() for x in refs.split("+")]]
def bloco(cod, titulo, refs, nomes, prompt):
    return [f"### {cod} · {titulo}", "", f"📁 **Salvar na pasta:** {PASTA}", "",
            "📄 **Nome do arquivo** (toque 3 vezes no nome para selecionar e copiar):"] + [f"=> {n}" for n in nomes] + [""] + anexar(refs) + ["", "```", prompt, "```", ""]
def bonito(n): return n.split("-", 1)[1].replace("-", " ").capitalize()
o = [f"# Tião Poupador · vídeo {NN}: o que gerar à mão", "",
     f"**Vídeo:** {C.TITULO}  ", f"**Vai ao ar:** {C.PUBLICA_TXT}  ", f"**Prazo:** {C.PRAZO}  ", "",
     f"📁 **Pasta onde salvar tudo:** {PASTA}", "",
     "**Como fazer cada pedido:** abra o link de cada imagem em «Anexar», baixe e anexe no meta.ai (ou no Flow); copie o texto da caixa cinza; gere; salve com o nome indicado, na pasta indicada.",
     "Se algum pedido não ficar bom ou faltar tempo, não tem problema: o robô usa a imagem dele no lugar e o vídeo sai do mesmo jeito.", ""]
o += ["## 1. A capa (meta.ai) · a mais importante", "", "No meta.ai, escolha o formato **16:9** (horizontal). Salve a melhor das 4.", ""]
NOMES = getattr(C, "NOMES", {})
def arq(cod, n, ext): return f"{cod}_{NOMES[n]}{ext}" if n in NOMES else f"{cod}{ext}"  # o robo acha pelo codigo do comeco
o += bloco("CAPA", "a capa do vídeo", C.CAPA[0], [arq("CAPA", "capa", ".jpg")],
           QUATRO + R169 + CONS + "Bold YouTube thumbnail, flat 2D cartoon illustration with thick clean black outlines, very saturated warm colors, cinematic lighting, high contrast, 16:9. " + quem(C.CAPA[0]) + C.CAPA[1] + " No logos, no brand names.\n" + QUATRO_FIM + "\n" + FIM4)
o += [f"## 2. Imagens principais (meta.ai) · {len(meta)} pedidos", "", "No meta.ai, escolha o formato **16:9** (horizontal). Salve as 4 variações, cada uma com o seu nome.", ""]
for i, n in enumerate(meta, 1):
    refs = C.IMG[n][1]; c = f"M{i:02d}"
    o += bloco(c, bonito(n), refs, [arq(f"{c}-{x}", n, ".jpg") for x in "abcd"], QUATRO + R169 + CONS + STYLE + quem(refs) + "Scene: " + C.PEDIDO[n] + NEG + "\n" + QUATRO_FIM + "\n" + FIM4)
o += [f"## 3. Clipes animados (Flow) · {len(flow)} pedidos", "", "No Google Flow: modo **Ingredients to Video**, formato **16:9**, e **sem som** (se aparecer a opção de áudio, desligue).", ""]
for i, n in enumerate(flow, 1):
    refs = C.IMG[n][1]; c = f"F{i:02d}"
    o += bloco(c, bonito(n), refs, [arq(c, n, ".mp4")], R169 + CONS + STYLE + quem(refs) + "Scene: " + C.PEDIDO[n] + SOM + NEG)
codigos = {**{n: f"M{i:02d}" for i, n in enumerate(meta, 1)}, **{n: f"F{i:02d}" for i, n in enumerate(flow, 1)}}
open(f"{P}/fabrica/saida/{NN}-pedidos.md", "w", encoding="utf-8").write("\n".join(o))
import json; json.dump(codigos, open(f"{P}/fabrica/saida/{NN}-codigos.json", "w"), indent=1)
print(f"{len(meta)} meta, {len(flow)} flow -> fabrica/saida/{NN}-pedidos.md")
