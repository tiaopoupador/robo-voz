# Cenas do video 07 MODELADO (longo com imagens: Como as Farmacias Ganham Dinheiro? (Nao E o Remedio)). Roteiro: roteiros/07-farmacias.md.
# 27/11/2026: modelo Dinheiro Descomplicado «Como Buffets Livres Ganham Dinheiro? (Nao E Comida)», 12x (ficha 07-preparo.md).
# As cenas com gente vao ao Matheus no Team (pedidos.py 07 --matheus --enviar): 2 imagens + GIF lento por cena.
# Lugares e objetos sem gente: Cloudflare gratis ("cf"). Nenhuma farmacia, rede ou laboratorio com nome ou logotipo.
from fabrica.kit import *

FARM = ("inside a bright modern Brazilian neighborhood drugstore, white floor, clean shelves, soft white light, a long counter at the back, "
        "plain green and white signs with NO words, NO brand, NO logo, NO pharmacy name anywhere, ")
_C = "cida-ficha.jpg"
_T = "tiao-ficha-oficial.jpg"
_CT = "cida-ficha.jpg + tiao-ficha-oficial.jpg"
_V = "valeria-ficha-a.jpg.jpg"
_M = "marcos-neutro.jpg + tiao-ficha-oficial.jpg"
IMG = {
 # ---- lugares e objetos (Cloudflare, sem pessoa) ----
 "fachada":        ("cf", "", "Exterior of a modern Brazilian neighborhood drugstore early on a sunny morning, glass front, green and white colors, a plain blank green sign, an EMPTY sidewalk in front. The street is completely deserted: NOBODY, no people, no pedestrians, no figures, no silhouettes."),
 "entrada-beleza": ("cf", "", "Right after the entrance " + FARM + "shelves full of sunscreen bottles, shampoo, makeup and perfume, beautifully lit, no medicine in sight. No people."),
 "corredor-fundo": ("cf", "", "Long drugstore aisle in one-point perspective, beauty and hygiene products on both sides, the medicine counter very far at the back wall. " + FARM + "No people."),
 "expositor-caixa":("cf", "", "Drugstore checkout counter with a small metal impulse rack full of chocolate bars, candies, chewing gum, batteries and small water bottles, a card machine. " + FARM + "No people."),
 "etiqueta":       ("cf", "", "Extreme close-up of a blank white drugstore shelf price tag with ONLY two thick horizontal grey bars (no digits, no letters, no numbers at all); the top bar is crossed out with a thick red diagonal line, a small green sticker shape next to it. Colorful blurred boxes around. No people."),
 "maquininha":     ("cf", "", "Extreme close-up of a black card payment machine lying on a white drugstore counter, its screen glowing with one big plain green rounded button with a white check mark icon and some tiny grey lines (no words, no letters). Empty blurred background, nobody in the scene, no people, no hands."),
 "governo":        ("cf", "", "A modern government building in Brasilia on a sunny day, the Brazilian flag waving in front, clear blue sky. No people, no readable text."),
 "farm-popular":   ("cf", "", "Close-up of the glass door of a Brazilian drugstore with a round generic sticker of a government health program (a simple heart and cross drawing, NO words), sunny street reflected. No people."),
 # ---- cenas com gente (o Matheus, no Team) ----
 "meta-cida-calcada":  ("meta", _CT, "cf:fachada"),
 "meta-cida-balcao":   ("meta", _C, "cf:maquininha"),
 "meta-cida-muro":     ("meta", _CT, "cf:fachada"),
 "meta-iogurte":       ("meta", "nenhuma", "cf:entrada-beleza"),
 "meta-cida-corredor": ("meta", _C, "cf:corredor-fundo"),
 "meta-cida-caixa":    ("meta", _C, "cf:expositor-caixa"),
 "meta-cida-termo":    ("meta", _CT, "cf:maquininha"),
 "meta-cida-lista-gov":("meta", _CT, "cf:farm-popular"),
 "meta-senhor-receita":("meta", "nenhuma", "cf:farm-popular"),
 "meta-fila":          ("meta", "nenhuma", "cf:expositor-caixa"),
 "meta-cida-cozinha":  ("meta", _C, "cf:etiqueta"),
 "meta-cida-volta":    ("meta", _C, "cf:corredor-fundo"),
 "meta-cida-sai":      ("meta", _CT, "cf:fachada"),
 "meta-valeria-caixa": ("meta", _V, "cf:expositor-caixa"),
 "meta-marcos-portaria":("meta", _M, "cf:governo"),
}
_CIDA = "Dona Cida (kind grandmother about 67, short and a little plump, dark brown skin, short curly gray-white hair, round thin gold-rimmed glasses, light-blue floral dress with a beige knitted cardigan)"
_TIAO = "Tiao, an ADULT man about 30 years old with adult body proportions (NOT a child, NOT a teenager), mustard-yellow polo shirt"
PEDIDO = {
 "meta-cida-calcada":  f"Morning, on the sidewalk right outside a modern Brazilian neighborhood drugstore (plain sign with NO words). {_CIDA}, pale and worried, holds a small paper pharmacy bag in one hand and pushes her lit phone toward {_TIAO}, who leans in to read the screen, surprised. Cida LEFT, Tiao RIGHT.",
 "meta-cida-balcao":   f"{FARM}{_CIDA} stands at the medicine counter; a young smiling pharmacy attendant in a white coat (no name tag text) turns a card machine toward her; Cida presses the big green button on the machine without reading, trusting. Cida LEFT, attendant RIGHT behind the counter.",
 "meta-cida-muro":     f"Sunny sidewalk outside the drugstore. {_CIDA} leans back against a low wall, pale, holding the paper pharmacy bag tight against her chest, phone in her other hand. {_TIAO} stands next to her, worried, one hand gently on her shoulder.",
 "meta-iogurte":       "Inside a bright Brazilian supermarket aisle: a friendly promoter woman in a plain red apron (no logo) stands behind a small table offering tiny cups of yogurt to two shoppers who taste them, smiling; she writes their names on a clipboard. No readable text, no brands.",
 "meta-cida-corredor": f"{FARM}{_CIDA} walks down a very long aisle full of shampoo, makeup and sunscreen toward the medicine counter far at the back, looking around at the colorful shelves, slightly lost. Seen from behind at three-quarter view.",
 "meta-cida-caixa":    f"{FARM}At the checkout, {_CIDA} places a sunscreen bottle and a chocolate bar next to her small medicine box on the counter, a little embarrassed smile; a metal rack full of candies and chocolate right beside her.",
 "meta-cida-termo":    f"In the lobby of a fancy city apartment building, at the doorman desk. {_TIAO} (the doorman) and {_CIDA} look together at her phone: the screen shows a very long paragraph of tiny unreadable text. Cida frowns, Tiao points at the screen.",
 "meta-cida-lista-gov":f"Doorman desk in the lobby of a fancy apartment building, afternoon. {_TIAO} holds his phone showing a simple list (blurred, unreadable); {_CIDA} taps the screen with her finger, mouth open in shock, the other hand on her chest.",
 "meta-senhor-receita":f"{FARM}An elderly Brazilian man with a cane hands a paper prescription across the counter to a smiling pharmacist in a white coat; on the glass door behind, a round generic government health program sticker (a heart and a cross, NO words).",
 "meta-fila":          f"{FARM}A checkout line of four different people: an older woman, a young man in a work uniform looking at his watch, a mother holding a small child's hand, a young woman on her phone. A card machine on the counter. No readable text.",
 "meta-cida-cozinha":  f"Simple Brazilian kitchen in the morning, a red and white checkered tablecloth, a coffee cup. {_CIDA} sits at the table with her round glasses on, typing a short shopping list on her phone with one finger, concentrated, satisfied.",
 "meta-cida-volta":    f"{FARM}{_CIDA}, firm and confident, a paper prescription and a small receipt in her hand, asks a question at the counter; the young attendant behind it looks embarrassed, not knowing what to answer.",
 "meta-cida-sai":      f"Sunny sidewalk outside a Brazilian drugstore (plain sign with NO words). {_CIDA} walks out smiling, lifting a small paper pharmacy bag like a trophy; {_TIAO}, on the sidewalk, waves and smiles back proudly.",
 "meta-valeria-caixa": f"{FARM}At the checkout, Valeria (elegant woman about 36, sunglasses pushed up on her head, white blazer) puts her phone away and politely refuses with a small hand gesture while the attendant waits; in the line behind her, a short chubby man in a mustard polo (Tiao) watches with a small smile.",
 "meta-marcos-portaria":f"Early morning in the lobby of a fancy city apartment building. Marcos (tall slim man, gelled dark hair, white shirt, big silver watch, clean-shaven) stands at the doorman desk holding out a folded banknote, with a car key in his other hand, a hesitant face as if about to ask something; {_TIAO}, the doorman, behind the desk, takes the note, surprised.",
}
NOMES = {}
TITULO = "Como as Farmácias Ganham Dinheiro? (Não É o Remédio)"
MODELO = {"id": "JMDZ-934bpo", "canal": "@dinheirodescomplicadooficial", "vezes": 12.0}
CAPA_TEXTO = "DESCONTO DE FARMÁCIA É ISCA"
# 26/11: o texto vai DENTRO do prompt (pedidos.py). Modelagem: a capa A tem a MESMA composicao do modelo (balcao em primeiro
# plano, clientes a esquerda, atendente esperta no caixa a direita, fundo azul de planta tecnica, titulo grande no alto, setas).
CAPA_LETRAS = {"A": ("DESCONTO DE FARMÁCIA É ISCA", "ISCA", "vermelho"), "B": ("SEU CPF TEM PREÇO", "PREÇO", "amarelo"),
               "C": ("O REMÉDIO É O DE MENOS", "DE MENOS", "vermelho"), "D": ("ELES SABEM O SEU REMÉDIO", "SABEM", "amarelo")}
