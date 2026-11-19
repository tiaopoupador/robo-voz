# Cenas do video 03 (Tiao Conversa, dinheiro esquecido). Formato em fabrica/LEIA-ME.md e no cenas.py do 02.
# 18/11: por enquanto so a ABERTURA (falas 0 a 3), para a previa que o Ed pediu («tem como gerar um pedaco pra eu ver?»).
from fabrica.kit import *
C, T = "C", "T"  # Dona Cida, Tiao
RUA = "fundo-banquinho"  # fundo da conversa: a varanda do Tiao com o banquinho, sem carro (o 01 tinha a picape)
IMG = {
 # ---- 19/11: o Ed refaz estas no meta.ai (Ed: «parecem crianças», «as duas dentro de uma casa», «muito feia») ----
 "meta-cida-tiao-janela": ('meta', 'cida-ficha.jpg + tiao-frente-sozinho.jpg', 'cf:cida-tiao-janela'),
 "meta-cozinha-cida": ('meta', 'cida-ficha.jpg + tiao-frente-sozinho.jpg', 'cf:cozinha-cida'),
 "meta-cida-vizinha": ('meta', 'cida-ficha.jpg', 'cf:cida-vizinha'),
 "meta-tiao-loja-lembranca": ('meta', 'tiao-frente-sozinho.jpg', 'cf:tiao-loja-lembranca'),
 "meta-banco-1990": ('meta', '', 'cf:banco-1990'),
 # ---- resto do video (19/11) ----
 "cida-tiao-janela": ("cf", C + T, "Medium-wide shot from the sidewalk. Dona Cida leans out of the open window of her small simple Brazilian house holding an old smartphone with a pink case, calling with an excited face; Tiao stands outside on the sidewalk below the window holding a paper bread bag in his LEFT hand, looking up at her, curious. Morning light, potted plants on the windowsill."),
 "cida-mao-peito":   ("cf", C, "Medium shot at her window. She presses her RIGHT hand flat on her chest, shocked and pale, mouth open, round gold glasses, an old smartphone with a pink case in her LEFT hand. Morning light."),
 "cozinha-cida":     ("cf", C + T, "Wide shot of a simple Brazilian kitchen in the morning: a small table with a white crochet tablecloth, two coffee cups, a paper bread bag on the table. Dona Cida pours coffee from a thermos into the cup of Tiao; Tiao sits at the table, smiling politely. Warm light from the window."),
 "papel-pao-conta":  ("cf", "", "Close-up of a brown paper bread bag lying flat on a white crochet tablecloth, with a few short handwritten pencil scribbles and a small sum drawn as plain lines (nothing readable), a short yellow carpenter pencil on top, a coffee cup beside it. No people, no hands."),
 "tiao-loja-lembranca": ("cf", T, "FLASHBACK, faded warm colors. Medium shot: a younger version of him, very young adult, stands behind the counter of a small Brazilian building materials shop (paint cans, cement bags, tools on the wall), wearing a plain name badge clipped to his polo shirt, smiling shyly."),
 "tiao-portaria":    ("cf", T, "Medium shot in the elegant marble lobby of a fancy downtown apartment building: he stands behind the doorman desk with a small plain name badge on his polo shirt, listening with surprised raised eyebrows. Elevator doors in the background. Bright clean light."),
 "cida-oculos":      ("cf", C, "Close-up from the chest up at her kitchen table: she slowly takes off her round gold-rimmed glasses with her RIGHT hand, worried and thoughtful face, eyebrows up. White crochet tablecloth, warm kitchen light."),
 "papel-duas-colunas": ("cf", "", "Flat top-down view, the paper lying FLAT: a flattened brown paper bread bag on a kitchen table with a white crochet tablecloth; one vertical pencil line divides it into a LEFT column and a RIGHT column, each with four short scribbled lines (nothing readable), and the RIGHT column is circled with a thick pencil circle. A short yellow carpenter pencil beside it. No people, no hands."),
 "cida-tiao-celular": ("cf", C + T, "Flat 2D cartoon drawing, NOT realistic, NOT a photo. Exactly TWO different people: one elderly grandmother (Dona Cida, DARK BROWN skin, short curly gray-white hair, round gold glasses, light-blue floral dress, beige cardigan) and one ADULT man about 30 years old, short and chubby (Tiao). Medium shot at the kitchen table with a white crochet tablecloth: Dona Cida and Tiao sit side by side looking together at an old smartphone with a pink case that she holds in BOTH hands, Tiao points at the screen with his RIGHT index finger, both focused. Warm morning light."),
 "cida-feliz":       ("cf", C, "Medium shot at her open window, plain walls with nothing written on them: she laughs with joy, raising an old smartphone with a pink case in her RIGHT hand as if showing the whole street, LEFT hand on her cheek, round gold glasses. Sunny morning."),
 "lourival-caixa":   ("cf", "L", "He holds an old smartphone in his RIGHT hand in front of his chest and reads its screen. Medium shot behind the wooden counter of his small simple Brazilian neighborhood grocery store (shelves with plain solid-color packages, no labels): he looks at an old smartphone over his reading glasses with a surprised face, mouth slightly open. Morning light."),
 "papel-lista":      ("cf", "", "Close-up of a brown paper bread bag on a kitchen table with three short handwritten pencil lines numbered with plain dots (nothing readable), a short yellow carpenter pencil on top. No people, no hands."),
 "cida-vizinha":     ("cf", C, "Medium-wide shot, plain walls with nothing written: Dona Cida (elderly, gray curly hair) at her open window shows an old smartphone with a pink case to a YOUNG neighbor woman in her thirties with long straight BLACK hair and a red T-shirt who passes on the sidewalk carrying a shopping bag; Dona Cida talks seriously with one finger raised. Sunny afternoon."),
 "cida-foto-antiga": ("cf", C, "Flat 2D cartoon drawing, NOT a photo, NOT realistic. Medium shot in her small living room in the late afternoon: she sits in an old armchair holding an old faded black-and-white photograph with BOTH hands, serious and sad face, round gold glasses. Warm dim light."),
 "banco-1990":       ("cf", "", "FLASHBACK, faded colors like an old photo, completely empty scene with NOBODY at all: the closed glass door of an old Brazilian bank branch from 1990 with a metal security grille pulled down, a blank white paper notice taped on the glass, an empty sidewalk. No people."),
 # selo da serie (Ed 18/11: «o tiao sentado numa cadeira de area e tomando um cafezinho e saindo fumacinha da caneca»)
 "selo-tiao-cafe": ("cf", T, "Full body, front three-quarter view. He sits relaxed on a classic Brazilian porch chair made of woven plastic strings in RED and WHITE stripes on a thin silver metal frame, legs crossed at the knee, holding a clean plain white enamel coffee mug with a small chip on the rim with BOTH hands near his chest, eyes half closed, peaceful happy smile. Background: one flat solid pure chroma-key green (#00FF00) from edge to edge, no floor, no shadow, nothing else."),
 "celular-toalha": ("cf", "", "Close-up of an old smartphone with a pink case and a small crack in one corner of the screen, lying on a white crochet tablecloth on a simple kitchen table, morning light from a window, the screen glowing with a plain blank notification bubble. No people, no hands."),
 "fundo-banquinho": ("cf", "", "Wide shot of a small simple Brazilian house porch in the morning: a low wooden stool and an old white enamel mug on a little side table, a colorful quiet suburban street with small houses and palm trees in the background, soft warm sunlight. No people, no cars."),
 "cida-janela":    ("cf", C, "Medium shot from the street. She leans at the open window of her small simple Brazilian house, wearing round thin gold-rimmed reading glasses, holding an old smartphone with a pink case at chest height with BOTH hands, looking at the screen with wide hopeful eyes, mouth visible, morning light, potted plants on the windowsill."),
 "cida-dedo":      ("cf", C, "Close-up from the chest up, three-quarter view. She sits at a kitchen table with a white crochet tablecloth, holding an old smartphone with a pink case in her LEFT hand, her RIGHT index finger hovering just above the screen, about to tap, worried and hopeful face, round gold glasses on her nose."),
}
L = {
 0: [("^", "C", (RUA, "P4", 1)), ("trinta dias", "M", nu(30, "O prazo para o dono reclamar", "depois disso, perdeu de vez", cor=VERM, fmt="int", suf=" dias", emoji="⏳")), ("Quem não reclamou", "C", (RUA, "P4", 1))],
 1: [("^", "C", (RUA, "P2", -1)), ("o celular vibra", "I", "celular-toalha"),
     ("Banco Central informa", "M", nu(1847, "«Banco Central informa»", "clique aqui para liberar", cor=AMAR, casas=2, emoji="📱")),
     ("Clique aqui", "I", "cida-janela")],
 2: [("^", "I", "cida-dedo"), ("três coisas", "M", ic([("🚨", "é golpe?", False), ("🔎", "onde conferir", False), ("⏳", "a medida de maio", False)], "Hoje, três coisas")), ("onde se confere", "C", (RUA, "P2", 1))],
 3: [("^", "C", (RUA, "P2", -1))],  # convite: a pose sorrindo (Ed 18/11: a de apontar de cara fechada nao combina)
 4: [("^", "C", (RUA, "P2", 1))],   # depois da vinheta: «Chega mais!»
 5: [("^", "C", (RUA, "P1", -1)), ("porteiro", "C", (RUA, "P2", -1))],
 6: [("^", "I", "banco:cenarios/rua-bairro-entardecer-01.jpg"), ("papel de pão", "C", (RUA, "P2", -1))],
 7: [("^", "I", "cida-janela"), ("bateu no vidro", "I", "meta-cida-tiao-janela")],
 8: [("^", "I", "meta-cida-tiao-janela"), ("trinta e nove", "M", nu(39.90, "«Taxa para liberar»", "para receber R$ 1.847,00", cor=VERM, casas=2, emoji="🚨"))],
 9: [("^", "C", (RUA, "P4", 1)), ("O link abriu", "M", fr("O link abriu um *WhatsApp* que ninguém conhecia.", "e pediu um Pix"))],
 10: [("^", "M", ic([("💸", "pediu dinheiro?", False), ("🔗", "mandou link?", False), ("🔑", "pediu senha?", False)], "Uma resposta sim = golpe"))],
 11: [("^", "C", (RUA, "P2", -1)), ("não faça qualquer tipo", "M", fr("NÃO faça qualquer tipo de *pagamento* para ter acesso aos valores.", "gov.br, Valores a Receber"))],
 12: [("^", "C", (RUA, "P3", 1)), ("não envia links", "M", fr("O Banco Central *não envia links* nem entra em contato.", "nem SMS, nem WhatsApp, nem ligação"))],
 13: [("^", "M", fr("O banco *nunca* pede a sua senha."))],
 14: [("^", "I", "cida-mao-peito"), ("aplicativo do banco", "C", (RUA, "P3", -1))],
 15: [("^", "C", (RUA, "P2", 1))],
 16: [("^", "I", "meta-cozinha-cida")],
 17: [("^", "C", (RUA, "P2", -1))],
 18: [("^", "C", (RUA, "P2", 1)), ("cinco bilhões", "M", fr("*R$ 5,79 bilhões* esperando os donos.", "Banco Central, dados até agosto de 2026"))],
 19: [("^", "I", "papel-pao-conta"), ("cento e oitenta", "M", nu(180, "Na média, por pessoa", "R$ 4,31 bi para 23,94 milhões de pessoas", cor=VERDE, emoji="💰"))],
 20: [("^", "I", "meta-cozinha-cida"), ("É mesmo", "C", (RUA, "P2", -1))],
 21: [("^", "C", (RUA, "P3", 1)), ("Conta corrente", "M", ic([("🏦", "conta encerrada com saldo", False), ("🧾", "tarifa cobrada a mais", False), ("📄", "parcela cobrada a mais", False), ("🤝", "sobra de cooperativa", False), ("🏍️", "consórcio encerrado", False)], "De onde vem"))],
 22: [("^", "C", (RUA, "P1", -1))],
 23: [("^", "C", (RUA, "P4", 1))],
 24: [("^", "C", (RUA, "P2", -1))],
 25: [("^", "I", "meta-tiao-loja-lembranca")],
 26: [("^", "I", "tiao-portaria"), ("quarenta e sete", "M", nu(47.10, "Esquecido na conta do 1º emprego", "anos com o banco, e não comigo", cor=AMAR, casas=2, emoji="😮"))],
 27: [("^", "M", fr("*R$ 13,35 bilhões* já voltaram para os donos.", "Banco Central, até dezembro de 2025"))],
 28: [("^", "I", "meta-cozinha-cida"), ("mais antigo", "C", (RUA, "P1", 1))],
 29: [("^", "C", (RUA, "P4", -1))],
 30: [("^", "C", (RUA, "P4", 1)), ("trinta dias", "M", nu(30, "O prazo para o dono reclamar", "depois disso, perdeu de vez", cor=VERM, fmt="int", suf=" dias", emoji="⏳"))],
 31: [("^", "C", (RUA, "P2", -1)), ("Medida Provisória", "M", fr("Medida Provisória *1.355*", "4 de maio de 2026, Novo Desenrola"))],
 32: [("^", "C", (RUA, "P2", 1))],
 33: [("^", "M", li(["até 31/12/2024", "maio: vai para o fundo", "30 dias para reclamar"], 1, "O que a medida mandou"))],
 34: [("^", "M", li(["até 31/12/2024", "maio: vai para o fundo", "30 dias para reclamar"], 2, "O que a medida mandou")), ("forma definitiva", "M", fr("Não contestado: incorporado de forma *definitiva* ao fundo.", "art. 13 da MP 1.355"))],
 35: [("^", "I", "cida-oculos"), ("Ninguém avisou", "C", (RUA, "P3", -1))],
 36: [("^", "C", (RUA, "P2", 1)), ("trinta e um de agosto", "M", fr("A medida *caiu* em 31 de agosto.", "não virou lei")), ("não achei", "C", (RUA, "P1", 1))],
 37: [("^", "C", (RUA, "P1", -1))],
 38: [("^", "C", (RUA, "P3", 1))],
 39: [("^", "C", (RUA, "P2", -1)), ("duas colunas", "I", "papel-duas-colunas")],
 40: [("^", "I", "papel-duas-colunas"), ("cinco bilhões", "M", fr("*R$ 5,79 bilhões* estão lá agora.", "dados de agosto, depois da medida"))],
 41: [("^", "C", (RUA, "P4", 1))],
 42: [("^", "I", "cida-tiao-celular")],
 43: [("^", "M", fr("*valoresareceber.bcb.gov.br*", "digite você mesmo, nunca clique em link"))],
 44: [("^", "M", ic([("🪪", "conta gov.br prata ou ouro", False), ("🔐", "verificação em duas etapas", False)], "Para entrar"))],
 45: [("^", "M", ic([("🔑", "escolha a sua chave Pix", False), ("📝", "anote o protocolo", False), ("⏳", "12 dias úteis", False)], "Para receber")), ("não custa nada", "M", fr("Não custa *nada*.", "todos os serviços são gratuitos"))],
 46: [("^", "C", (RUA, "P3", -1))],
 47: [("^", "I", "celular-toalha"), ("trezentos e doze", "M", nu(312.48, "O dinheiro de verdade da Dona Cida", "uma tarifa cobrada a mais", cor=VERDE, casas=2, emoji="🎉"))],
 48: [("^", "M", ba([("O golpe prometia", 1847, VERM), ("O de verdade", 312.48, VERDE)], "O golpe sempre promete mais")), ("é seu", "C", (RUA, "P1", 1))],
 49: [("^", "I", "cida-feliz")],
 50: [("^", "C", (RUA, "P2", -1))],
 51: [("^", "I", "lourival-caixa"), ("Seiscentos e oitenta e três", "M", nu(683, "O consórcio da moto, de 2008", "a sobra que ninguém foi buscar", cor=AMAR, emoji="🏍️"))],
 52: [("^", "C", (RUA, "P3", 1))],
 53: [("^", "C", (RUA, "P4", -1))],
 54: [("^", "C", (RUA, "P2", 1))],
 55: [("^", "C", (RUA, "P1", -1))],
 56: [("^", "V", "banco:FM:3-extrato/extrato__estilo-moldura-celular__horizontal.mp4"), ("sete dias", "M", nu(7, "Dá para testar o FinMoovi", "link na descrição", cor=VERDE, fmt="int", suf=" dias", emoji="📱"))],
 57: [("^", "I", "papel-lista")],
 58: [("^", "M", ic([("🎂", "uma vez por ano, no seu aniversário", False)], "Dica 1"))],
 59: [("^", "M", ic([("✂️", "conta que não usa, pede para fechar", False)], "Dica 2"))],
 60: [("^", "M", ic([("👵", "confere por quem não sabe conferir", False)], "Dica 3"))],
 61: [("^", "C", (RUA, "P3", 1))],
 62: [("^", "I", "meta-cida-vizinha")],
 63: [("^", "C", (RUA, "P2", -1))],
 64: [("^", "I", "cida-foto-antiga")],
 65: [("^", "I", "meta-banco-1990"), ("um ano e meio", "M", fr("A poupança ficou *presa* por um ano e meio.", "Plano Collor, 1990"))],
 66: [("^", "C", (RUA, "P3", 1))],
 67: [("^", "C", (RUA, "P2", -1))],
}
TITULO = "Tem Dinheiro Seu Parado no Banco e Ninguém Te Avisou"
CAPA_TEXTO = "R$ ??? NO SEU NOME"
CLIMA = {0: "alerta"}  # Tiao Conversa: musica de alerta (Ed 18/11)
VINHETA = 3  # a vinheta entra depois da fala 3 («Vamos começar?»)
PUBLICA = "2026-11-21 10:00"
PUBLICA_TXT = "sábado, 21/11, às 10h (Brasília, 13h em Lisboa)"
PRAZO = "sexta, 20/11, até as 18h (o vídeo vai ao ar sábado às 10h)"
CAPA = ("cida-ficha.jpg + tiao-frente-sozinho.jpg",
        "Bright warm yellow background. LEFT, big and close: Tiao, shocked face, mouth open, pointing with one finger at an old phone with a pink case held by Dona Cida. "
        "RIGHT: Dona Cida, an elderly Black Brazilian woman with dark brown skin, white curly hair, round glasses, blue flowered dress and beige cardigan, holding the phone, surprised. "
        "The phone screen shows only a big yellow question mark. Leave the top third empty for the title text.")

