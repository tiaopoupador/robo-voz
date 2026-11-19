# Cenas do video 05 (longo so motion, a Valeria da SUV). Roteiro: roteiros/05-valeria-da-suv.md.
# 19/11: por enquanto so os pedidos do que o Ed gera a mao (os cenarios vazios e as capas). Os personagens entram por
# codigo (as poses oficiais, render/src/motion/boneco/Turma.tsx); as falas e as cenas (L) vem depois da voz.
# Ed, 19/11: «agora cada video ja vai falar do assunto do proximo»: a Valeria era o 04 e virou o 05 (o 04 e o da Dona Cida, 1990).
IMG = {
 # cenarios VAZIOS (sem ninguem): os personagens entram por cima, animados por codigo
 "meta-rua-noite": ("meta", "rua-casa-suv.jpg", ""),
 "meta-varanda-noite": ("meta", "nenhuma", ""),
 "meta-varanda-domingo": ("meta", "nenhuma", ""),
 "meta-ponto-onibus": ("meta", "nenhuma", ""),
}
VAZIO = (" EMPTY BACKGROUND PLATE for animation: NOBODY in the scene, no people, no faces, no silhouettes, no animals. "
         "Leave the lower middle of the image free and clear, where 2 cartoon characters will be placed later, standing on the ground.")
PEDIDO = {
 "meta-rua-noite": "The SAME street and the SAME house as the attached image (copy the house, the palm trees and the white SUV exactly), "
                   "but at night, 11:40 pm: the whole street dark and asleep, the showy two-story beige house with big dark glass windows, "
                   "the shiny white SUV parked in front catching a little moonlight, and on the right edge of the image a small simple house "
                   "with only ONE warm yellow porch light on. Deep blue night sky, a few stars." + VAZIO,
 "meta-varanda-noite": "A small simple Brazilian house porch at night: a classic porch chair made of woven plastic strings in RED and WHITE "
                       "stripes on a thin silver metal frame, a second identical chair facing it, a tiny wooden side table between them with "
                       "a plain WHITE enamel mug with a small chip on the rim and a flattened brown paper bread bag with a short yellow "
                       "carpenter pencil on it. One bare warm yellow light bulb on the wall, cozy light. Behind, the dark quiet street." + VAZIO,
 "meta-varanda-domingo": "The same small simple Brazilian house porch on a sunny Sunday morning at 9 am: the RED and WHITE striped woven plastic "
                         "porch chair and a second identical chair, a tiny wooden side table with a plain WHITE enamel mug with a small chip "
                         "on the rim, steam rising from it, and a flattened brown paper bread bag. Soft golden morning light, a colorful quiet "
                         "street with small houses behind." + VAZIO,
 "meta-ponto-onibus": "A simple bus stop at the corner of a colorful Brazilian neighborhood street, early morning at 6:30, soft orange sunrise "
                      "light: a small metal bus shelter with a plain blank sign, a bench, a sidewalk, small houses and a bakery with its door "
                      "open in the background." + VAZIO,
}
TITULO = "Por Que a Vizinha da SUV Pediu R$ 50 Emprestado ao Porteiro"
CAPA_TEXTO = "ELA? PEDINDO?!"
PUBLICA = "2026-11-25 18:00"  # Ed 19/11: ordem nova aprovada
PUBLICA_TXT = "quarta, 25/11, às 18h (Brasília, 21h em Lisboa)"
PRAZO = "domingo, 22/11, até as 18h"
PRAZO_ISO = "2026-11-22T18:00:00-03:00"
_V = "valeria-ficha-a.jpg.jpg + tiao-ficha-oficial.jpg"
CAPA = (_V, "Close-up, red dominant colors. LEFT: Valeria, elegant woman, big black sunglasses on her face, spinning the key of a car on her "
            "index finger with a smug disdainful look, nose up. RIGHT: Tiao, calm, holding a plain white enamel mug with a small chip on the "
            "rim, a small knowing smile, one eyebrow up, as if he knows a secret. Behind them, out of focus, a shiny white SUV in front of a "
            "showy beige house at golden hour. Empty space at the top for big title letters.", "valeria-chave")
CAPAS_TESTE = [
 (_V, "Close-up at night, red and dark blue colors. LEFT: Valeria, on tiptoe, sunglasses pushed up on her head, looking sideways as if "
      "checking that nobody is watching, embarrassed, holding a smartphone with a bright screen against her chest. RIGHT: Tiao in a red "
      "and white striped porch chair, holding a plain white chipped mug, eyes wide open in total surprise. A warm yellow porch light. "
      "Empty space at the top for big title letters.", "valeria-noite"),
 (_V, "Close-up, red dominant colors. CENTER: a shiny car key and one folded Brazilian 50 reais banknote side by side, big, in the "
      "foreground. Behind: Valeria with sunglasses on her head, ashamed, covering half of her face with one hand; Tiao beside her, calm, "
      "holding a plain white chipped mug. Empty space at the top for big title letters.", "chave-e-nota"),
]
GIF = "foto"

VAZIOS = {"meta-rua-noite", "meta-varanda-noite", "meta-varanda-domingo", "meta-ponto-onibus"}  # cenarios sem ninguem (pedidos.py)
