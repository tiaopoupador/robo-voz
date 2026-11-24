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
DESC = ("Onze e quarenta da noite, a vizinha do carrão de R$ 189.900 bate na porta do porteiro e pede R$ 50 emprestados até sexta.\n\n"
        "Neste vídeo o Tião faz, no papel de pão, as três contas que ninguém da rua via por trás daquele carro: a parcela do financiamento "
        "(com a taxa do Banco Central), o aluguel da casa de vitrine e o rotativo do cartão, a conta que engorda até no domingo. "
        "E mostra o que a lei do Desenrola diz sobre os juros do rotativo.")
TAGS = ["financiamento de carro", "juros do financiamento", "rotativo do cartão", "juros do cartão de crédito", "desenrola", "lei 14.690",
        "carro financiado", "dívida no cartão", "educação financeira", "finanças pessoais", "Tião Poupador"]
PERGUNTA = "Qual é o carro da sua rua que você nunca entendeu como foi pago?"
CAP_NOMES = {"Abertura (é um Reels: entende-se sozinha)": "Onze e quarenta da noite", "Quem fala": "Chega mais", "A chave": "A chave do carrão",
             "Onze e quarenta da noite": "O pedido", "Conta número um: a parcela": "Conta 1: a parcela",
             "Conta número dois: a casa de vitrine": "Conta 2: a casa de vitrine", "Conta número três: o cartão": "Conta 3: o cartão",
             "O que o Tião respondeu": "O que o Tião respondeu", "O carrão sai da rua": "O carrão sai da rua"}
FORTES = {"valéria", "carrão", "parcela", "rotativo", "juros", "desenrola", "cartão", "aluguel"}
CLIMA = {0: "tensao", 4: "calma", 7: "humor", 14: "tensao", 20: "curiosa", 24: "drama", 32: "tensao", 37: "triste", 38: "reflexiva",
         41: "virada", 46: "calma", 48: "reflexiva", 51: "virada", 54: "final", 58: "curiosa", 59: "tensao"}
AMB = [("grilos", 0, "^", 14, 0.22), ("grilos", 14, "^", 40, 0.2), ("grilos", 15, "^", 30, 0.2), ("passaros", 7, "^", 20, 0.2),
       ("grilos", 38, "^", 30, 0.18), ("passaros", 48, "^", 20, 0.2), ("passaros", 51, "^", 16, 0.2), ("passaros", 54, "^", 20, 0.2)]

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
CARRO = {"src": F + "carrao.png", "x": 1060, "y": 890, "w": 840}
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
VD = dict(x=80, y=40, larg=950, rabo=(1180, 470))       # balao de quem esta sozinho, a direita
BT = dict(x=90, larg=930, rabo=(1290, 560))            # balao do Tiao (ele a direita, a Valeria a esquerda)
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

