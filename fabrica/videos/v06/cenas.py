# Cenas do video 06 REFEITO (27/11/2026 tarde). Roteiro: roteiros/06-dez-regras.md. Fatos: fabrica/biblia.md.
# Ed recusou a 1.a montagem: card inacabado no comeco, balao com fala que o narrador nao dizia, imagem sem ligacao com a fala,
# pouco motion e pouca musica. Regras desta versao:
#  - balao SO quando a fala do personagem e dita, com g = a 1.a palavra da fala dele e ate = a ultima;
#  - cada livro, estudo e pesquisa tem o seu cartao de citacao (ci) ou grafico (ba, li, nu);
#  - o video final sai acelerado (RITMO), na nuvem.
from fabrica.kit import *
from fabrica.videos.v05.cenas import (P, B, T, VE, TI, GE, DE, TS_D, VS_D, dom_larga, dom_perto, rua_dia, rua_noite, foco, cel, conta,
                                      CANECA_D)
from fabrica.videos.v03.cenas import IMG as _I3

RUA = "fundo-banquinho"
IMG = {k: _I3[k] for k in ("fundo-banquinho", "selo-tiao-cafe")}
_V = "valeria-ficha-a.jpg.jpg + tiao-ficha-oficial.jpg"
_T = "tiao-ficha-oficial.jpg"
TITULO = "10 Regras do Tião Para Viver Tranquilo Ganhando Pouco (Salário de R$ 2.800)"
MODELO = {"id": "HIrzIYQCzMU", "canal": "@eduinvesteoficial", "vezes": 24.8}
RITMO = 1.25  # Ed, 27/11: «assisti o video 6 na velocidade 1,25 e ficou otimo»
CAPA_TEXTO = "GANHA POUCO VIVE TRANQUILO"
CAPA_LETRAS = {"A": ("GANHA POUCO VIVE TRANQUILO", "TRANQUILO", "verde"), "B": ("R$ 2.800 E DORME BEM", "DORME BEM", "verde"),
               "C": ("GANHA O TRIPLO E PEDE EMPRESTADO", "PEDE EMPRESTADO", "vermelho"), "D": ("10 REGRAS ZERO APERTO", "ZERO APERTO", "amarelo")}
VINHETA = 3  # a vinheta entra depois da fala 3 («Vamos começar?»)
REELS_DE = 1  # 27/11: a fala 0 e o «No episódio anterior»; o Reels do gancho comeca na fala 1
PUBLICA = "2026-11-27 18:00"
PUBLICA_TXT = "sexta, 27/11, às 18h (Brasília, 21h em Lisboa)"
PRAZO = "sexta, 27/11, até as 15h (o vídeo vai ao ar às 18h)"
PRAZO_ISO = "2026-11-27T15:00:00-03:00"
CAPA = (_T, "Same composition as a calm before-and-after split, warm cream background, flat 2D cartoon. LEFT (smaller): Tiao tired and worried at a cheap "
            "wooden desk at night, bills and crumpled papers on the floor, head in his hand. A big thick GREEN curved arrow from left to right. RIGHT (bigger): "
            "the same Tiao relaxed on his simple porch armchair, hands behind his head, smiling, a plain white enamel mug with a chipped rim and a small stack "
            "of coins on a little table, a sleeping cat. Leave the TOP-LEFT empty for two big lines of title text.", "antes-depois")
CAPAS_TESTE = [
    (_T, "CALM CONTRAST mood, soft green and cream. Tiao big and close on the RIGHT, sleeping peacefully on his porch armchair at night, a smile, his "
         "white chipped mug beside him; behind him, through the window of the house across the street, a tall man (Marcos) awake at 3am under a lamp, "
         "pulling his hair over a pile of bills. Leave the left half empty for the title text.", "dorme-bem"),
    ("marcos-neutro.jpg + tiao-ficha-oficial.jpg", "PUBLIC EMBARRASSMENT mood, red and white. Inside a busy neighborhood butcher shop: Marcos (tall man, gelled hair, "
         "white shirt, big silver watch) laughing awkwardly, holding a declined card toward the camera, a red X over the card machine; behind him in line, "
         "Tiao calmly takes cash from a simple wallet. Leave the top third empty for the title text.", "acougue"),
    (_T, "ORGANIZED mood, yellow and dark blue. Tiao standing at the doorman desk of a fancy building lobby, smiling, holding up his phone with a clean "
         "green budget chart; ten small round icons float around him in a circle (house, cart, bus, piggy bank, scissors, heart, phone, calendar, coins, mirror). "
         "Leave the top third empty for the title text.", "dez-regras"),
]
DESC = ("O Tião ganha R$ 2.800 por mês como porteiro e dorme tranquilo. O Marcos, o vizinho da picape zero, ganha o triplo, e no dia 20 pede "
        "dinheiro emprestado na fila do açougue.\n\n"
        "Neste vídeo o Tião mostra as 10 regras dele, uma por uma, com a conta feita em cima do salário dele: para onde vai cada real, pagar a si mesmo "
        "primeiro (a lição de 1926 de O Homem Mais Rico da Babilônia e o estudo do Nobel Richard Thaler), a casa que manda nas outras contas (IBGE), "
        "o mercado com lista, não parcelar (o cheque especial e a pesquisa de endividamento da CNC), cortar o que paga e não usa (e a linha do extrato "
        "que deixou a Valéria branca), o carro, o prazer sem culpa, o décimo terceiro e a comparação. Com a lei na mão: o cheque especial "
        "(Resolução CMN 4.765), os serviços bancários grátis (Resolução CMN 3.919), o vale-transporte (Lei 7.418) e o 13º (Lei 4.749).")
