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

# ============================ 23/11/2026: as cenas (depois da voz), o 1.o longo SO MOTION ============================
# Cada cena da historia e uma "turma" (render/src/motion/boneco/CenaTurma.tsx): o cenario vazio do meta.ai (banco/imagens/
# cenarios/v05), as poses oficiais da turma (respiram, piscam, falam), o andar e o balao (opcao A: a voz e do Tiao contando,
# o balao mostra a fala do personagem e no lugar dela nao aparece legenda). Os numeros vao em cartoes do kit.
from fabrica.kit import *
VINHETA = 3  # a vinheta entra depois da fala 3 («Vamos começar?»)
DESC = ("Quase meia-noite, a vizinha do carrão de R$ 189.900 bate no portão do porteiro e pede R$ 50 emprestados até sexta. "
        "Dois meses antes, ela tinha rido dele na frente da rua inteira.\n\n"
        "Neste vídeo o Tião conta os dois meses de sinais que ninguém da rua quis ver e faz, no papel de pão, as três contas por trás "
        "daquele carro: a parcela do financiamento (com a taxa do Banco Central), o aluguel da casa de vitrine e o rotativo do cartão, "
        "a conta que engorda até no domingo. E dá as 3 dicas de que a Valéria riu, com o que a lei do Desenrola diz sobre os juros do rotativo.")
TAGS = ["financiamento de carro", "juros do financiamento", "rotativo do cartão", "juros do cartão de crédito", "desenrola", "lei 14.690",
        "carro financiado", "dívida no cartão", "educação financeira", "finanças pessoais", "Tião Poupador"]
PERGUNTA = "Qual é o carro da sua rua que você nunca entendeu como foi pago?"
CAP_NOMES = {"Abertura (é um Reels: entende-se sozinha)": "Três batidinhas no portão", "Quem fala": "Chega mais",
             "Dois meses antes: a chave": "Dois meses antes: a chave", "O bilhete": "O bilhete", "O primeiro mês: os sinais": "Os sinais",
             "O segundo mês: o posto": "O posto", "De volta àquela noite": "O pedido", "Conta número um: a parcela": "Conta 1: a parcela",
             "Conta número dois: a casa de vitrine": "Conta 2: a casa de vitrine", "Conta número três: o cartão": "Conta 3: o cartão",
             "As três dicas": "As dicas de que ela riu", "O que o Tião respondeu": "O que o Tião respondeu", "A dica número três": "A dica número três",
             "O ponto de ônibus": "O ponto de ônibus", "Quatro meses depois": "Quatro meses depois"}
FORTES = {"valéria", "carrão", "parcela", "rotativo", "juros", "desenrola", "cartão", "aluguel", "bilhete", "dica"}
# 24/11 (Ed: «use mais trilhas tipo de cinema»): o clima troca a cada 2 ou 3 min (novela.md, regra 11)
CLIMA = {0: "tensao", 4: "calma", 7: "humor", 11: "drama", 14: "reflexiva", 17: "calma", 18: "curiosa", 22: "tensao", 24: "drama",
         28: "tensao", 33: "reflexiva", 45: "drama", 49: "triste", 50: "reflexiva", 56: "calma", 60: "reflexiva", 64: "calma",
         68: "drama", 72: "virada", 73: "virada", 76: "final", 80: "reflexiva", 81: "curiosa", 82: "tensao"}
AMB = [("grilos", 0, "^", 14, 0.22), ("passaros", 4, "^", 14, 0.2), ("passaros", 7, "^", 30, 0.2), ("grilos", 14, "^", 30, 0.2),
       ("passaros", 18, "^", 20, 0.2), ("grilos", 21, "^", 14, 0.2), ("grilos", 26, "^", 25, 0.2), ("grilos", 29, "^", 30, 0.2),
       ("grilos", 56, "^", 30, 0.18), ("passaros", 64, "^", 20, 0.2), ("passaros", 68, "^", 16, 0.2), ("passaros", 73, "^", 16, 0.2),
       ("passaros", 76, "^", 20, 0.2), ("grilos", 80, "^", 16, 0.18), ("passaros", 81, "^", 16, 0.2)]

F = "banco:cenarios/v05/"
LV = {"tipo": "varanda", "lado": 1, "forca": 0.7}   # de noite, a lampada da varanda do Tiao
LN = {"tipo": "noite", "forca": 0.85}                # a rua apagada
def P(pid, x, y, alt, *poses, **kw):
    """um personagem: poses = ("COD", "palavra" ou None para ja estar)"""
    return {"pid": pid, "x": x, "y": y, "alt": alt, "poses": [{"cod": c, **({"g": g} if g else {"ini": 0})} for c, g in poses], **kw}
def B(texto, quem, g, ate=None, x=330, y=28, larg=1060, rabo=(740, 470)):
    b = {"texto": texto, "quem": quem, "g": g, "x": x, "y": y, "larg": larg, "rabo": list(rabo)}
    if ate: b["ate"] = ate
    return b
def T(fundo, gente, baloes=(), **kw): return {"k": "turma", "fundo": F + fundo, "gente": list(gente), "baloes": list(baloes), **kw}
CARRO = {"src": F + "carrao.png", "x": 1060, "y": 890, "w": 840, "frente": "esq"}  # a frente do carro olha para a esquerda
def rua_dia(gente=(), baloes=(), carro=True, anda_carro=None, **kw):
    return T("rua-sem-carro.jpg", gente, baloes, objetos=[dict(CARRO, **(anda_carro or {}))] if carro else [], zoom=[1.0, 1.06], **kw)
