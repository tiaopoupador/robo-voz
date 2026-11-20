# Cenas do video 04 (Tiao Conversa, Dona Cida 1990). Formato em fabrica/LEIA-ME.md e no cenas.py do 03 (o molde aprovado com nota 8).
# 20/11: primeiro so os PEDIDOS das imagens (vao para o Ed pelo Team); o L (cena por fala) entra depois da voz gravada.
from fabrica.kit import *
C, T = "C", "T"  # Dona Cida, Tiao
RUA = "fundo-banquinho"
CIDA_HOJE = "Dona Cida, 67 years old, dark brown skin, short curly white hair, round gold glasses, light-blue floral dress, beige cardigan"
CIDA_1990 = ("FLASHBACK with faded warm colors like an old photo, Brazil in 1990. Dona Cida when she was about 30 years old: the SAME face as the reference, "
             "dark brown skin, BLACK curly hair tied back, no glasses, a simple 1990 cotton dress, a handbag on her shoulder")
TIAO = "Tiao, an ADULT man about 30 years old with adult body proportions (NOT a child, NOT a teenager)"
IMG = {
 "meta-cozinha-lata":    ('meta', 'cida-ficha.jpg + tiao-ficha-oficial.jpg', 'cf:cozinha-cida'),
 "meta-costura-1990":    ('meta', 'cida-ficha.jpg', 'cf:cida-foto-antiga'),
 "meta-fila-banco-1990": ('meta', 'cida-ficha.jpg', 'cf:banco-1990'),
 "meta-caixa-1990":      ('meta', 'cida-ficha.jpg', 'cf:banco-1990'),
 "meta-cama-1990":       ('meta', 'cida-ficha.jpg', 'cf:cida-foto-antiga'),
 "meta-tiao-conta":      ('meta', 'cida-ficha.jpg + tiao-ficha-oficial.jpg', 'cf:papel-pao-conta'),
 "meta-cida-lata-seria": ('meta', 'cida-ficha.jpg', 'cf:cida-oculos'),
 "meta-cida-janela-ri":  ('meta', 'cida-ficha.jpg', 'cf:cida-feliz'),
 "meta-cida-sobrinha":   ('meta', 'cida-ficha.jpg', 'cf:cida-vizinha'),
 # 20/11 (revisor: a virada de 1994 precisa da causa): a lata da comadre queimada, sem ninguem (Cloudflare, gratis)
 "lata-queimada-1994": ("cf", "", "FLASHBACK, faded colors like an old 1994 photo. Close-up of a burned, blackened round biscuit tin lying open on the floor of a burned room, gray ashes and a few burnt paper scraps inside, soft smoke. No people, no hands, no text."),
 "meta-janela-noite-suv": ('meta', 'cida-ficha.jpg + rua-casa-suv.jpg', 'cf:cida-janela'),
}
PEDIDO = {
 "meta-cozinha-lata": f"A simple Brazilian kitchen in the afternoon. {CIDA_HOJE}, sits at a small table with a white crochet tablecloth and opens an old ROUND BLUE biscuit tin: inside, a few banknotes and an old worn BLUE savings passbook, which she lifts carefully with both hands. {TIAO}, sits across the table with a white enamel mug with a chipped rim, watching quietly. Cida LEFT, Tiao RIGHT.",
 "meta-costura-1990": f"{CIDA_1990}. At night in a small simple 1990 bedroom, she sews a white dress on an old black sewing machine under a weak yellow lamp, tired but determined; a small blue savings passbook rests next to the machine.",
 "meta-fila-banco-1990": f"{CIDA_1990}. A long line of worried Brazilian people of all ages in 1990 clothes on the sidewalk in front of an old bank branch with a metal grille half down; a man in a suit cries with his hand over his face; an elderly lady sits on the curb with her hand on her chest. Young Dona Cida, in the line, holds a small blue savings passbook against her chest, anxious. Nobody smiles.",
 "meta-caixa-1990": f"{CIDA_1990}. Inside an old 1990 Brazilian bank branch, at the teller counter with a glass window: she holds out an open blue savings passbook, shocked; the young male teller behind the glass shakes his head without looking at the paper. Old wooden counters, old calculators, no computers.",
 "meta-cama-1990": f"{CIDA_1990}. Evening in her small simple bedroom: she sits on the edge of the bed holding the blue savings passbook on her lap with both hands, staring at it, sad and silent, eyes wet. A sewing machine in the corner.",
 "meta-tiao-conta": f"Her simple Brazilian kitchen, afternoon. {TIAO}, writes a calculation with a short yellow carpenter pencil on a flattened brown paper bread bag on the table (scribbles only, nothing readable). {CIDA_HOJE}, sits next to him with arms crossed and one eyebrow raised, suspicious; the round blue biscuit tin is open on the table. Tiao LEFT, Cida RIGHT.",
 "meta-cida-lata-seria": f"Close medium shot at her kitchen table: {CIDA_HOJE}, looks down into the open round blue biscuit tin full of old banknotes, serious and shocked, one hand on her cheek, as if she just understood something. Warm afternoon light.",
 "meta-cida-janela-ri": f"Seen from the sidewalk OUTSIDE her small simple colorful Brazilian house: {CIDA_HOJE}, leans out of her open window and laughs with a clever look, one finger raised as if telling a secret; the round blue biscuit tin sits on the windowsill among potted plants. Sunny afternoon.",
 "meta-cida-sobrinha": f"Her small living room, afternoon. {CIDA_HOJE}, shows the open round blue biscuit tin and the old blue savings passbook to her niece, a young Brazilian woman in her twenties with long curly black hair and a yellow T-shirt, who listens surprised. Family photos on the wall (blank frames).",
 "meta-janela-noite-suv": f"NIGHT. Seen from the street: {CIDA_HOJE}, leans at her lit open window and points with her chin across the dark street at a big shiny WHITE SUV parked in front of a modern house with a large glass front, suspicious face. The street lamps are on, the rest of the street is dark and quiet.",
}
TITULO = "Dona Cida Não Confia em Banco Desde 1990. Ela Tem Razão?"
CAPA_TEXTO = "E SE VOLTAR?!"
CLIMA = {0: "alerta"}
VINHETA = 3  # a vinheta entra depois da fala 3 («Vamos começar?»)
PUBLICA = "2026-11-24 10:00"
PUBLICA_TXT = "terça, 24/11, às 10h (Brasília, 13h em Lisboa)"
PRAZO = "domingo, 22/11, até as 18h (o vídeo vai ao ar terça às 10h)"
PRAZO_ISO = "2026-11-22T18:00:00-03:00"
CAPA = ("cida-ficha.jpg",
        "DANGER / FEAR mood, strong red background with a dark vignette. Dona Cida, an elderly Black Brazilian woman with dark brown skin, white curly hair, round glasses, "
        "blue flowered dress and beige cardigan, big and close on the RIGHT, serious and suspicious, hugs an old blue savings passbook against her chest with both hands. "
        "Behind her, the closed metal door of an old bank, with a heavy chain and padlock. Leave the left half empty for the title text. No text, no letters, no numbers anywhere (the title goes on later).")