PUBLICA = "2026-11-29 17:00"
PUBLICA_TXT = "domingo, 29/11, às 17h (Brasília, 20h em Lisboa)"
PRAZO = "sábado, 28/11, até as 20h (o vídeo vai ao ar domingo às 17h)"
PRAZO_ISO = "2026-11-28T20:00:00-03:00"
CAPA = (_C, "Same composition as a classic 'how businesses make money' thumbnail. Bright BLUE blueprint background with thin white technical lines. "
            "In the foreground, a long drugstore counter full of colorful products (sunscreen, shampoo, chocolate, small medicine boxes without any text). "
            "LEFT: Dona Cida, 67, dark brown skin, short curly gray-white hair, round gold-rimmed glasses, light-blue floral dress and beige cardigan, holding a small pharmacy bag, shocked face, mouth open. RIGHT: a smirking young "
            "pharmacy attendant in a white coat behind a card machine, one eyebrow up, sly smile. Four thick black hand-drawn ARROWS point at the card machine, "
            "the medicine box, the chocolate rack and the attendant's screen (arrows only, no labels). Leave the TOP band empty for one big title line.", "balcao-azul")
CAPAS_TESTE = [
    (_C, "ALERT mood, red and dark blue. Close-up: Dona Cida (67, dark brown skin, short curly gray-white hair, round gold-rimmed glasses) big on the RIGHT, pale, holding her phone toward the viewer: on the "
         "screen a big pill icon and a message bubble (no readable text). Behind her, out of focus, a drugstore counter. Leave the left half empty for the title.", "mensagem"),
    (_C, "MONEY mood, yellow and green. A giant ID card shape (blank, no text, no numbers) on a drugstore counter being weighed on an old two-pan scale against "
         "a small medicine box; the card side is heavier. Dona Cida on the LEFT, hands on her cheeks, surprised. Leave the top third empty for the title.", "balanca"),
    (_CT, "INVESTIGATION mood, deep blue and red. Tiao (adult, mustard polo) holds a big magnifying glass over a long drugstore receipt that unrolls to the floor; "
          "Dona Cida beside him points at one line (only scribbles, nothing readable). Leave the top third empty for the title.", "lupa"),
]
DESC = ("A Dona Cida pagou menos da metade do preço no remédio de pressão, só por dar o CPF. Três minutos depois, uma mensagem no celular dela já "
        "sabia o nome do remédio.\n\n"
        "Neste vídeo o Tião mostra, com os documentos do governo na mão, como as farmácias ganham dinheiro: quem paga o desconto por CPF (os programas "
        "dos laboratórios), por que o preço da etiqueta é um teto e não o preço de verdade (Anvisa e a Nota Técnica 6/2025 da Autoridade Nacional de "
        "Proteção de Dados), o desenho da loja, o Farmácia Popular (remédio de pressão de graça desde fevereiro de 2025), o que diz a Lei Geral de "
        "Proteção de Dados sobre dado de saúde e a lei de São Paulo sobre o CPF na farmácia.")