# Ed, 19/11 (nota na capa, no Team): «Nao gostei dessa nao! Sempre mande 4 prompts de capas diferentes! Espero mais 3!»
# Identidade das capas (canal-dark titulo-e-capa.md): cor pelo assunto, nunca fundo vazio, Tiao com emocao forte, sem texto (as letras vao por codigo).
CAPAS_TESTE = [
    ("tiao-ficha-oficial.jpg",
     "SECRET / DISCOVERY mood, warm yellow and gold. Inside an old dusty bank vault: a huge round steel safe door slightly open, cobwebs on it, warm golden light and a pile of old coins and banknotes glowing inside. "
     "Tiao, close to the camera, peeks through the gap with wide surprised eyes, one finger on his lips as if keeping a secret, the other hand pulling the heavy door. "
     "Leave the right third empty for the title text.", "cofre-esquecido"),
    ("tiao-ficha-oficial.jpg",
     "URGENT / DEADLINE mood, strong red background with a dark vignette. Tiao, big and close, alarmed, eyebrows up, holds with both hands a giant glass hourglass almost empty: "
     "instead of sand, small gold coins fall to the bottom. A large plain wall calendar behind him with many days crossed out in red (no numbers, no words). "
     "Leave the left third empty for the title text.", "ampulheta-moedas"),
    ("cida-ficha.jpg + tiao-ficha-oficial.jpg",
     "TRAP / SCAM mood, red and dark blue contrast. RIGHT: Dona Cida, happy and naive, holds up her old phone with a pink case; a big metal FISHING HOOK comes out of the phone screen, hanging just in front of her. "
     "LEFT, big and close: Tiao, suspicious, eyes narrowed, stops her with one open hand and points at the hook with the other. Blank glowing phone screen. "
     "Leave the top third empty for the title text.", "anzol-no-celular"),
]
DESC = ("Uma mensagem dizia que a Dona Cida tinha R$ 1.847,00 esquecidos no Banco Central. Era golpe. Mas o dinheiro esquecido existe de verdade: são R$ 5,79 bilhões, de 23,94 milhões de pessoas, segundo o Banco Central.\n\n"
        "Neste vídeo o Tião mostra de onde vem esse dinheiro, o que a medida do governo de maio de 2026 fez com o dinheiro antigo, o único site oficial para conferir, e como não cair no golpe.")