TAGS = ["viver tranquilo ganhando pouco", "como viver com salário baixo", "regras de dinheiro", "como organizar o salário", "pague-se primeiro",
        "o homem mais rico da babilônia", "orçamento pessoal", "cheque especial", "cesta de serviços", "vale-transporte", "décimo terceiro",
        "como guardar dinheiro ganhando pouco", "educação financeira", "Tião Poupador", "Tião Conversa"]
PERGUNTA = "Qual das 10 regras você começa hoje? Só o número."
CAP_NOMES = {"No episódio anterior": "No episódio anterior", "Abertura (é um Reels: entende-se sozinha)": "Ele ganha o triplo",
             "Para onde vai cada real": "Regras 1 e 2", "A casa e a panela": "Regras 3 e 4", "O dia vinte": "Regra 5 e o dia 20",
             "A linha do extrato": "Regra 6: a linha do extrato", "O carro e o prazer": "Regras 7 e 8", "O que a rua não viu": "Regra 9",
             "A última regra": "Regra 10", "O próximo": "A mensagem da farmácia"}
FORTES = {"regra", "salário", "marcos", "valéria", "sandra", "extrato", "reserva", "parcela", "limite", "picape", "aluguel", "mercado", "prazer",
          "livro", "estudo", "pesquisa"}
GIF = "foto"
REELS_TOPO = "Ele ganha o *TRIPLO*|e no dia 20 pede|dinheiro *EMPRESTADO*|na fila do açougue!"  # a frase isca do Short do gancho (fabrica/reels.py)
REELS_EMOJI = "1f631"
PLAYLIST = "tiao-conversa"

# o clima troca a cada 2 ou 3 min; 27/11: 15 faixas novas e rodizio por video (montar.py); o gancho (67) e sempre a Hitman
CLIMA = {0: "drama", 1: "alerta", 4: "calma", 10: "curiosa", 15: "virada", 18: "reflexiva", 22: "humor", 25: "tensao", 29: "triste",
         32: "tensao", 35: "curiosa", 39: "drama", 40: "virada", 42: "tensao", 44: "humor", 45: "calma", 49: "humor", 54: "reflexiva",
         58: "calma", 59: "reflexiva", 62: "virada", 63: "drama", 66: "final", 67: "gancho"}
AMB = [("passaros", 4, "^", 20, 0.2), ("passaros", 18, "^", 20, 0.2), ("passaros", 35, "^", 20, 0.2), ("grilos", 42, "^", 14, 0.2)]

# ---------- as pecas que se repetem ----------
def tiao(pose, lado=1): return (RUA, pose, lado)
VE_B = dict(x=110, y=40, larg=1080, rabo=(640, 470))  # balao de quem esta a esquerda
def so(pid, pose, texto=None, g1=None, g2=None, noite=False):
    """um da turma de perto, na rua, com balao opcional (g1 e g2 = a 1.a e a ultima palavra da FALA DELE, ditas nesta fala)"""
    f = rua_noite if noite else rua_dia
    return f([GE(pid, (pose, None), x=700)], [B(texto, 0, g1, g2, **VE_B)] if texto else [], **({} if noite else {"carro": False}))
def perto_v(*poses, baloes=(), x=600): return dom_perto([VE(*poses, x=x)], baloes)
def extrato(destaque=()):
    return cel("Extrato · conta do salário", [("Salário", "+ 8.700,00", True), ("Pacote de serviços", "- 54,90", False),
                                              ("Juros cheque especial", "- 188,25", False)], destaque)