TAGS = ["como as farmácias ganham dinheiro", "cpf na farmácia", "desconto na farmácia", "por que a farmácia pede cpf", "farmácia popular",
        "remédio de graça", "lgpd", "dados de saúde", "preço máximo do remédio", "anpd farmácia", "educação financeira", "Tião Poupador"]
PERGUNTA = "Você sabia que o seu remédio de uso contínuo pode sair de graça? Sabia ou não sabia?"
GIF = "foto"

# ---------- as cenas por fala (27/11, depois do roteiro revisado) ----------
from fabrica.videos.v03.cenas import IMG as _I3
IMG.update({k: _I3[k] for k in ("fundo-banquinho", "selo-tiao-cafe")})
RUA = "fundo-banquinho"
def tiao(pose, lado=1): return (RUA, pose, lado)
def cel(titulo, linhas, destaque=()): return {"k": "celular", "titulo": titulo, "linhas": [{"r": a, "v": b, **({"pos": True} if p else {})} for a, b, p in linhas], "destaque": list(destaque)}
VINHETA = 3
CLIMA = {0: "alerta", 4: "calma", 9: "tensao", 12: "humor", 15: "curiosa", 19: "curiosa", 22: "tensao", 25: "drama", 27: "virada", 30: "reflexiva",
         34: "drama", 40: "calma", 42: "virada", 44: "humor", 46: "reflexiva", 47: "final"}