CAPAS_TESTE = [
    ("cida-ficha.jpg + tiao-ficha-oficial.jpg",
     "SECRET mood, warm yellow and gold. A kitchen table seen close: an old round blue biscuit tin wide open, glowing, full of old banknotes. Dona Cida (RIGHT) holds the lid, suspicious, "
     "one finger on her lips; Tiao (LEFT), big and close, shocked, eyebrows up, pointing at the tin. Leave the top third empty for the title text. No text, no letters, no numbers anywhere (the title goes on later).", "lata-segredo"),
    ("cida-ficha.jpg",
     "MEMORY mood, sepia and faded orange like an old 1990 photo. A long worried line of people in front of a closed old bank door; in front, big and close, young Dona Cida "
     "(about 30, black curly hair tied back, the same face as the reference) holds a blue savings passbook against her chest, eyes wet. Leave the right third empty for the title text. No text, no letters, no numbers anywhere (the title goes on later).", "fila-1990"),
    ("cida-ficha.jpg + tiao-ficha-oficial.jpg",
     "LOSS mood, cold blue and red. An old mattress lifted at one corner: banknotes hidden under it are crumbling into dust and flying away. Dona Cida (LEFT) lifts the mattress, shocked; "
     "Tiao (RIGHT), big and close, holds a brown paper bread bag with a calculation, worried. Leave the top third empty for the title text. No text, no letters, no numbers anywhere (the title goes on later).", "colchao-some"),
]
DESC = ("Em março de 1990, a Dona Cida foi ao banco buscar o dinheiro de dez anos de costura, e ouviu: «acima de cinquenta mil, não sai». Desde então ela guarda tudo em casa.\n\n"
        "Neste vídeo o Tião mostra, com a lei na mão, o que fizeram com a poupança em 1990, o que protege o seu dinheiro hoje (e o que não protege), quanto o dinheiro guardado em casa perdeu desde o Plano Real, "
        "e a única coisa que a Dona Cida faz até hoje para nunca mais ser pega de surpresa.")
TAGS = ["plano collor", "confisco da poupança", "confisco 1990", "poupança 1990", "FGC", "fundo garantidor de créditos", "dinheiro no colchão",
        "inflação plano real", "educação financeira", "finanças pessoais", "Tião Poupador", "Tião Conversa"]
PERGUNTA = "Na sua família, alguém perdeu dinheiro naquele março de 1990?"
CAP_NOMES = {"Abertura (é um Reels: entende-se sozinha)": "Março de 1990", "Quem fala": "Chega mais",
             "A manhã na porta do banco": "A manhã na porta do banco", "O que fizeram com a poupança": "O que fizeram com a poupança",
             "O colchão também confisca": "O colchão também confisca", "Ela tem razão?": "Ela tem razão?",
             "A única coisa que ela faz até hoje": "A única coisa que ela faz até hoje", "A lata, a janela e a vizinha da SUV": "A vizinha da SUV"}
GIF = "foto"
L = {}  # entra depois da voz (os gatilhos sao palavras da fala)