def rua_noite(gente=(), baloes=(), **kw): return T("rua-noite.jpg", gente, baloes, luz=LN, zoom=[1.0, 1.08], fx=70, **kw)
def noite_larga(gente=(), baloes=(), **kw): return T("varanda-noite.jpg", gente, baloes, **{"luz": LV, "lampada": {"x": 970, "y": 150, "r": 760}, "zoom": [1.0, 1.07], "fy": 55, **kw})
def noite_perto(gente=(), baloes=(), **kw): return T("varanda-noite-perto.jpg", gente, baloes, **{"luz": LV, "lampada": {"x": 960, "y": 180, "r": 700}, "zoom": [1.0, 1.05], **kw})
def dom_larga(gente=(), baloes=(), **kw): return T("varanda-domingo.jpg", gente, baloes, **{"zoom": [1.0, 1.07], "fx": 35, "fy": 60, **kw})
def dom_perto(gente=(), baloes=(), **kw): return T("varanda-domingo-perto.jpg", gente, baloes, **{"zoom": [1.0, 1.05], **kw})
def ponto(gente=(), baloes=(), perto=False, **kw): return T("ponto-perto.jpg" if perto else "ponto.jpg", gente, baloes, zoom=[1.0, 1.06], **kw)
def foco(fundo, fx, fy, z=1.3, **kw): return T(fundo, [], **{"zoom": [1.0, z], "fx": fx, "fy": fy, **kw})  # a camera chega perto de um objeto do cenario
# enquadramentos que se repetem
def VE(*poses, x=600, **kw): return P("valeria", x, 1290, 1060, *poses, **kw)    # Valeria de perto (da cintura para cima)
def TI(*poses, x=1480, **kw): return P("tiao", x, 1290, 1040, *poses, **kw)      # Tiao de perto
VD = dict(x=760, y=40, larg=1080, rabo=(1180, 470))       # balao de quem esta sozinho, a direita
BT = dict(x=860, larg=1030, rabo=(1290, 560))            # balao do Tiao (ele a direita, a Valeria a esquerda)
def TS_N(*ps): return P("tiao", 690, 690, 520, *(ps or (("P16", None),)))      # sentados na varanda de noite (ele a esquerda, ela a direita)
def VS_N(*ps): return P("valeria", 1235, 690, 520, *(ps or (("P17", None),)))
def TS_D(*ps): return P("tiao", 400, 700, 470, *(ps or (("P16", None),)))      # sentados na varanda de domingo
def VS_D(*ps): return P("valeria", 870, 700, 470, *(ps or (("P17", None),)))
def chega_noite(): return rua_noite([P("valeria", 1450, 985, 560, ("R1", None), anda={"de": -250, "g": "chega", "dur": 3.2, "oculos": True})])
def pede():
    return noite_perto([VE(("P09", None), ("P10", "Tião")), TI(("P05", None), ("P14", "sexta"))],
                       [B("Tião... você me empresta cinquenta reais até sexta?", 0, "Tião", "sexta")])
def conta(titulo, linhas, total="Sobra", neutro=False, passo=0.9):
    return {"k": "conta", "titulo": titulo, "linhas": [{"rotulo": a, "valor": b} for a, b in linhas], "total": total, "neutro": neutro, "passo": passo}
def cel(titulo, linhas, destaque=()): return {"k": "celular", "titulo": titulo, "linhas": [{"r": a, "v": b, **({"pos": True} if p else {})} for a, b, p in linhas], "destaque": list(destaque)}
CANECA_D, PAPEL_N = ("varanda-domingo-perto.jpg", 40, 45), ("varanda-noite-perto.jpg", 58, 45)

# ======================= 24/11/2026: a versao NOVELA (roteiros/escaleta-05-nova.md, 84 falas) =======================
# Ed: «parece uma historia muito superficial». Dois meses de sinais, a humilhacao em publico, o bilhete, o posto, a Sandra
# que quer uma SUV igual, as 3 dicas. As poses novas (Team: tiao-v05-novela) entram quando chegam; ate la, a parecida.
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)) + "/../../.."
def ps(pid, novo, velho):
    """a pose nova se ja foi recortada, senao a que ja existe"""
    return novo if _os.path.exists(f"{_R}/render/public/boneco/turma/{pid}/{novo}.png") else velho
def _tem(fundo): return _os.path.exists(f"{_R}/banco/imagens/cenarios/v05/{fundo}")
def GE(pid, *poses, x=960, **kw): return P(pid, x, 1290, 1060, *poses, **kw)   # qualquer um da turma, de perto
def DE(pid, x, **kw): return P(pid, x, 960, 600, ("R1", None), **kw)           # de corpo inteiro na rua
def RODA(): return [DE("marcos", 300), DE("sandra", 480), DE("rafa", 1720)]     # a rua na calcada, longe do carrao
def posto(gente=(), baloes=(), **kw):
    return T("posto.jpg", gente, baloes, zoom=[1.0, 1.06], **kw) if _tem("posto.jpg") else rua_dia(gente, baloes, carro=False, **kw)
def portao():
    return T("portao-bilhete.jpg", [], luz=LV, zoom=[1.0, 1.3], fx=50, fy=86) if _tem("portao-bilhete.jpg") else foco(*PAPEL_N, luz=LV)