MSG = cel("Mensagem nova", [("Olá, Dona Cida!", "", True), ("O seu remédio de pressão acaba no dia 20.", "", False), ("Quer receber em casa?", "", False)], [1])
L = {
 0: [("^", "I", "meta-cida-calcada"), ("menos da metade", "M", nu(50, "A menos no remédio de pressão", "menos da metade do preço", cor=VERDE, emoji="💊")),
     ("mensagem", "M", MSG)],
 1: [("^", "I", "meta-cida-calcada"), ("documento do governo", "I", "governo"),
     ("potencialmente fictícios", "M", fr("Descontos *potencialmente fictícios*", "Autoridade Nacional de Proteção de Dados, Nota Técnica 6/2025"))],
 2: [("^", "M", ic([("🏷️", "o que a farmácia vende de verdade", False), ("💸", "de onde vem o dinheiro do desconto", False), ("🫵", "quem paga a conta", False)], "Até o fim, 3 respostas")),
     ("Spoiler", "C", tiao("P4", 1))],
 3: [("^", "C", tiao("P2", 1)), ("puxa a cadeira", "I", "fachada")],
 4: [("^", "C", tiao("P1", -1))],
 5: [("^", "C", tiao("P2", 1)), ("Dona Cida", "I", "meta-cida-muro"), ("voltar uns minutos", "C", tiao("P3", -1))],
 6: [("^", "I", "meta-cida-balcao"), ("oitenta e nove", "M", nu(89.90, "O preço na etiqueta", casas=2, emoji="🏷️")),
     ("maquininha", "I", "maquininha"), ("trinta e nove", "M", nu(39.90, "Com o CPF", "depois do «sim»", cor=VERDE, casas=2, emoji="💊"))],
 7: [("^", "M", nu(50, "A menos", "menos da metade do preço!", cor=VERDE, emoji="😮")), ("desconfiada", "C", tiao("P4", -1)), ("Na calçada", "M", MSG)],
 8: [("^", "I", "meta-cida-muro"), ("documentos", "I", "governo")],
 9: [("^", "I", "governo"), ("Autoridade Nacional", "M", fr("*5 de fevereiro de 2025*: a Autoridade Nacional de Proteção de Dados abre processo", "contra a maior rede de farmácias do país")),
     ("A suspeita", "M", fr("Suspeita: perfis feitos com *dados de saúde* para vender propaganda", "Agência Brasil, 08/02/2025"))],
 10: [("^", "M", nu(8497500, "Multa do Procon de Minas Gerais", "dezembro de 2024, por exigir o CPF", cor=VERM, emoji="⚖️")),
      ("ainda está aberto", "M", fr("O processo do governo está *aberto*.", "A empresa diz que segue a lei.")), ("ninguém briga", "C", tiao("P3", 1))],
 11: [("^", "C", tiao("P1", -1)), ("furo", "M", fr("Um furo do tamanho de um *balcão*.")), ("supermercado", "C", tiao("P2", 1))],
 12: [("^", "I", "meta-iogurte"), ("fábrica do iogurte", "M", ic([("🏭", "a fábrica paga o copinho", False), ("🛒", "o mercado só empresta o corredor", False)], "O copinho do iogurte"))],
 13: [("^", "I", "meta-iogurte"), ("mensagem do iogurte", "C", tiao("P3", -1)), ("na farmácia", "M", fr("Na farmácia, o copinho é o *desconto* do seu remédio."))],
 14: [("^", "C", tiao("P2", 1)),
      ("documento técnico", "M", fr("No programa do laboratório, é ele quem *decide os dados*; a farmácia atua *apenas como operadora*", "Autoridade Nacional de Proteção de Dados, Nota Técnica 6/2025")),
      ("A farmácia é o corredor", "I", "corredor-fundo")],
 15: [("^", "M", nu(89.90, "O número da etiqueta", "é o teto, não o preço", cor=VERM, casas=2, emoji="🏷️")), ("preço máximo", "M", fr("Preço máximo ao consumidor = *teto*", "câmara do governo que regula o preço dos remédios")),
      ("qualquer valor abaixo", "M", fr("Qualquer valor *abaixo* do teto é permitido.", "Anvisa"))],
 16: [("^", "C", tiao("P4", -1)), ("muito superiores", "M", fr("Preços máximos *muito superiores* aos custos de fabricação", "Autoridade Nacional de Proteção de Dados, Nota Técnica 6/2025")),
      ("potencialmente fictícios", "M", fr("Descontos expressivos, mas *potencialmente fictícios*")), ("era o teto", "C", tiao("P3", 1))],
 17: [("^", "C", tiao("P2", 1)), ("âncora", "M", ci("Tversky e Kahneman", 1974, "revista Science", "o primeiro número que você vê vira a régua de tudo")),
      ("Prêmio Nobel", "M", fr("Kahneman: *Prêmio Nobel* de Economia, 2002")),
      ("O oitenta e nove", "M", ba([("A âncora (etiqueta)", 89.90, VERM), ("Com o CPF", 39.90, VERDE)], "Parece presente"))],
 18: [("^", "C", tiao("P3", -1)), ("inscreve", "C", tiao("P2", 1)), ("dentro da loja", "I", "entrada-beleza")],
 19: [("^", "I", "fachada"), ("A primeira coisa", "I", "entrada-beleza"), ("corredor da beleza", "H", ("entrada-beleza", [et("a porta: beleza", 30, 25)]))],
 20: [("^", "I", "meta-cida-corredor"), ("lá no fundo", "I", "corredor-fundo"), ("leite no fundo", "C", tiao("P3", 1))],
 21: [("^", "I", "expositor-caixa"), ("Leve três", "M", fr("Leve *3*, pague 2")), ("A Dona Cida", "I", "meta-cida-caixa")],
 22: [("^", "C", tiao("P4", -1)),
      ("pesquisa de mercado", "M", ic([("🛍️", "o que você compra", False), ("📅", "quando compra", False), ("⏳", "quando acaba", False), ("🧺", "junto com o quê", False)], "A pesquisa de graça")),
      ("Só um", "I", "maquininha")],
 23: [("^", "M", fr("Dado referente à saúde = *dado pessoal sensível*", "Lei 13.709/2018, art. 5º, II (Lei Geral de Proteção de Dados)")), ("pressão alta", "C", tiao("P2", 1))],
 24: [("^", "I", "meta-cida-cozinha"),
      ("fralda geriátrica", "M", ic([("💊", "remédio de pressão: dia certo para acabar", False), ("🧓", "fralda geriátrica: um idoso em casa", False), ("🍼", "teste de gravidez: um bebê a caminho", False)], "Cada caixinha conta")),
      ("montar perfis", "I", "governo")],
 25: [("^", "I", "meta-cida-termo"), ("laboratório", "M", fr("Quem mandou a mensagem: o *laboratório* do remédio")), ("dia em que a caixa acaba", "C", tiao("P4", 1))],
 26: [("^", "M", nu(50, "A menos no remédio de pressão", "menos da metade do preço", cor=VERDE, emoji="💊")), ("mensagem", "I", "meta-cida-calcada"),
      ("O desconto foi o copinho", "M", fr("O desconto foi o *copinho*.", "O preço de verdade foi a informação."))],
 27: [("^", "C", tiao("P2", -1)), ("Primeiro", "M", ic([("🏭", "o laboratório paga boa parte do desconto", False)], "1"))],
 28: [("^", "I", "entrada-beleza"), ("preço máximo", "M", ic([("💊", "remédio de receita: preço máximo regulado", False), ("🧴", "xampu: sem teto", False)], "2")),
      ("corredor da beleza", "I", "corredor-fundo")],
 29: [("^", "I", "meta-senhor-receita"), ("Farmácia Popular", "I", "farm-popular"),
      ("trinta e uma mil", "M", nu(31170, "Farmácias credenciadas", "Agência Gov, janeiro de 2025", fmt="int", emoji="🏥")),
      ("três bilhões", "M", nu(3600000000, "O programa em 2024", "Agência Gov", emoji="💰"))],
 30: [("^", "C", tiao("P4", -1)), ("de graça", "M", fr("Desde fevereiro de 2025: *100% de graça*", "site oficial do Ministério da Saúde")),
      ("pressão alta", "M", ic([("🧾", "receita do posto ou de médico particular", False), ("🪪", "documento com foto", False), ("🔢", "CPF", False)], "Remédio de pressão: o que levar"))],
 31: [("^", "I", "meta-cida-lista-gov"), ("Eu pagava por isso", "M", nu(39.90, "Ela pagava por mês", "por um remédio de graça", cor=VERM, casas=2, emoji="😳"))],
 32: [("^", "C", tiao("P2", 1)), ("regra de um programa do governo", "M", fr("No Farmácia Popular, o CPF é *regra do programa*", "para registrar a entrega, não para vender"))],
 33: [("^", "C", tiao("P3", -1)), ("comentários", "M", fr("Comenta: *sabia* ou *não sabia*?")), ("quem paga", "C", tiao("P4", 1))],
 34: [("^", "I", "meta-fila"), ("paga em informação", "M", ba([("Com CPF: paga em dados", 39.90, AMAR), ("Sem CPF: paga perto do teto", 89.90, VERM)], "Os dois pagam"))],
 35: [("^", "C", tiao("P4", -1)), ("duas vezes", "M", fr("Quem paga a conta? *Você.* Duas vezes."))],
 36: [("^", "C", tiao("P2", 1)), ("não é livre", "M", fr("Um «sim» com R$ 50 na frente *não é livre*", "Autoridade Nacional de Proteção de Dados, Nota Técnica 6/2025"))],
 37: [("^", "M", fr("Dado de saúde não se passa para outra empresa *para ganhar dinheiro*", "Lei 13.709/2018, art. 11, § 4º")), ("cuidar de você", "C", tiao("P3", 1))],
 38: [("^", "M", fr("São Paulo: a farmácia não pode exigir o CPF *sem explicar* o cadastro", "Lei estadual 17.301/2020, art. 1º")), ("aviso na loja", "I", "farm-popular")],
 39: [("^", "M", fr("Rio de Janeiro: o *Ministério Público Federal* investiga se é prática abusiva", "fevereiro de 2025"))],
 40: [("^", "I", "meta-cida-cozinha")],
 41: [("^", "I", "meta-cida-cozinha"), ("FinMoovi", "V", "banco:FM:5-compras/compras__estilo-carrinho__horizontal.mp4"),
      ("sete dias", "M", nu(7, "Dá para testar o FinMoovi", "link na descrição · www.finmoovi.com", cor=VERDE, fmt="int", suf=" dias", emoji="📱"))],
 42: [("^", "I", "meta-cida-volta"), ("sem o cê pê éfe", "M", fr("1. O preço *sem* o CPF")), ("cadastro é para quê", "I", "meta-cida-volta"),
      ("sair do programa", "M", fr("2. *Saiu* do programa do laboratório")), ("de graça", "I", "meta-cida-sai")],
 43: [("^", "M", nu(478.80, "Por ano, que ficam com ela", "R$ 39,90 × 12", cor=VERDE, casas=2, emoji="✅")), ("Caneca velha", "I", "meta-cida-sai")],
 44: [("^", "I", "meta-valeria-caixa"), ("Hoje não", "M", fr("«Hoje *não*, obrigada.»")), ("canto de olho", "C", tiao("P1", 1))],
 45: [("^", "M", ic([("🏷️", "o preço sem o CPF, antes de dar o número", False), ("🏥", "o remédio de todo mês no Farmácia Popular", False)], "As duas coisas da Dona Cida"))],
 46: [("^", "C", tiao("P2", -1)), ("o caminho até ele", "I", "corredor-fundo"), ("fiado do laboratório", "M", fr("O seu CPF virou o *fiado* do laboratório."))],
 47: [("^", "I", "meta-marcos-portaria"), ("Qual é o número", "M", fr("«Tião... qual é o *número*?»")), ("buzinou", "C", tiao("P4", 1))],
 48: [("^", "M", fr("A regra dos *R$ 1.000*", "o número que te tira da corrida dos ratos")), ("Clica agora", "C", tiao("P2", 1))],
}