TAGS = ["dinheiro esquecido", "valores a receber", "banco central", "valores a receber banco central", "golpe do pix", "golpe dinheiro esquecido",
        "MP 1355", "educação financeira", "finanças pessoais", "Tião Poupador", "Tião Conversa", "dinheiro parado no banco"]
PERGUNTA = "Você já conferiu se tem dinheiro esquecido no seu nome? Achou quanto?"
CAP_NOMES = {"Abertura (é um Reels: entende-se sozinha)": "Trinta dias para reclamar", "Quem fala": "Chega mais",
             "A mensagem da Dona Cida": "A mensagem da Dona Cida", "De onde vem esse dinheiro": "De onde vem esse dinheiro",
             "Os trinta dias": "Os trinta dias da medida de maio", "A conferida de dois minutos": "A conferida de dois minutos",
             "Para não esquecer de novo": "Para não esquecer de novo"}

GIF = "foto"
PRAZO_ISO = "2026-11-20T18:00:00-03:00"
PEDIDO = {'meta-cida-tiao-janela': 'Morning, seen from the sidewalk of a simple colorful Brazilian neighborhood street. Dona Cida, 67 years old, leans out of the open window of her small house, knocking on the glass with her knuckles and holding an old phone with a pink case, calling him with an excited face. Tiao, an ADULT man about 30 years old with adult body proportions (NOT a child, NOT a teenager), stands on the sidewalk right below the window holding a brown paper bread bag, looking up at her, curious. Cida LEFT, Tiao RIGHT.',
 'meta-cozinha-cida': "A simple Brazilian kitchen in the morning. Dona Cida pours coffee from a thermos into Tiao's cup. Tiao, an ADULT man about 30 years old with adult body proportions (NOT a child), sits at a small table with a white crochet tablecloth, smiling politely; a brown paper bread bag and a short yellow pencil lie on the table. Cida LEFT, Tiao RIGHT.", 'meta-cida-vizinha': 'Seen from the sidewalk OUTSIDE the house: Dona Cida leans out of the open window of her small simple Brazilian house, knocking on the glass and showing her old phone with a pink case. On the sidewalk in front of the window, a neighbor woman in her thirties with long straight black hair and a red T-shirt passes carrying a shopping bag and stops to listen, surprised. Colorful street, potted plants under the window.',
 'meta-tiao-loja-lembranca': 'FLASHBACK with faded warm colors. Tiao when he was about 20 years old: the SAME face, the same short messy black hair and a thin black pencil mustache, slimmer and younger. He stands behind the counter of a small Brazilian building materials shop (paint cans, cement bags, tools on the wall), wearing a plain name badge on his mustard polo shirt, smiling shyly.',
 'meta-banco-1990': 'FLASHBACK, March 1990 in Brazil, faded colors like an old photo. A long line of worried Brazilian people of all ages, in 1990 clothes, in front of an old bank branch with its glass door closed and a metal grille half down. An elderly woman in the line holds a small savings passbook against her chest. A man reads a blank paper notice taped on the door. Nobody smiles.'}