CONTA_TIAO = conta("O mês do Tião", [("Salário", 2800), ("Aluguel", -750), ("Luz, água, gás e internet", -290), ("Mercado", -750),
                                     ("Ônibus (vale)", -168), ("Celular", -42), ("Farmácia", -50), ("O carro velho", -190)], total="Sobram")
def regra(n, texto, emoji): return ic([(emoji, texto, False)], f"Regra {n}")

L = {
 # 0. No episodio anterior
 0: [("^", "M", so("valeria", "P15")), ("caneca velha", "M", foco(*CANECA_D)),
     ("meia-noite", "M", rua_noite([DE("valeria", 900)])), ("cinquenta reais", "M", nu(50, "Para a gasolina", "e eu não emprestei", cor=VERM, emoji="⛽")),
     ("fez a conta", "M", conta("A conta da Valéria", [("Salário", 8700), ("Parcela da SUV", -4555.56), ("Aluguel", -3900)], total="Sobram")),
     ("extrato do banco", "M", extrato()),
     ("Ficou branca", "M", perto_v(("P03", None), baloes=[B("Tião, isso aqui sai todo mês?", 0, "Tião", "mês", **VE_B)])),
     ("Hoje você vai saber", "C", tiao("P4", 1))],
 # 1. Abertura (Reels)
 1: [("^", "C", tiao("P4", 1)), ("ganha o triplo", "M", ba([("Eu, o Tião", 2800, VERDE), ("O Marcos", 8400, VERM)], "Salário por mês")),
     ("fila do açougue", "M", so("marcos", "P01")), ("recusado", "M", cel("Maquininha do açougue", [("Cartão do Marcos", "RECUSADO", False)], [0]))],
 2: [("^", "M", so("sandra", "P01")), ("dez regras", "M", fr("*10 regras*. Nenhuma pede para ganhar mais.")),
     ("livro", "M", li(["1926: um livro", "2004: um estudo", "2026: o meu extrato"], 0, "De onde vêm as regras")),
     ("Nobel", "M", li(["1926: um livro", "2004: um estudo", "2026: o meu extrato"], 1, "De onde vêm as regras")),
     ("susto", "M", li(["1926: um livro", "2004: um estudo", "2026: o meu extrato"], 2, "De onde vêm as regras"))],
 3: [("^", "C", tiao("P2", 1)), ("puxa a cadeira", "M", dom_larga())],
 # 2. Para onde vai cada real
 4: [("^", "M", dom_perto([TI(("P08", None), x=960)]))],
 5: [("^", "C", tiao("P1", 1)), ("lápis amarelo", "C", tiao("P2", -1)), ("filho", "M", fr("Com filho, os *números* mudam.", "A ordem das regras, não."))],
 6: [("^", "M", perto_v(("P08", None))), ("regra seis", "M", fr("A linha da Valéria: *regra 6*.")), ("susto", "C", tiao("P4", -1))],
 7: [("^", "M", regra(1, "saiba para onde vai cada real", "🧭")), ("Aluguel da casinha", "M", CONTA_TIAO)],
 8: [("^", "M", rua_dia([DE("tiao", 1100)])), ("pega no tranco", "M", so("marcos", "P06")),
     ("dois mil duzentos e quarenta", "M", nu(2240, "A vida básica, paga", "todo mês", emoji="🧾")),
     ("quinhentos e sessenta", "M", nu(560, "O meu espaço de manobra", "R$ 2.800 menos R$ 2.240", cor=VERDE, emoji="🟢"))],
 9: [("^", "C", tiao("P3", 1)), ("Quanto precisam", "M", fr("Sabem quanto *ganham*.", "Quanto precisam, não.")),
     ("deu de ombros", "M", so("marcos", "P06", "Depende, Tião.", "Depende", "Tião")), ("perde dinheiro", "C", tiao("P3", -1))],
 10: [("^", "C", tiao("P1", 1)),
      ("Escassez", "M", ci("Sendhil Mullainathan e Eldar Shafir", "2013", "livro «Escassez»", "Quando falta dinheiro, a preocupação ocupa a cabeça inteira.")),
      ("cabeça cheia", "M", fr("Não é burrice. É *cabeça cheia*.")), ("escrevo tudo", "C", tiao("P2", -1))],
 11: [("^", "M", ic([("🏠", "essencial", False), ("👟", "desejo", False), ("🧊", "imprevisto", False)], "Cada gasto num grupo")),
      ("onde aquilo entra", "C", tiao("P2", 1)), ("somem rapidinho", "M", nu(560, "Somem rápido", "se não tiverem destino", cor=VERM, emoji="💨"))],
 12: [("^", "M", regra(2, "pague a você mesmo primeiro", "🐷")),
      ("duzentos e oitenta", "M", cel("Dia 5 · transferência", [("Para: conta da reserva", "- 280,00", False)], [0])),
      ("décimo", "M", nu(10, "Um décimo do salário", "R$ 280 de R$ 2.800", cor=VERDE, fmt="int", suf="%", emoji="🐷"))],
 13: [("^", "M", ci("George S. Clason", "1926", "«O Homem Mais Rico da Babilônia»", "De cada dez moedas, gaste no máximo nove. A décima é sua.")),
      ("gaste no máximo", "M", ic([("🪙", "9 moedas: para viver", False), ("💰", "1 moeda: para ficar", False)], "A primeira lição")),
      ("continua de pé", "C", tiao("P3", 1))],
 14: [("^", "M", so("marcos", "P05")), ("Nada", "M", fr("O que sobra no fim do mês dele: *nada*.")),
      ("Cyril Parkinson", "M", ci("C. Northcote Parkinson", "1960", "livro «The Law and the Profits»", "Os gastos sobem até encostar no que a gente ganha.")),
      ("me pago primeiro", "C", tiao("P2", 1))],
 15: [("^", "C", tiao("P3", -1)), ("agendei", "M", cel("Agendado", [("Todo dia 5", "R$ 280,00", True), ("Repetir", "sempre", True)], [0])),
      ("Richard Thaler", "M", ci("Richard Thaler e Shlomo Benartzi", "2004", "estudo «Save More Tomorrow» (Nobel de Thaler: 2017)", "A poupança no automático subiu de 3,5% para 13,6% do salário em 40 meses.")),
      ("treze e meio", "M", ba([("Antes", 3.5, VERM), ("40 meses depois", 13.6, VERDE)], "Quanto do salário era guardado (%)", fmt="num")),
      ("força de vontade perde", "C", tiao("P4", 1))],
 16: [("^", "M", nu(3360, "Em um ano", "R$ 280 por mês", cor=VERDE, emoji="📅")), ("quarto mês", "M", li(["mês 1", "mês 2", "mês 3", "mês 4"], 3, "Passei dos R$ 1.000")),
      ("outra vida", "C", tiao("P1", 1))],
 17: [("^", "M", ic([("🐷", "R$ 280 para a reserva", False), ("🎉", "R$ 180 para o prazer", False), ("🧰", "R$ 100 para o que der e vier", False)], "Dinheiro com nome")),
      ("like", "C", tiao("P2", -1)), ("mais pesada", "C", tiao("P4", 1))],
 # 3. A casa e a panela
 18: [("^", "M", regra(3, "a casa manda em todas as outras contas", "🏠")), ("setecentos e cinquenta", "M", nu(750, "O meu aluguel", "uns 27% do salário", emoji="🏠")),
      ("bairros bonitos", "C", tiao("P2", 1)), ("ninguém paga", "C", tiao("P3", -1))],
 19: [("^", "C", tiao("P2", -1)),
      ("Pesquisa de Orçamentos Familiares", "M", ci("IBGE", "2017-2018", "Pesquisa de Orçamentos Familiares", "A moradia é o maior gasto das famílias: 36,6% de tudo o que consomem.")),
      ("chega perto de quarenta", "M", nu(39.2, "Nas famílias que ganham menos", "IBGE, POF 2017-2018", cor=VERM, casas=1, fmt="num", suf="%", emoji="🏠"))],
 20: [("^", "M", so("sandra", "P03")),
      ("O meu salário inteiro", "M", ba([("Aluguel do Tião", 750, VERDE), ("Aluguel que a Sandra quer", 2800, VERM)], "Só para morar, por mês")),
      ("vinte e quatro mil", "M", nu(24600, "A mais, em um ano", cor=VERM, emoji="📅")), ("caneta", "M", so("marcos", "P06"))],
 21: [("^", "C", tiao("P2", -1)), ("teto", "M", fr("Um *terço* da renda é o teto da casa.")), ("ganha no sono", "C", tiao("P3", 1))],
 22: [("^", "M", regra(4, "comida feita em casa e mercado com lista", "🛒")), ("setecentos e cinquenta por mês", "M", nu(750, "Mercado por mês", "uns R$ 25 por dia", emoji="🛒")),
      ("lista no celular", "M", cel("Lista do sábado", [("Arroz", "✓", True), ("Feijão", "✓", True), ("Ovos", "✓", True), ("Frango", "✓", True)], []))],
 23: [("^", "C", tiao("P4", -1)), ("biscoito", "M", ic([("🍪", "biscoito", True), ("🥤", "refrigerante", True), ("🍕", "comida pronta", True)], "Nada disso estava na lista")),
      ("A base", "M", ic([("🍚", "arroz", False), ("🫘", "feijão", False), ("🥚", "ovo", False), ("🍗", "frango", False), ("🥕", "legume da época", False)], "A base")),
      ("marmita", "M", fr("Uma panela grande = a *marmita* da semana."))],
 24: [("^", "M", so("marcos", "P03", noite=True)), ("dia inteiro", "M", fr("Um pedido do Marcos = o meu *dia inteiro* de comida.")),
      ("Exceção", "C", tiao("P1", 1)), ("perigo", "C", tiao("P4", -1))],
 # 4. O dia vinte
 25: [("^", "M", regra(5, "não parcele o que não pode pagar à vista", "💳")), ("doze de cento e vinte", "M", fr("*12 × R$ 120*", "cabe no bolso?")),
      ("preço de não esperar", "M", nu(1440, "O mesmo celular, parcelado", "R$ 240 a mais", cor=VERM, emoji="📱"))],
 26: [("^", "C", tiao("P2", 1)), ("cento e oitenta", "M", nu(180, "Só a tela nova", "à vista", cor=VERDE, emoji="✅")),
      ("trinta dias", "M", ic([("⏳", "não cabe à vista? espera 30 dias", False), ("🐷", "ainda quer? junta antes", False), ("💳", "fatura do cartão: paga inteira", False)], "A regra 5 em três partes"))],
 27: [("^", "C", tiao("P4", 1)), ("cheque especial", "M", fr("Cheque especial = o *limite* que o banco cola na sua conta")),
      ("oito por cento", "M", nu(8, "O teto do cheque especial", "Resolução CMN 4.765/2019, art. 3º", cor=VERM, fmt="int", suf="% ao mês", emoji="🔥")),
      ("sete e meio", "M", nu(7.53, "A média em setembro de 2026", "Banco Central (SGS 25463)", cor=VERM, casas=2, fmt="num", suf="% ao mês", emoji="📈"))],
 28: [("^", "C", tiao("P2", -1)),
      ("oitenta e um", "M", nu(81.6, "Famílias com dívida", "CNC, pesquisa Peic, outubro de 2026", cor=VERM, casas=1, fmt="num", suf="%", emoji="🧾")),
      ("conta atrasada", "M", nu(29.3, "Com conta em atraso", "CNC, pesquisa Peic, outubro de 2026", cor=VERM, casas=1, fmt="num", suf="%", emoji="⏰")),
      ("oitenta e quatro milhões", "M", nu(84.2, "Brasileiros com o nome negativado", "Serasa, setembro de 2026", cor=VERM, casas=1, fmt="num", suf=" milhões", emoji="📉"))],
 29: [("^", "C", tiao("P1", 1)),
      ("dificuldade para dormir", "M", nu(83, "Endividados com dificuldade para dormir", "Serasa e Opinion Box, 5.225 pessoas", cor=VERM, fmt="int", suf="%", emoji="🌙")),
      ("sessenta e cinco estudos", "M", ci("Richardson, Elliott e Roberts", "2013", "revista Clinical Psychology Review (65 estudos)", "Quem tem dívida tem cerca de 3 vezes mais chance de um problema de saúde mental.")),
      ("tira o sono", "C", tiao("P4", -1))],
 30: [("^", "M", ic([("📱", "o celular", False), ("🛋️", "o sofá", False), ("🔥", "a churrasqueira", False), ("🎁", "até o presente da Sandra", False)], "O Marcos parcela tudo")),
      ("se empilham", "M", so("marcos", "P07"))],
 31: [("^", "C", tiao("P1", -1)), ("primeiro degrau", "M", fr("Não é bronca. É o *primeiro degrau*."))],
 32: [("^", "C", tiao("P4", 1)), ("ganha o triplo", "M", ba([("Eu, o Tião", 2800, VERDE), ("O Marcos", 8400, VERM)], "Salário por mês")),
      ("fila do açougue", "M", so("marcos", "P01"))],
 33: [("^", "M", rua_dia([DE("marcos", 700), DE("tiao", 1100), DE("sandra", 1450)], carro=False)),
      ("não passou", "M", cel("Maquininha do açougue", [("Cartão do Marcos", "RECUSADO", False)], [0])),
      ("rindo alto", "M", so("marcos", "P01", "Tião, paga aí a carne do churrasco, que dia cinco eu te devolvo!", "Tião", "devolvo")),
      ("Cem reais", "M", nu(100, "A carne do churrasco", "paga pelo porteiro", emoji="🥩")), ("quase tudo", "C", tiao("P4", -1))],
 34: [("^", "C", tiao("P2", 1)), ("risada", "C", tiao("P3", -1)), ("quase invisível", "C", tiao("P4", 1))],
 # 5. A linha do extrato
 35: [("^", "M", regra(6, "corte o que você paga e não usa", "✂️")), ("Volta comigo", "M", dom_larga([TS_D(), VS_D(("P18", None))])),
      ("passando o dedo", "M", perto_v(("P08", None))), ("parou numa linha", "M", extrato([2])),
      ("Ficou branca", "M", perto_v(("P03", None), baloes=[B("Tião, isso aqui sai todo mês?", 0, "Tião", "mês", **VE_B)]))],
 36: [("^", "M", extrato([2])), ("mês anterior", "M", li(["março", "abril", "maio", "...", "outubro"], 4, "Juros cheque especial: R$ 188,25 todo mês")),
      ("desde março", "C", tiao("P4", 1))],
 37: [("^", "M", perto_v(("P11", None), baloes=[B("Mas eu nunca usei cheque especial, Tião! Eu nem tenho talão de cheque!", 0, "Mas", "cheque", **VE_B)])),
      ("antigamente", "C", tiao("P2", -1)), ("todo dia dez", "M", fr("A conta descia do *zero* todo dia 10.")),
      ("sete e meio", "M", nu(7.53, "Juros por mês, em média", "Banco Central, setembro de 2026", cor=VERM, casas=2, fmt="num", suf="%", emoji="📈"))],
 38: [("^", "M", extrato([1])), ("duas assinaturas", "M", ic([("🎬", "filme", False), ("🎵", "música", False)], "Assinaturas esquecidas")),
      ("criou perna", "C", tiao("P4", -1))],
 39: [("^", "M", conta("As duas linhas no ano", [("Juros do limite", -2259.00), ("Pacote de serviços", -658.80)], total="Por ano")),
      ("Quase três mil", "M", nu(2917.80, "Por ano, para o banco", cor=VERM, casas=2, emoji="😱"))],
 40: [("^", "M", nu(10, "Os dez minutos", cor=VERDE, fmt="int", suf=" min", emoji="⏱️")), ("Cancelou", "M", ic([("📺", "cancelou as 2 assinaturas", False)], "Minuto 1")),
      ("baixar o limite", "M", ic([("📉", "baixou o limite do cheque especial", False)], "Minuto 4")),
      ("serviços essenciais", "M", ic([("✂️", "trocou a cesta pelos serviços grátis", False)], "Minuto 9"))],
 41: [("^", "C", tiao("P2", 1)), ("cartão de débito", "M", ic([("💳", "cartão de débito", False), ("🏧", "até 4 saques por mês", False), ("🔁", "até 2 transferências no mesmo banco", False),
                                                              ("🧾", "até 2 extratos por mês", False), ("📱", "consultas pela internet", False)], "De graça por regra (Res. CMN 3.919, art. 2º)")),
      ("quem escolhe", "M", fr("Pagar *pacote* ou só o que usa: quem escolhe é o cliente.", "Resolução CMN 3.919/2010, art. 9º"))],
 42: [("^", "C", tiao("P4", -1)), ("olhar o meu extrato", "M", rua_noite([TI(("P14", None), x=1250)])),
      ("cesta de serviços", "M", cel("O extrato do Tião", [("Salário", "+ 2.800,00", True), ("Cesta de serviços", "- 12,90", False)], [1])),
      ("Novecentos e vinte e oito", "M", nu(928.80, "Seis anos de cesta", "R$ 12,90 × 72 meses", cor=VERM, casas=2, emoji="😳"))],
 43: [("^", "C", tiao("P3", 1)), ("três meses", "M", fr("A cada *3 meses*: um dia só para ler o extrato.")), ("dorme", "C", tiao("P1", -1))],
 44: [("^", "C", tiao("P2", 1)), ("só o número", "M", fr("Comenta *só o número*: quanto era a linha estranha do seu extrato")),
      ("o carro", "C", tiao("P4", -1))],
 # 6. O carro e o prazer
 45: [("^", "M", regra(7, "pense duas vezes antes de usar o carro todo dia", "🚌")), ("branco de dois mil e um", "M", rua_dia([DE("tiao", 1100)])),
      ("vale-transporte", "M", fr("O patrão paga o que passar de *6% do salário*", "Lei 7.418/1985, art. 4º")),
      ("cento e sessenta e oito", "M", nu(168, "O que eu pago de ônibus", "6% de R$ 2.800", cor=VERDE, emoji="🚌"))],
 46: [("^", "C", tiao("P2", -1)), ("seiscentos", "M", ba([("De ônibus", 168, VERDE), ("De carro, todo dia", 600, VERM)], "O meu transporte, por mês")),
      ("trabalha no sábado", "M", ic([("🧺", "a feira", False), ("🌳", "um passeio", False), ("🚑", "uma emergência", False)], "O carro velho, no sábado")),
      ("cento e noventa", "M", nu(190, "O carro velho, por mês", "e eu sei para que ele serve", cor=VERDE, emoji="🚗"))],
 47: [("^", "M", so("marcos", "P08")), ("Parcela", "M", conta("A picape do Marcos, por mês", [("Parcela", -2890), ("Seguro", -380), ("Combustível", -600),
                                                                                              ("Imposto e manutenção", -250)], total="Por mês")),
      ("Quase metade", "M", ba([("A picape", 4120, VERM), ("O salário dele", 8400, VERDE)], "O Marcos, por mês")), ("ri do meu carro", "C", tiao("P3", 1))],
 48: [("^", "C", tiao("P2", -1)), ("trabalhando para o carro", "C", tiao("P3", 1)), ("usado, à vista", "M", fr("Quando cansar: *usado*, à vista e com calma."))],
 49: [("^", "M", regra(8, "separe dinheiro para o prazer e gaste sem culpa", "🍦")), ("cento e oitenta reais", "M", nu(180, "Por mês, só para o prazer", cor=VERDE, emoji="🍦"))],
 50: [("^", "M", ic([("🍦", "sorvete na praça", False), ("⚽", "futebol de sábado", False), ("🎬", "cinema no dia da promoção", False), ("🍽️", "almoço fora, 1 vez por mês", False)], "Prazer planejado")),
      ("de graça", "M", ic([("🌳", "o parque", False), ("🎪", "a festa de rua", False), ("🎟️", "o evento da prefeitura", False)], "De graça")),
      ("acabou", "C", tiao("P3", 1))],
 51: [("^", "C", tiao("P1", -1)), ("essa regra é sua", "C", tiao("P2", 1)), ("meio termo", "M", fr("O *meio termo* é onde a vida acontece."))],
 52: [("^", "M", ba([("A Sandra, para tirar foto", 600, VERM), ("O Tião, o prazer todo", 180, VERDE)], "Por mês")), ("volto de um sábado", "M", so("sandra", "P03")),
      ("estar ali", "C", tiao("P2", -1))],
 53: [("^", "C", tiao("P4", 1))],
 # 7. O que a rua nao viu
 54: [("^", "M", regra(9, "o dinheiro sobe, o padrão fica", "📈")), ("décimo terceiro", "M", fr("1ª metade do *13º*: até 30 de novembro", "Lei 4.749/1965, art. 2º")),
      ("vinte de dezembro", "M", fr("O resto: até *20 de dezembro*", "Lei 4.749/1965, art. 1º")), ("mil e quatrocentos", "M", nu(1400, "O meu agora", emoji="💰"))],
 55: [("^", "M", ic([("📱", "celular novo", True), ("👕", "roupa nova", True), ("🍽️", "jantar fora", True)], "Em janeiro, nada")),
      ("esteira hedônica", "M", ci("Philip Brickman e Donald Campbell", "1971", "a «esteira hedônica»", "A alegria de ganhar mais passa rápido: a gente se acostuma e logo quer mais.")),
      ("não sai do lugar", "C", tiao("P4", -1))],
 56: [("^", "M", conta("O 13º do Tião", [("Primeira metade", 1400), ("Para a reserva", -700), ("Para viver melhor", -700)], total="Decidido antes", neutro=True)),
      ("cabeça fria", "C", tiao("P3", 1))],
 57: [("^", "M", so("marcos", "P04")), ("sete mil para oito mil e quatrocentos", "M", ba([("Antes", 7000, VERDE), ("Depois do aumento", 8400, VERDE)], "O salário do Marcos")),
      ("vantagem escondida", "C", tiao("P2", -1)), ("recado rápido", "C", tiao("P2", 1))],
 58: [("^", "C", tiao("P2", 1)), ("balanço", "V", "banco:FM:4-balanco/balanco__estilo-donut-despesas__horizontal.mp4"),
      ("décimo terceiro cair", "M", conta("O 13º no balanço", [("Primeira metade", 1400), ("Fatia da reserva", -700), ("Fatia da vida", -700)], total="Tudo com destino", neutro=True)),
      ("os juros e as tarifas", "M", ic([("💸", "Juros do cheque especial", False), ("🧾", "Cesta de serviços", False)], "Uma fatia só para eles")),
      ("sete dias", "M", nu(7, "Dá para testar o FinMoovi", "link na descrição · www.finmoovi.com", cor=VERDE, fmt="int", suf=" dias", emoji="📱"))],
 # 8. A ultima regra
 59: [("^", "M", regra(10, "compare-se só com você mesmo, de um ano atrás", "🪞")), ("Sandra posta", "M", so("sandra", "P03")),
      ("peito aperta", "C", tiao("P1", -1)), ("ninguém posta o depois", "M", ic([("🧾", "a fatura", False), ("💢", "a briga", False), ("🌙", "a noite sem dormir", False)], "O que ninguém posta"))],
 60: [("^", "C", tiao("P3", 1)),
      ("Morgan Housel", "M", ci("Morgan Housel", "2020", "livro «A Psicologia Financeira»", "A habilidade mais difícil: parar de mudar a linha de chegada e saber quando é suficiente.")),
      ("nunca chega", "C", tiao("P4", -1))],
 61: [("^", "M", ic([("❓", "não sabia para onde ia o dinheiro", True), ("0️⃣", "zero guardado", True), ("😟", "medo", True)], "Um ano atrás")),
      ("Hoje eu sei", "M", ic([("🧭", "sei para onde vai cada real", False), ("🐷", "tenho reserva", False), ("😴", "durmo", False)], "Hoje")),
      ("única comparação", "C", tiao("P2", -1))],
 62: [("^", "M", nu(650, "A geladeira pifou", "paga à vista, com a reserva", cor=VERDE, emoji="🧊")), ("Respirei", "C", tiao("P1", 1)),
      ("Caneca velha", "M", foco(*CANECA_D))],
 63: [("^", "M", rua_dia([DE("marcos", 900)], carro=False)), ("carta do banco", "M", fr("*Parcela da picape*: em atraso")),
      ("a Valéria contou", "M", so("marcos", "P07", "Tião, a Valéria contou para a Sandra que você fez uma conta com ela, e que ela parou de afundar. Me ensina essa conta?", "Tião", "conta"))],
 64: [("^", "C", tiao("P2", 1)), ("A picape", "M", conta("No verso da carta do banco", [("Salário", 8400), ("A picape", -4120), ("Aluguel, parcelas e aplicativo", -3980)], total="Sobram")),
      ("trezentos reais", "M", nu(300, "O que sobrava ao Marcos", "de R$ 8.400", cor=VERM, emoji="😶")),
      ("A Sandra vai me matar", "M", so("marcos", "P02", "A Sandra vai me matar.", "A Sandra", "matar")), ("Vamos ver", "C", tiao("P3", 1))],
 65: [("^", "M", rua_dia([P("valeria", 1100, 960, 600, ("R4", None)), DE("marcos", 500)], carro=False)),
      ("bilhete", "M", fr("A desculpa dela: num *bilhete*, escondida.", "Em público, nunca.")),
      ("Boa tarde", "M", so("valeria", "P15", "Boa tarde, Tião.", "Boa", "Tião")), ("primeiro passo", "C", tiao("P1", -1))],
 66: [("^", "C", tiao("P2", 1)), ("distância", "M", fr("Tranquilidade = o que você *ganha* menos o que você *precisa*")),
      ("dorme em paz", "C", tiao("P3", -1))],
 # 9. O proximo
 67: [("^", "M", so("cida", "P01")), ("Me passa o seu", "M", so("cida", "P04", "Me passa o seu CPF, que tem desconto.", "Me", "desconto")),
      ("Cadastro de Pessoas Físicas", "M", fr("*CPF*: o número do Cadastro de Pessoas Físicas")), ("desconfiou", "M", so("cida", "P04"))],
 68: [("^", "M", cel("Mensagem nova", [("Olá, Dona Cida!", "", True), ("Sobre o seu remédio de pressão...", "", False)], [1])),
      ("me olhou", "M", so("cida", "P03", "Tião, como é que eles sabem disso?", "Tião", "disso"))],
 69: [("^", "M", fr("Como as farmácias ganham *dinheiro*?", "Não é o remédio")), ("esse próximo vídeo", "C", tiao("P2", 1))],
}