def casa_luz(): return rua_noite(lampada={"x": 650, "y": 360, "r": 300})       # acende o quarto dela, na casa de vidro
def chega(g): return rua_noite([P("valeria", 1450, 985, 560, ("R1", None), anda={"de": -250, "g": g, "dur": 3.2, "oculos": True})])
def pedido(): return [("^", "M", rua_noite()), ("Só a luz", "M", noite_larga([TS_N()])), ("três batidinhas", "M", chega("três batidinhas")),
                      ("falou baixinho", "M", pede())]
V_ZOMBA, V_CARTAO, V_FINGE, V_BILHETE = ps("valeria", "P19", "P12"), ps("valeria", "P23", "P11"), ps("valeria", "P22", "P13"), ps("valeria", "P21", "P09")
T_HUMILHADO, T_BILHETE = ps("tiao", "P19", "P13"), ps("tiao", "P18", "P09")

L = {
 # 0. Abertura (Reels)
 0: pedido(),
 1: [("^", "M", nu(50, "Emprestados até sexta", "pedido de quem desceu de um carrão de R$ 189.900", cor=VERM, fmt="int", suf=" reais", emoji="🤫")),
     ("Dois meses antes", "M", rua_dia([VE((V_ZOMBA, None), x=700)])), ("na noite daquele", "M", rua_noite([VE((V_BILHETE, None), x=1350)], lampada={"x": 650, "y": 360, "r": 300})),
     ("por baixo do meu portão", "M", portao())],
 2: [("^", "M", ic([("✉️", "o que dizia o bilhete", False), ("🚗", "as três contas por trás do carrão", False), ("🤐", "o que eu respondi", False)], "Hoje")),
     ("Essa última", "M", noite_perto([TI(("P10", None), x=960)]))],
 3: [("^", "M", rua_dia([TI(("P03", None), x=450)])), ("fica comigo", "M", dom_perto([TI(("P06", None), x=960)])), ("puxa a cadeira", "M", dom_larga())],
 # 1. Quem fala
 4: [("^", "M", dom_perto([TI(("P08", None), x=960)]))],
 5: [("^", "M", dom_perto([TI(("P06", None), ("P07", "porteiro"), x=1250)])), ("Nem sempre", "M", dom_perto([TI(("P10", None), x=1250)])),
     ("Tomo café", "M", foco(*CANECA_D)), ("papel de pão", "M", dom_larga([TS_D(("P17", None))]))],
 6: [("^", "M", rua_noite([GE("cida", ("P04", None), x=700)], [B("Essa moça ainda vai bater na sua porta.", 0, "me avisou", "porta")])),
     ("Bateu", "M", noite_perto([VE(("P09", None), x=960)])), ("voltar dois meses", "M", fr("*Dois meses* antes"))],
 # 2. Dois meses antes: a chave
 7: [("^", "M", rua_dia(carro=False)), ("o Marcos", "M", rua_dia(RODA(), carro=False)), ("a Dona Cida", "M", rua_dia([GE("cida", ("P02", None), x=1500)], carro=False)),
     ("Eu na minha varanda", "M", dom_larga([TS_D()])), ("E aí ela chegou", "M", rua_dia(RODA(), anda_carro={"de": 2900, "g": "chegou", "dur": 6.0}))],
 8: [("^", "M", rua_dia([P("valeria", 1640, 960, 600, ("R1", None))])), ("Ela gerencia", "M", rua_dia([VE(("P01", None), x=1300)])),
     ("desceu", "M", rua_dia([VE(("P05", None), x=1450)]))],
 9: [("^", "M", rua_dia([VE(("P07", None), x=1250)], [B("R$ 189.900, gente. Peguei ontem.", 0, "Cento", "ontem", **VD)]))],
 10: [("^", "M", rua_dia([GE("sandra", ("P02", None))])), ("O Marcos", "M", rua_dia([GE("marcos", ("P07", None))])),
      ("E eu, que", "M", dom_perto([TI(("P05", None), x=960)])),
      ("para quem compra", "M", dom_perto([TI(("P09", None), x=960)], [B("Valéria, para quem compra carro assim, eu tenho três dicas.", 0, "para quem compra", "dicas")]))],
 11: [("^", "M", rua_dia([VE((V_ZOMBA, None), x=700)])),
      ("Dica de porteiro", "M", rua_dia([VE((V_ZOMBA, None), x=700)], [B("Dica de porteiro, gente!", 0, "Dica de", "gente"),
                                                                       B("Quem vai de ônibus vai me ensinar a comprar carro!", 0, "Quem vai", "carro")]))],
 12: [("^", "M", foco(*CANECA_D)),
      ("Ai, Tião", "M", rua_dia([VE(("P06", None), ("P02", "Compra"), x=1250)], [B("Ai, Tião... que pobreza. Essa caneca tem a idade da rua.", 0, "Ai", "rua", **VD),
                                                                                  B("Compra uma nova, homem, que eu até te dou o dinheiro.", 0, "Compra", "dinheiro", **VD)]))],
 13: [("^", "M", rua_dia(RODA())), ("E quem riu", "M", rua_dia([GE("sandra", ("P01", None))])), ("Eu ri junto", "M", dom_perto([TI((T_HUMILHADO, None), x=960)])),
      ("dentro da caneca", "M", foco(*CANECA_D)), ("fiquei ali", "M", dom_perto([TI(("P13", None), x=960)]))],
 # 3. O bilhete
 14: [("^", "M", noite_larga([TS_N()])), ("vi um papel", "M", portao()), ("Eu conheço", "M", noite_perto([TI((T_BILHETE, None), x=960)]))],
 15: [("^", "M", fr("*Desculpa por hoje.*", "Não conta pra ninguém que eu pedi desculpa.")), ("Sem nome", "M", noite_perto([TI((T_BILHETE, None), x=960)]))],
 16: [("^", "M", noite_perto([TI(("P10", None), x=960)])), ("E olhei pela janela", "M", casa_luz()), ("Guarda esse bilhete", "M", noite_perto([TI(("P10", None), x=960)]))],
 17: [("^", "M", noite_perto([TI(("P06", None), x=960)])), ("deixa o like", "M", {"k": "botao", "tipo": "like", "texto": "Deixa o like"}),
      ("se inscreve", "M", {"k": "botao", "tipo": "inscrever", "texto": "E se inscreve"}),
      ("conta aqui embaixo", "M", fr("Qual carro da *sua rua* ninguém entende como foi pago?", "escreve aqui embaixo, eu leio e respondo"))],
 # 4. O primeiro mes: os sinais
 18: [("^", "M", fr("O *primeiro* mês")), ("Eu saio", "M", dom_perto([TI(("P07", None), x=960)])),
      ("eu vi a Valéria", "M", rua_dia([P("valeria", 1700, 960, 600, ("R1", None), anda={"de": 400, "g": "saindo de casa", "dur": 5.0, "oculos": True})])),
      ("O carrão ficou", "M", rua_dia())],
 19: [("^", "M", ponto([P("valeria", 900, 860, 600, ("R1", None))])),
      ("Quando a Sandra", "M", rua_dia([GE("sandra", ("P05", None), x=600), GE("valeria", ("P12", None), x=1480)], [B("Está na revisão.", 1, "Está na", "revisão", **BT)])),
      ("Carro zerinho", "M", dom_perto([TI(("P03", None), x=960)]))],
 20: [("^", "M", rua_dia([GE("sandra", ("P06", None))])),
      ("que fazia escova", "M", ic([("💇", "escova de 15 em 15 dias", True), ("🔒", "cabelo preso, três sábados seguidos", False)], "O que a Sandra reparou")),
      ("E a casa de vidro", "M", casa_luz()), ("passou a apagar", "M", rua_noite())],
 21: [("^", "M", rua_noite()), ("Tião, eu te falei", "M", rua_noite([GE("cida", ("P04", None), x=700)], [B("Tião, eu te falei. Carro parado e dona indo de ônibus.", 0, "Tião, eu", "ônibus"),
                                                                                                  B("Isso não é revisão, meu filho. Isso é parcela.", 0, "Isso não", "parcela")]))],
 22: [("^", "M", rua_dia([GE("sandra", ("P04", None))])),
      ("Se a Valéria pode", "M", rua_dia([GE("sandra", ("P05", None), x=600), GE("marcos", ("P07", None), x=1480)],
                                          [B("Se a Valéria pode ter uma SUV, a gente também pode.", 0, "Se a Valéria", "também pode"),
                                           B("A gente troca essa picape. Sábado eu quero ir na concessionária.", 0, "A gente troca", "concessionária")]))],
 23: [("^", "M", dom_perto([TI(("P04", None), x=960)])), ("Sem saber", "M", fr("A Sandra quer entrar no *mesmo buraco*", "sem saber de nada"))],
 # 5. O segundo mes: o posto
 24: [("^", "M", fr("O *segundo* mês")), ("tirou o carro", "M", rua_dia(anda_carro={"de": 1060, "x": -900, "g": "tirou o carro", "dur": 6.0})),
      ("na fila do posto", "M", posto()), ("era o Rafa", "M", posto([GE("rafa", ("P01", None))]))],
 25: [("^", "M", cel("Maquininha do posto", [("Cartão", "recusado", False)], [0])),
      ("Passou de novo", "M", cel("Maquininha do posto", [("Cartão", "recusado", False), ("De novo", "recusado", False)], [0, 1])),
      ("A Valéria tirou", "M", posto([VE((V_CARTAO, None), x=960)])),
      ("Essa maquininha", "M", posto([VE(("P12", None), x=960)], [B("Essa maquininha de vocês está com defeito.", 0, "Essa maquininha", "defeito")])),
      ("E saiu do posto", "M", posto([GE("rafa", ("P03", None))]))],
 26: [("^", "M", noite_perto([GE("rafa", ("P02", None), x=600), TI(("P05", None))])),
      ("Primo, a madame", "M", noite_perto([GE("rafa", ("P02", None), x=600), TI(("P05", None))], [B("Primo, a madame da SUV não tem nem para a gasolina!", 0, "Primo, a", "gasolina")])),
      ("Amanhã a rua", "M", noite_perto([GE("rafa", ("P01", None), x=600), TI(("P04", None))], [B("Amanhã a rua inteira vai saber. Eu vou contar para a Sandra!", 0, "Amanhã", "Sandra")]))],
 27: [("^", "M", noite_perto([GE("rafa", ("P04", None), x=600), TI(("P07", None))], [B("Rafa, não conta. Quem já levou um não na frente de todo mundo sabe o tamanho disso.", 1, "Rafa, não", "disso", **BT)])),
      ("Ele parou de rir", "M", noite_perto([GE("rafa", ("P04", None))])), ("E foi embora", "M", noite_larga([TS_N()]))],
 # 6. De volta aquela noite
 28: [("^", "M", noite_perto([TI(("P10", None), x=960)])), ("Uma semana", "M", fr("*Uma semana* depois do posto"))],
 29: pedido(),
 30: [("^", "M", noite_perto([VE(("P08", None), x=960, treme=[{"g": "apitou", "dur": 0.6}])])),
      ("Sua fatura", "M", cel("Cartão de crédito", [("Sua fatura vence", "segunda", False), ("Valor", "R$ 3.200", False)], [1]))],
 31: [("^", "M", noite_perto([VE(("P10", None)), TI(("P05", None))], [B("É só para a gasolina, Tião. Eu preciso ir trabalhar segunda.", 0, "É só", "segunda")])),
      ("Eu sei que", "M", noite_perto([VE(("P11", None)), TI(("P13", None))], [B("Eu sei que não tenho o direito de te pedir nada, depois daquele sábado.", 0, "Eu sei", "sábado")])),
      ("Mas a sua luz", "M", noite_perto([VE(("P01", None)), TI(("P03", None))], [B("Mas a sua luz é a única acesa. E você nunca me perguntou do carro.", 0, "Mas a sua", "carro")]))],
 32: [("^", "M", noite_larga([TS_N(), P("valeria", 1350, 930, 640, ("R1", None))],
                            [B("Senta aí, Valéria. Antes dos cinquenta, deixa eu te mostrar uma coisa.", 0, "Senta", "coisa", x=520, y=30, larg=1000, rabo=(720, 290))])),
      ("papel de pão", "M", foco(*PAPEL_N, luz=LV))],
 # 7. Conta numero um: a parcela
 33: [("^", "M", fr("Conta número *1*: a parcela")), ("Ela contou", "M", noite_larga([TS_N(("P17", None)), VS_N()])),
      ("Deu o carro antigo", "M", conta("O carrão", [("Preço", 189900), ("Carro antigo, de entrada", -30000)], "Financiado", neutro=True, passo=1.8)),
      ("sessenta meses", "M", nu(60, "Parcelas", "cinco anos pagando", cor=VERM, fmt="int", suf=" meses", emoji="📅"))],
 34: [("^", "M", noite_perto([TI(("P05", None), x=960)])), ("Em setembro", "M", nu(1.96, "Juros médios do financiamento de carro, ao mês", "Banco Central, setembro", cor=VERM, fmt="num", casas=2, suf="%", emoji="🏦")),
      ("No ano", "M", nu(26, "No ano", "Banco Central, setembro", cor=VERM, fmt="int", suf="%", emoji="📈"))],
 35: [("^", "M", nu(4555.56, "A parcela da Valéria", "todo mês", cor=VERM, casas=2, emoji="🚗")),
      ("Todo mês", "M", {"k": "grade", "total": 60, "cols": 12, "titulo": "60 parcelas", "cor": VERM, "rotuloFim": "cinco anos"}),
      ("já tinha pagado", "M", fr("Já tinha pagado *2* de 60"))],
 36: [("^", "M", ba([("Emprestado", 159900, AZUL), ("Ela vai pagar", 273333, VERM)], "Somando as 60 parcelas")),
      ("São cento e treze", "M", nu(113433, "Só de juros", "mais da metade de outro carrão", cor=VERM, emoji="🏦"))],
 37: [("^", "M", noite_perto([VE(("P03", None)), TI(("P05", None))], [B("Cento e treze mil, Tião?! Isso é mentira.", 0, "Cento", "mentira")])),
      ("O vendedor", "M", noite_perto([VE(("P04", None)), TI(("P05", None))], [B("O vendedor falou que a parcela cabia no meu bolso!", 0, "O vendedor", "bolso")]))],
 38: [("^", "M", noite_perto([TI(("P07", None), x=960)])), ("Esse dinheiro", "M", fr("Esse dinheiro *criou perna*!"))],
 39: [("^", "M", noite_perto([TI(("P11", None), x=960)])), ("o financiamento de carro", "M", nu(48, "Prazo médio do financiamento de carro", "Banco Central, setembro", cor=VERM, fmt="int", suf=" meses", emoji="📅")),
      ("Quatro anos", "M", rua_dia())],
 # 8. Conta numero dois: a casa de vitrine
 40: [("^", "M", fr("Conta número *2*: a casa")),
      ("Eu achava", "I", (F + "rua-sem-carro.jpg", [dict(cb("ALUGADA", 50, 40, VERM), g="alugada")])), ("Três mil e novecentos", "M", nu(3900, "Aluguel, por mês", "fora a luz", cor=VERM, emoji="🏠")),
      ("Agora eu entendia", "M", rua_noite())],
 41: [("^", "M", noite_larga([TS_N(("P17", None)), VS_N()])),
      ("já com os descontos", "M", conta("O mês da Valéria", [("Salário, já com os descontos", 8700), ("Parcela do carro", -4555.56), ("Aluguel", -3900)], passo=2.4))],
 42: [("^", "M", nu(244.44, "Sobra para o mês inteiro", "depois da parcela e do aluguel", cor=VERM, casas=2, emoji="😬")),
      ("Para comida", "M", ic([("🍚", "comida", False), ("⛽", "gasolina", False), ("💡", "luz", False), ("📱", "celular", False)], "Com R$ 244")),
      ("Foi por isso", "M", rua_dia()), ("Não era revisão", "M", fr("Não era revisão. Era a *gasolina* que não cabia."))],
 43: [("^", "M", cel("Mensagem do Rafa", [("Rafa", "não contei para ninguém", True), ("Rafa", "nem para a Sandra", True)], [0])),
      ("Eu não mostrei", "M", noite_perto([TI(("P10", None), x=960)]))],
 44: [("^", "M", noite_perto([VE(("P01", None)), TI(("P05", None))], [B("Mas eu nunca fiquei sem nada, Tião. O cartão segura até o outro mês.", 0, "Mas eu", "outro mês")])),
      ("E aí ela mesma", "M", noite_perto([VE(("P08", None), x=960)]))],
 # 9. Conta numero tres: o cartao
 45: [("^", "M", fr("Conta número *3*: o cartão")), ("O almoço", "M", ic([("🍽️", "o almoço", False), ("⛽", "a gasolina", False), ("💇", "o salão", False), ("👗", "a roupa nova", False)], "Tudo no cartão")),
      ("Até o cartão", "M", posto([VE((V_CARTAO, None), x=960)])),
      ("E a fatura chegou", "M", cel("Cartão de crédito", [("Fatura", "R$ 3.200", False), ("Na conta", "não tem", False)], [0]))],
 46: [("^", "M", noite_perto([VE(("P04", None), x=960)])), ("só o mínimo", "M", cel("Cartão de crédito", [("Pagou", "só o mínimo", False)], [0])),
      ("Sabe para onde", "M", noite_perto([TI(("P05", None), x=960)])), ("Para o rotativo", "M", fr("O resto vai para o *rotativo*", "um dos dinheiros mais caros do banco"))],
 47: [("^", "M", nu(15.29, "Juros médios do rotativo do cartão, ao mês", "Banco Central, setembro", cor=VERM, fmt="num", casas=2, suf="%", emoji="🔥")),
      ("No ano", "M", nu(450, "No ano, passa de", "Banco Central, setembro", cor=VERM, fmt="int", suf="%", emoji="🔥"))],
 48: [("^", "M", nu(489, "Juros só no primeiro mês", "R$ 3.200 a 15% ao mês", cor=VERM, emoji="📈")),
      ("Em três meses", "M", ba([("Hoje", 3200, AMAR), ("Em 3 meses sem pagar", 4904, VERM)], "A fatura no rotativo")),
      ("É essa a conta", "M", noite_perto([VE(("P04", None), x=960)]))],
 49: [("^", "M", noite_perto([VE(("P04", None), x=960)])), ("Pôs os óculos", "M", noite_perto([VE(("P14", None), x=960)])),
      ("me escreve", "M", fr("Fatura que não cabe? Escreve aqui embaixo: *eu também*")), ("Você não está", "M", noite_perto([TI(("P13", None), x=960)]))],
 # 10. As tres dicas
 50: [("^", "M", noite_larga([TS_N(), VS_N()])), ("lembrei daquele sábado", "M", rua_dia([VE((V_ZOMBA, None), x=700)])),
      ("lembra das três", "M", noite_perto([VE(("P11", None)), TI(("P05", None))], [B("Valéria... lembra das três dicas de que você riu?", 1, "lembra das", "riu", **BT)]))],
 51: [("^", "M", noite_perto([VE(("P11", None)), TI(("P05", None))])),
      ("Tião, eu sei", "M", noite_perto([VE(("P10", None)), TI(("P06", None))], [B("Tião, eu sei que é besteira de porteiro... mas fala.", 0, "Tião, eu sei", "fala"),
                                                                              B("Eu não tenho mais nada a perder.", 0, "Eu não tenho", "perder")]))],
 52: [("^", "M", fr("*Dica 1*", "pergunte o total, não a parcela")), ("É só multiplicar", "M", fr("Parcela *×* número de parcelas", "= o que você paga de verdade")),
      ("O vendedor mostra", "M", noite_perto([TI(("P09", None), x=960)]))],
 53: [("^", "M", fr("*Dica 2*", "fatura que não cabe nunca fica no mínimo")),
      ("Liga para o banco", "M", cel("Cartão de crédito", [("Parcelar a fatura", "em 3 vezes", True), ("Só o mínimo", "nunca", False)], [0])),
      ("E tem uma lei", "M", noite_perto([TI(("P06", None), x=960)]))],
 54: [("^", "M", noite_perto([TI(("P09", None), x=960)])), ("Está no site", "M", fr("Lei *14.690*, de 2023 (Desenrola)", "site oficial da Câmara dos Deputados")),
      ("Ela diz que", "M", fr("Juros do rotativo: no máximo *o tamanho da dívida*", "Lei 14.690/2023, art. 28")),
      ("Três mil e duzentos viram", "M", ba([("A dívida", 3200, AMAR), ("O máximo, com os juros", 6400, VERM)], "A dívida pode, no máximo, dobrar")),
      ("Se o banco", "M", noite_perto([TI(("P06", None), x=960)]))],
 55: [("^", "M", fr("*Dica 3*", "fica para o fim: é a que dói")), ("Mas antes", "M", noite_perto([TI(("P07", None), x=960)]))],
 # 11. O que o Tiao respondeu
 56: [("^", "M", noite_larga([TS_N(), VS_N()], zoom=[1.0, 1.15]))],
 57: [("^", "M", noite_perto([VE(("P04", None)), TI(("P03", None))], [B("Cinquenta para gasolina eu não te empresto.", 1, "Valéria", "empresto", **BT)])),
      ("Porque", "M", noite_perto([VE(("P14", None)), TI(("P07", None))], [B("Segunda você vai precisar de mais cinquenta. E o carro continua comendo R$ 4.500 por mês.", 1, "Porque", "mês", **BT)]))],
 58: [("^", "M", noite_larga([TS_N(), P("valeria", 1350, 930, 640, ("R1", None), sai={"ate": 2300, "g": "levantou", "dur": 4.0, "oculos": True})]))],
 59: [("^", "M", noite_perto([VE(("P03", None)), TI(("P05", None))], [B("Mas o cartão do ônibus da semana eu pago.", 1, "Mas o cartão", "pago", **BT)])),
      ("E segunda", "M", noite_perto([VE(("P03", None)), TI(("P06", None))], [B("E segunda, seis e meia, eu vou junto com você até o ponto.", 1, "E segunda", "ponto", **BT)])),
      ("E domingo", "M", noite_perto([VE(("P01", None)), TI(("P09", None))], [B("Domingo a gente senta aqui, com café, e eu te dou a dica número três.", 1, "E domingo", "três", **BT)]))],
 60: [("^", "M", noite_perto([VE(("P16", None), x=960)])),
      ("Por que você", "M", noite_perto([VE(("P15", None)), TI(("P05", None))], [B("Por que você faz isso por mim, Tião? Depois de tudo?", 0, "Por que", "tudo")])),
      ("Eu não respondi", "M", noite_perto([TI(("P10", None), x=960)])), ("Ela abriu a boca", "M", noite_perto([VE(("P16", None), x=960)]))],
 61: [("^", "M", rua_noite([P("valeria", 1450, 985, 560, ("R1", None), sai={"ate": 680, "g": "atravessou", "dur": 4.5, "oculos": True})])),
      ("Um minuto depois", "M", casa_luz())],
 62: [("^", "M", noite_perto([TI(("P10", None), x=960)]))],
 63: [("^", "M", noite_perto([TI(("P09", None), x=960)])), ("usa o FinMoovi", "V", "banco:FM:1-cartoes/cartoes__estilo-moldura-celular__horizontal.mp4"),
      ("São sete dias", "M", nu(7, "Dá para testar o FinMoovi", "link na descrição", cor=VERDE, fmt="int", suf=" dias", emoji="📱"))],
 # 12. A dica numero tres
 64: [("^", "M", dom_larga([TS_D(), P("valeria", 1300, 950, 620, ("R1", None), anda={"de": 2300, "g": "ela apareceu", "dur": 3.2, "oculos": True})])),
      ("Eu passei o café", "M", foco(*CANECA_D)), ("E dei a dica", "M", dom_perto([TI(("P09", None), x=960)]))],
 65: [("^", "M", fr("*Dica 3*", "a pergunta que ninguém faz")),
      ("Quanto esse carro", "M", dom_perto([VE(("P04", None)), TI(("P05", None))], [B("Quanto esse carro vale hoje, e quanto eu ainda devo dele?", 1, "Quanto esse", "dele", **BT)])),
      ("Se vendendo", "M", fr("Vendendo dá para quitar? O carro é *seu*.", "Se não dá, quem manda nele é o banco."))],
 66: [("^", "M", dom_larga([TS_D(("P17", None)), VS_D(("P18", None))])), ("vendendo agora", "M", dom_perto([VE(("P03", None), x=960)])),
      ("Mas a parcela", "M", nu(4555.56, "A parcela do carro", "sumia", cor=VERDE, casas=2, emoji="✅"))],
 67: [("^", "M", dom_perto([VE(("P07", None), x=960)])), ("Depois empurrou", "M", dom_perto([VE(("P10", None)), TI(("P05", None))], [B("Me ajuda a vender, Tião.", 0, "Me ajuda", "Tião")]))],
 # 13. O ponto de onibus
 68: [("^", "M", ponto([P("tiao", 700, 860, 560, ("R1", None)), P("valeria", 980, 860, 600, ("R1", None))])),
      ("A Sandra abriu", "M", ponto([GE("sandra", ("P04", None))], perto=True))],
 69: [("^", "M", ponto([GE("sandra", ("P01", None))], [B("Valéria?! De ônibus? Com o porteiro?", 0, "Valéria", "porteiro")], perto=True)),
      ("E riu alto", "M", ponto([GE("sandra", ("P02", None))], perto=True))],
 70: [("^", "M", ponto([P("tiao", 700, 860, 560, ("R1", None)), P("valeria", 980, 860, 600, ("R1", None), sai={"ate": 1300, "g": "Deu um passo", "dur": 1.6, "oculos": True})])),
      ("levantou o queixo", "M", ponto([VE((V_FINGE, None), x=960)], [B("Ele só está me mostrando o ponto.", 0, "Ele só", "ponto")], perto=True)),
      ("Como se eu", "M", ponto([TI((T_HUMILHADO, None), x=960)], perto=True))],
 71: [("^", "M", ponto()), ("E fui para a portaria", "M", ponto([P("tiao", 700, 860, 560, ("R1", None), sai={"ate": -300, "g": "E fui", "dur": 4.0})])),
      ("Doeu mais", "M", ponto([TI(("P13", None), x=960)], perto=True))],
 72: [("^", "M", rua_dia(anda_carro={"de": 1060, "x": -900, "g": "dirigiu", "dur": 6.0})), ("A rua inteira viu", "M", rua_dia(carro=False)),
      ("a Dona Cida", "M", rua_dia([GE("cida", ("P04", None), x=700)], [B("Era a parcela, minha filha. Quatro mil e quinhentos por mês.", 0, "Era a parcela", "mês")], carro=False)),
      ("o Marcos perguntou", "M", rua_dia([GE("sandra", ("P07", None), x=600), GE("marcos", ("P06", None), x=1480)],
                                         [B("E a concessionária, sábado?", 1, "E a concessionária", "sábado", **BT)], carro=False)),
      ("A Sandra olhou", "M", rua_dia([GE("sandra", ("P06", None), ("P07", "Deixa a picape"))], [B("Deixa a picape onde está.", 0, "Deixa a picape", "está")], carro=False))],
 # 14. Quatro meses depois (o final de que o Ed gostou)
 73: [("^", "M", fr("*Quatro meses* depois")), ("Outro sábado", "M", rua_dia(carro=False)),
      ("a garagem vazia", "I", (F + "rua-sem-carro.jpg", [pl("ALUGA-SE", 28, 62, cor=VERM, tam=64)]))],
 74: [("^", "M", ic([("🚗", "financiamento quitado", False), ("🏠", "casa menor", False), ("💳", "fatura em 3 vezes", False), ("🚌", "de ônibus", False)], "Quatro meses depois")),
      ("Parcelou a fatura", "M", cel("Cartão de crédito", [("Fatura parcelada", "3 vezes", False), ("Só o mínimo", "nunca mais", False)], [0])),
      ("E vai de ônibus", "M", ponto([P("valeria", 900, 860, 600, ("R1", None))]))],
 75: [("^", "M", rua_dia([P("valeria", 2300, 960, 600, ("R1", None), anda={"de": -300, "g": "comentou", "dur": 7.0, "oculos": True})], carro=False,
                       baloes=[{"texto": "A Valéria quebrou.", "g": "A Valéria quebrou", "ate": "quebrou", "x": 560, "y": 60, "larg": 800}])),
      ("Ela ri", "M", rua_dia([VE(("P12", None), x=1250)], carro=False)), ("Ninguém da rua", "M", rua_dia([VE(("P15", None), x=1250)], carro=False))],
 76: [("^", "M", dom_larga([TS_D(), P("valeria", 1300, 950, 620, ("R1", None), anda={"de": 2300, "g": "passagem", "dur": 3.0, "oculos": True})])),
      ("Tirou da bolsa", "M", nu(50, "Dentro da caneca", "dobrada em quatro", cor=VERDE, fmt="int", suf=" reais", emoji="💵")),
      ("A mesma caneca", "M", foco(*CANECA_D))],
 77: [("^", "M", dom_perto([VE(("P02", None), x=1250)], [B("Para você comprar uma caneca nova, Tião!", 0, "Para você", "Tião", **VD)]))],
 78: [("^", "M", dom_perto([TI(("P08", None), x=960)])), ("Caneca velha", "M", fr("Caneca velha, *bolso cheio*!"))],
 79: [("^", "M", rua_dia([P("valeria", 900, 960, 600, ("R1", None), sai={"ate": 2400, "g": "foi embora", "dur": 4.0, "oculos": True})], carro=False))],
 80: [("^", "M", noite_perto([TI((T_BILHETE, None), x=960)])),
      ("Dentro dela", "M", rua_noite([VE((V_BILHETE, None), x=1350)], lampada={"x": 650, "y": 360, "r": 300})),
      ("A desculpa daquele", "M", fr("A desculpa daquele sábado, e a do ponto, eu ainda te devo *em voz alta*.")),
      ("Eu guardei junto", "M", noite_perto([TI(("P10", None), x=960)])), ("Ela ainda não pediu", "M", noite_larga([TS_N()]))],
 81: [("^", "M", dom_perto([TI(("P06", None), x=960)])), ("escreve aqui embaixo", "M", fr("Vai fazer a sua conta hoje? Escreve aqui embaixo:", "*eu vou fazer a conta*")),
      ("E fica mais", "M", dom_perto([TI(("P10", None), x=960)]))],
 82: [("^", "M", dom_larga([TS_D(), VS_D()])),
      ("o extrato", "M", cel("Extrato da conta do salário", [("Salário", "+ R$ 8.700", True), ("Aluguel", "- R$ 3.900", False), ("Cartão", "- R$ 3.200", False), ("? ? ? ? ?", "- R$ ? ? ?", False)], [3])),
      ("Ficou branca", "M", dom_perto([VE(("P03", None), x=960, treme=[{"g": "Ficou branca", "dur": 0.7}])])),
      ("Tião... isso", "M", dom_perto([VE(("P03", None)), TI(("P05", None))], [B("Tião... isso aqui sai todo mês?", 0, "Tião", "mês")])),
      ("Eu olhei aquela linha", "M", dom_perto([TI(("P14", None), x=960)]))],
 83: [("^", "M", {"k": "cal", "mes": "O seu salário", "ate": 30, "marcados": {"10": {"cor": VERM, "rotulo": "acabou?"}}}),
      ("no próximo vídeo", "M", ic([("🔎", "o que ela achou naquela linha", False), ("📅", "quanto levava dela por ano", False), ("⏱️", "o que ela fez em 10 minutos", False)], "No próximo vídeo")),
      ("eu fui conferir", "M", dom_perto([TI(("P14", None), x=960)])),
      ("Seu salário acaba no dia dez? O", "M", fr("Seu salário acaba no *dia 10*?", "O problema não é o salário.")),
      ("Clica agora", "M", dom_perto([TI(("P12", None), x=960, braco={"tipo": "aceno", "g": "Clica agora"})]))],
}