L = {
 # 0. Abertura (Reels): a mesma cena volta, igualzinha, na fala 15
 0: [("^", "M", rua_noite()), ("Só a luz", "M", noite_larga([TS_N()])), ("E a Valéria", "M", chega_noite()), ("fala baixinho", "M", pede())],
 1: [("^", "M", nu(50, "Emprestados até sexta", "pedido de quem desceu de um carrão de R$ 189.900", cor=VERM, fmt="int", suf=" reais", emoji="🤫")),
     ("de manhã", "M", rua_dia([VE(("P06", None), x=1250)]))],
 2: [("^", "M", rua_dia()), ("três contas", "M", ic([("🚗", "quanto cada uma come por mês", False), ("📈", "a que engorda até no domingo", False), ("🤐", "o que eu respondi", False)], "Hoje, três contas")),
     ("Essa última", "M", noite_perto([TI(("P10", None), x=960)]))],
 3: [("^", "M", rua_dia([TI(("P03", None), x=450)])), ("fica comigo", "M", dom_perto([TI(("P06", None), x=960)])), ("puxa a cadeira", "M", dom_larga())],
 # 1. Quem fala
 4: [("^", "M", dom_perto([TI(("P08", None), x=960)]))],
 5: [("^", "M", dom_perto([TI(("P06", None), ("P07", "porteiro"), x=1250)])), ("Nem sempre", "M", dom_perto([TI(("P10", None), x=1250)]))],
 6: [("^", "M", dom_larga([TS_D()])), ("caneca branca", "M", foco(*CANECA_D)), ("papel de pão", "M", dom_larga([TS_D(("P17", None))])),
     ("Aqui eu faço", "M", dom_perto([TI(("P09", None), x=960)]))],
 # 2. A chave
 7: [("^", "M", rua_dia(carro=False)), ("eu na minha varanda", "M", dom_larga([TS_D()])),
     ("E aí ela chegou", "M", rua_dia(anda_carro={"de": -700, "g": "chegou", "dur": 3.0}))],
 8: [("^", "M", rua_dia([P("valeria", 1640, 960, 600, ("R1", None))])), ("Ela gerencia", "M", rua_dia([VE(("P01", None), x=1300)])),
     ("desceu", "M", rua_dia([VE(("P05", None), x=1450)]))],
 9: [("^", "M", rua_dia([VE(("P07", None), x=1250)], [B("R$ 189.900, gente. Peguei ontem.", 0, "Cento", "ontem", **VD)]))],
 10: [("^", "M", dom_larga([TS_D()], zoom=[1.0, 1.3], fx=22, fy=55)), ("Para a minha caneca", "M", foco(*CANECA_D))],
 11: [("^", "M", rua_dia([VE(("P06", None), ("P02", "Compra"), x=1250)], [B("Ai, Tião... que pobreza. Essa caneca tem a idade da rua.", 0, "Ai", "rua", **VD),
                                                                       B("Compra uma nova, homem, que eu até te dou o dinheiro.", 0, "Compra", "dinheiro", **VD)]))],
 12: [("^", "M", dom_perto([TI(("P01", None), x=960)])), ("A caneca é lascada", "M", foco(*CANECA_D)),
      ("chave girando", "M", rua_dia([VE(("P07", None), x=1250)])), ("uma pergunta", "M", dom_perto([TI(("P05", None), x=960)])),
      ("como é que fecha", "M", fr("Salário de gerente de loja e um carro de *R$ 189.900*", "como é que fecha essa conta?"))],
 13: [("^", "M", dom_perto([TI(("P06", None), x=960)])), ("deixa o like", "M", {"k": "botao", "tipo": "like", "texto": "Deixa o like"}),
      ("se inscreve", "M", {"k": "botao", "tipo": "inscrever", "texto": "E se inscreve"}),
      ("conta aqui embaixo", "M", fr("Qual carro da *sua rua* ninguém entende como foi pago?", "escreve aqui embaixo, eu leio e respondo"))],
 # 3. Onze e quarenta da noite
 14: [("^", "M", noite_larga([TS_N()])), ("A rua já dormia", "M", rua_noite())],
 15: [("^", "M", rua_noite()), ("Só a luz", "M", noite_larga([TS_N()])), ("E a Valéria", "M", chega_noite()), ("fala baixinho", "M", pede())],
 16: [("^", "M", noite_perto([VE(("P04", None)), TI(("P05", None))])), ("sem a chave", "M", noite_perto([VE(("P04", None), ("P08", "celular"), x=960)]))],
 17: [("^", "M", noite_perto([VE(("P08", None), x=960, treme=[{"g": "apitou", "dur": 0.6}])])),
      ("Sua fatura", "M", cel("Cartão de crédito", [("Sua fatura vence", "segunda", False), ("Valor", "R$ 3.200", False)], [1]))],
 18: [("^", "M", noite_perto([VE(("P10", None)), TI(("P05", None))], [B("É só para a gasolina, Tião.", 0, "É só", "Tião")])),
      ("O cartão estourou", "M", noite_perto([VE(("P04", None)), TI(("P05", None))], [B("O cartão estourou. O posto recusou na frente de todo mundo.", 0, "O cartão", "mundo")])),
      ("Eu preciso", "M", noite_perto([VE(("P01", None)), TI(("P03", None))], [B("Eu preciso ir trabalhar na segunda. Sexta eu te devolvo.", 0, "Eu preciso", "devolvo")])),
      ("Eu vim", "M", noite_perto([VE(("P01", None)), TI(("P03", None))], [B("A sua luz é a única acesa. E você nunca me perguntou do carro.", 0, "Eu vim", "carro")])),
      ("Se eu peço", "M", noite_perto([VE(("P11", None)), TI(("P13", None))], [B("Por favor, não conta para ninguém!", 0, "Por favor", "ninguém")]))],
 19: [("^", "M", noite_larga([TS_N(), P("valeria", 1350, 930, 640, ("R1", None))],
                            [B("Senta aí, Valéria. Antes dos cinquenta, deixa eu te mostrar uma coisa.", 0, "Senta", "coisa", x=520, y=30, larg=1000, rabo=(720, 290))])),
      ("papel de pão", "M", foco(*PAPEL_N, luz=LV))],
 # 4. Conta número um: a parcela
 20: [("^", "M", fr("Conta número *1*: a parcela")), ("Eu perguntei", "M", noite_larga([TS_N(("P17", None)), VS_N()])),
      ("Deu o carro antigo", "M", conta("O carrão", [("Preço", 189900), ("Carro antigo, de entrada", -30000)], "Financiado", neutro=True, passo=1.8)),
      ("sessenta meses", "M", nu(60, "Parcelas", "cinco anos pagando", cor=VERM, fmt="int", suf=" meses", emoji="📅"))],
 21: [("^", "M", noite_perto([TI(("P05", None), x=960)])), ("Em setembro", "M", nu(1.96, "Juros médios do financiamento de carro, ao mês", "Banco Central, setembro", cor=VERM, fmt="num", casas=2, suf="%", emoji="🏦")),
      ("No ano", "M", nu(26, "No ano", "Banco Central, setembro", cor=VERM, fmt="int", suf="%", emoji="📈"))],
 22: [("^", "M", nu(4555.56, "A parcela da Valéria", "todo mês", cor=VERM, casas=2, emoji="🚗")),
      ("Todo mês", "M", {"k": "grade", "total": 60, "cols": 12, "titulo": "60 parcelas", "cor": VERM, "rotuloFim": "cinco anos"})],
 23: [("^", "M", ba([("Emprestado", 159900, AZUL), ("Ela vai pagar", 273333, VERM)], "Somando as 60 parcelas")),
      ("São cento e treze", "M", nu(113433, "Só de juros", "mais da metade de outro carrão", cor=VERM, emoji="🏦"))],
 24: [("^", "M", noite_perto([VE(("P03", None)), TI(("P05", None))], [B("Cento e treze mil, Tião?! Isso é mentira.", 0, "Cento", "mentira")])),
      ("O vendedor", "M", noite_perto([VE(("P04", None)), TI(("P05", None))], [B("O vendedor falou que a parcela cabia no meu bolso!", 0, "O vendedor", "bolso")]))],
 25: [("^", "M", noite_perto([TI(("P07", None), x=960)])), ("Esse dinheiro", "M", fr("Esse dinheiro *criou perna*!"))],
 26: [("^", "M", noite_perto([TI(("P11", None), x=960)])), ("o financiamento de carro", "M", nu(48, "Prazo médio do financiamento de carro", "Banco Central, setembro", cor=VERM, fmt="int", suf=" meses", emoji="📅")),
      ("Quatro anos", "M", rua_dia())],
 # 5. Conta número dois: a casa de vitrine
 27: [("^", "M", fr("Conta número *2*: a casa")),
      ("Eu achava", "I", (F + "rua-sem-carro.jpg", [dict(cb("ALUGADA", 50, 40, VERM), g="alugada")])), ("Três mil e novecentos", "M", nu(3900, "Aluguel, por mês", "fora a luz", cor=VERM, emoji="🏠"))],
 28: [("^", "M", noite_larga([TS_N(("P17", None)), VS_N()])),
      ("já com os descontos", "M", conta("O mês da Valéria", [("Salário, já com os descontos", 8700), ("Parcela do carro", -4555.56), ("Aluguel", -3900)], passo=2.4))],
 29: [("^", "M", nu(244.44, "Sobra para o mês inteiro", "a partir do mês que vem", cor=VERM, casas=2, emoji="😬")),
      ("Para comida", "M", ic([("🍚", "comida", False), ("⛽", "gasolina", False), ("💡", "luz", False), ("📱", "celular", False), ("💇", "a escova da semana", False)], "Com R$ 244"))],
 30: [("^", "M", noite_perto([VE(("P01", None)), TI(("P05", None))], [B("Mas eu nunca fiquei sem nada, Tião.", 0, "Mas eu", "Tião")])),
      ("no dia dez", "M", {"k": "cal", "mes": "O salário da Valéria", "ate": 30, "marcados": {"10": {"cor": VERM, "rotulo": "já foi"}}}),
      ("Eu como fora", "M", noite_perto([VE(("P02", None)), TI(("P04", None))], [B("Eu como fora quase todo dia. Eu estou sempre arrumada.", 0, "Eu como", "arrumada")]))],
 31: [("^", "M", noite_perto([VE(("P04", None)), TI(("P03", None))], [B("Valéria, e como você vai pagar isso tudo com 240 reais?", 1, "Valéria", "reais", **BT)])),
      ("Ela olhou para o celular", "M", noite_perto([VE(("P08", None), x=960)]))],
 # 6. Conta número três: o cartão
 32: [("^", "M", fr("Conta número *3*: o cartão")), ("Há meses", "M", ic([("🍽️", "o almoço", False), ("⛽", "a gasolina", False), ("💇", "o salão", False), ("👗", "a roupa nova", False)], "Tudo no cartão")),
      ("Até o cartão", "M", noite_perto([VE(("P11", None), x=960)])),
      ("E a fatura chegou", "M", cel("Cartão de crédito", [("Fatura", "R$ 3.200", False), ("Na conta", "não tem", False)], [0]))],
 33: [("^", "M", noite_perto([TI(("P05", None), x=960)])), ("Entra no rotativo", "M", fr("O resto vai para o *rotativo*", "um dos dinheiros mais caros do banco"))],
 34: [("^", "M", nu(15.29, "Juros médios do rotativo do cartão, ao mês", "Banco Central, setembro", cor=VERM, fmt="num", casas=2, suf="%", emoji="🔥")),
      ("No ano", "M", nu(450, "No ano, passa de", "Banco Central, setembro", cor=VERM, fmt="int", suf="%", emoji="🔥"))],
 35: [("^", "M", nu(489, "Juros só no primeiro mês", "R$ 3.200 a 15% ao mês", cor=VERM, emoji="📈")),
      ("Em três meses", "M", ba([("Hoje", 3200, AMAR), ("Em 3 meses sem pagar", 4904, VERM)], "A fatura no rotativo")),
      ("É essa a conta", "M", noite_perto([VE(("P04", None), x=960)]))],
 36: [("^", "M", noite_perto([TI(("P09", None), x=960)])), ("Desenrola", "M", fr("Lei *14.690*, de 2023 (Desenrola)", "site oficial da Câmara dos Deputados")),
      ("Ela diz que", "M", fr("Juros do rotativo: no máximo *o tamanho da dívida*", "Lei 14.690/2023, art. 28")),
      ("Três mil e duzentos viram", "M", ba([("A dívida", 3200, AMAR), ("O máximo, com os juros", 6400, VERM)], "A dívida pode, no máximo, dobrar")),
      ("Se o banco", "M", noite_perto([TI(("P06", None), x=960)]))],
 37: [("^", "M", noite_perto([VE(("P14", None), x=960)])), ("me escreve", "M", fr("Fatura que não cabe? Escreve aqui embaixo: *eu também*")),
      ("deixa o like", "M", {"k": "botao", "tipo": "like", "texto": "Deixa o like"}), ("Ela não esperava", "M", noite_perto([TI(("P10", None), x=960)]))],
 # 7. O que o Tiao respondeu
 38: [("^", "M", noite_larga([TS_N(), VS_N()], zoom=[1.0, 1.15]))],
 39: [("^", "M", noite_perto([VE(("P04", None)), TI(("P03", None))], [B("Cinquenta para gasolina eu não te empresto.", 1, "Valéria", "empresto", **BT)])),
      ("Porque", "M", noite_perto([VE(("P11", None)), TI(("P07", None))], [B("Segunda você vai precisar de mais cinquenta. E o carro continua comendo R$ 4.500 por mês.", 1, "Porque", "mês", x=90, larg=930, rabo=(1290, 560))]))],
 40: [("^", "M", noite_larga([TS_N(), P("valeria", 1350, 930, 640, ("R1", None), sai={"ate": 2300, "g": "levantou", "dur": 4.0, "oculos": True})]))],
 41: [("^", "M", noite_perto([VE(("P03", None)), TI(("P05", None))], [B("Mas o cartão do ônibus da semana eu pago.", 1, "Mas", "pago", **BT)])),
      ("E segunda", "M", noite_perto([VE(("P03", None)), TI(("P06", None))], [B("E segunda, seis e meia, eu vou junto com você até o ponto.", 1, "E segunda", "ponto", **BT)])),
      ("Ninguém precisa", "M", noite_perto([VE(("P04", None)), TI(("P10", None))], [B("Ninguém precisa saber de nada.", 1, "Ninguém", "nada", **BT)])),
      ("E domingo", "M", noite_perto([VE(("P01", None)), TI(("P09", None))], [B("Domingo a gente senta aqui, com café, e faz a conta inteira. Conta por conta.", 1, "E domingo", "conta", x=90, larg=930, rabo=(1290, 560))]))],
 42: [("^", "M", foco(*PAPEL_N, luz=LV)), ("Aí, sem pedir", "M", noite_perto([VE(("P04", None), x=960)])),
      ("me ensina", "M", noite_perto([VE(("P10", None)), TI(("P05", None))], [B("Tião... me ensina a fazer essa conta?", 0, "Tião", "conta")]))],
 43: [("^", "M", noite_perto([VE(("P01", None)), TI(("P06", None))], [B("Ensino. Mas a conta, você copia com a sua letra.", 1, "Ensino", "letra", **BT)])),
      ("esse lápis", "M", noite_perto([VE(("P02", None)), TI(("P01", None))], [B("E esse lápis fica com você até domingo.", 1, "E esse", "domingo", **BT)]))],
 44: [("^", "M", noite_larga([TS_N(), VS_N(("P18", None))], zoom=[1.0, 1.18], fx=60)),
      ("juros do carro", "M", nu(113433, "Juros do carro", "a mão dela parou no meio do número", cor=VERM, emoji="✋"))],
 45: [("^", "M", noite_perto([VE(("P03", None)), TI(("P13", None))], [B("Eu assinei isso sem ler, Tião! O vendedor só me mostrou a parcela.", 0, "Eu assinei", "parcela")]))],
 46: [("^", "M", rua_noite([P("valeria", 1450, 985, 560, ("R1", None), sai={"ate": -300, "g": "foi para casa", "dur": 4.0, "oculos": True})])),
      ("Mas antes", "M", noite_perto([TI(("P10", None), x=960)]))],
 47: [("^", "M", noite_perto([TI(("P09", None), x=960)])), ("usa o FinMoovi", "V", "banco:FM:1-cartoes/cartoes__estilo-moldura-celular__horizontal.mp4"),
      ("São sete dias", "M", nu(7, "Dá para testar o FinMoovi", "link na descrição", cor=VERDE, fmt="int", suf=" dias", emoji="📱"))],
 # 8. O carrao sai da rua
 48: [("^", "M", dom_larga([TS_D(), P("valeria", 1300, 950, 620, ("R1", None), anda={"de": 2300, "g": "ela apareceu", "dur": 3.2, "oculos": True})])),
      ("Eu passei o café", "M", foco(*CANECA_D)),
      ("Aí eu perguntei", "M", dom_perto([VE(("P04", None)), TI(("P05", None))], [B("Quanto esse carro vale hoje, e quanto falta pagar?", 1, "Quanto", "pagar", **BT)])),
      ("Ela escreveu", "M", dom_larga([TS_D(("P17", None)), VS_D(("P18", None))])), ("vendendo", "M", dom_perto([VE(("P03", None), x=960)]))],
 49: [("^", "M", dom_perto([VE(("P07", None), x=960)])), ("Depois empurrou", "M", dom_perto([VE(("P10", None)), TI(("P05", None))], [B("Me ajuda a vender, Tião.", 0, "Me ajuda", "Tião")]))],
 50: [("^", "M", ponto([P("tiao", 700, 860, 560, ("R1", None)), P("valeria", 980, 860, 600, ("R1", None))])),
      ("ela dirigiu", "M", rua_dia(anda_carro={"de": 1060, "x": 2700, "g": "dirigiu", "dur": 3.5})),
      ("a gente voltou", "M", ponto([VE(("P02", None)), TI(("P01", None))], perto=True)),
      ("a parcela de quatro mil", "M", nu(4555.56, "A parcela do carro", "sumiu", cor=VERDE, casas=2, emoji="✅"))],
 51: [("^", "M", fr("*Quatro meses* depois")), ("Outro sábado", "M", rua_dia(carro=False)),
      ("a garagem vazia", "I", (F + "rua-sem-carro.jpg", [pl("ALUGA-SE", 28, 62, cor=VERM, tam=64)]))],
 52: [("^", "M", ic([("🚗", "financiamento quitado", False), ("🏠", "casa menor", False), ("💳", "fatura em 3 vezes", False), ("🚌", "de ônibus", False)], "Quatro meses depois")),
      ("Parcelou a fatura", "M", cel("Cartão de crédito", [("Fatura parcelada", "3 vezes", False), ("Só o mínimo", "nunca mais", False)], [0])),
      ("E vai de ônibus", "M", ponto([P("valeria", 900, 860, 600, ("R1", None))]))],
 53: [("^", "M", rua_dia([P("valeria", 2300, 960, 600, ("R1", None), anda={"de": -300, "g": "comentou", "dur": 7.0, "oculos": True})], carro=False,
                       baloes=[{"texto": "A Valéria quebrou.", "g": "A Valéria quebrou", "ate": "quebrou", "x": 560, "y": 60, "larg": 800}])),
      ("Ela ri", "M", rua_dia([VE(("P12", None), x=1250)], carro=False)), ("Ninguém da rua", "M", rua_dia([VE(("P15", None), x=1250)], carro=False))],
 54: [("^", "M", dom_larga([TS_D(), P("valeria", 1300, 950, 620, ("R1", None), anda={"de": 2300, "g": "passagem", "dur": 3.0, "oculos": True})])),
      ("Tirou da bolsa", "M", nu(50, "Dentro da caneca", "dobrada em quatro", cor=VERDE, fmt="int", suf=" reais", emoji="💵")),
      ("A mesma caneca", "M", foco(*CANECA_D))],
 55: [("^", "M", dom_perto([VE(("P02", None), x=1250)], [B("Para você comprar uma caneca nova, Tião!", 0, "Para você", "Tião", **VD)]))],
 56: [("^", "M", dom_perto([TI(("P08", None), x=960)])), ("Caneca velha", "M", fr("Caneca velha, *bolso cheio*!"))],
 57: [("^", "M", rua_dia([P("valeria", 900, 960, 600, ("R1", None), sai={"ate": 2400, "g": "foi embora", "dur": 4.0, "oculos": True})], carro=False))],
 58: [("^", "M", dom_perto([TI(("P06", None), x=960)])), ("escreve aqui embaixo", "M", fr("Vai fazer a sua conta hoje? Escreve aqui embaixo: *1*")),
      ("E fica mais", "M", dom_perto([TI(("P10", None), x=960)]))],
 59: [("^", "M", dom_larga([TS_D(), VS_D()])),
      ("o extrato", "M", cel("Extrato da conta do salário", [("Salário", "+ R$ 8.700", True), ("Aluguel", "- R$ 3.900", False), ("Cartão", "- R$ 3.200", False), ("? ? ? ? ?", "- R$ ? ? ?", False)], [3])),
      ("Ficou branca", "M", dom_perto([VE(("P03", None), x=960, treme=[{"g": "Ficou branca", "dur": 0.7}])])),
      ("Tião... isso", "M", dom_perto([VE(("P03", None)), TI(("P05", None))], [B("Tião... isso aqui sai todo mês?", 0, "Tião", "mês")])),
      ("Eu olhei aquela linha", "M", dom_perto([TI(("P14", None), x=960)]))],
 60: [("^", "M", {"k": "cal", "mes": "O seu salário", "ate": 30, "marcados": {"10": {"cor": VERM, "rotulo": "acabou?"}}}),
      ("no próximo vídeo", "M", ic([("🔎", "o que ela achou naquela linha", False), ("📅", "quanto levava dela por ano", False), ("⏱️", "o que ela fez em 10 minutos", False)], "No próximo vídeo")),
      ("eu fui conferir", "M", dom_perto([TI(("P14", None), x=960)])),
      ("Seu salário acaba no dia dez? O", "M", fr("Seu salário acaba no *dia 10*?", "O problema não é o salário.")),
      ("Clica agora", "M", dom_perto([TI(("P12", None), x=960, braco={"tipo": "aceno", "g": "Clica agora"})]))],
}
