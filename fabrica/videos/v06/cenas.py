# Cenas do video 06 (Tiao Conversa, o salario que acaba no dia 10). Roteiro: roteiros/06-salario-dia-10.md.
# 26/11/2026: sai sem nenhuma imagem nova. O Tiao fala com quem assiste nas poses P1 a P4 (o fundo do 03 e do 04), e as
# lembrancas daquele domingo sao cenas da turma viva nos cenarios do 05 (varanda de domingo, rua, noite), com as poses
# oficiais. Os numeros vao nos cartoes do kit (celular com o extrato, a conta no papel de pao). So a capa vai ao Ed (Team).
from fabrica.kit import *
from fabrica.videos.v05.cenas import (P, B, T, VE, TI, GE, DE, TS_D, VS_D, dom_larga, dom_perto, rua_dia, rua_noite, foco, cel, conta,
                                      CANECA_D, BT, VD)
from fabrica.videos.v03.cenas import IMG as _I3

RUA = "fundo-banquinho"
IMG = {k: _I3[k] for k in ("fundo-banquinho", "selo-tiao-cafe")}
_V = "valeria-ficha-a.jpg.jpg + tiao-ficha-oficial.jpg"  # no Drive o arquivo chama-se assim (como no 05)
TITULO = "Seu Salário Acaba no Dia 10? O Problema Não É o Salário"
CAPA_TEXTO = "SAI TODO MÊS?!"
# 26/11 (Ed: «quero que as thumbs de videos longos a partir de agora saia ja com textos»): o texto vai DENTRO do prompt da
# capa (pedidos.py), o meta.ai desenha. Por capa: (texto exato, a parte em destaque, cor do destaque). Nunca repete o titulo.
CAPA_LETRAS = {"A": ("SAI TODO MÊS?!", "TODO MÊS", "vermelho"), "B": ("O BANCO AGRADECE", "AGRADECE", "amarelo"),
               "C": ("R$ 188 POR MÊS", "R$ 188", "vermelho"), "D": ("ATÉ O TIÃO?!", "TIÃO", "amarelo")}
VINHETA = 3  # a vinheta entra depois da fala 3 («Vamos começar?»)
PUBLICA = "2026-11-27 10:00"
PUBLICA_TXT = "sexta, 27/11, às 10h (Brasília, 13h em Lisboa)"
PRAZO = "quinta, 26/11, até as 20h (o vídeo vai ao ar sexta às 10h)"
PRAZO_ISO = "2026-11-26T20:00:00-03:00"
CAPA = (_V, "ALERT mood, strong red background with a dark vignette. Close-up: Valeria, elegant woman in a white blazer, sunglasses pushed up on her head, "
            "big on the RIGHT, pale with shock, mouth open, holding a smartphone with a pink case toward the viewer: on the bright screen, ONE line of a "
            "bank statement is highlighted with a thick red marker (scribbles only, nothing readable). Behind her, out of focus, Tiao holding a plain white "
            "enamel mug with a chipped rim, one eyebrow up. Leave the left half empty for the title text. No text, no letters, no numbers anywhere (the title goes on later).",
        "valeria-linha")
CAPAS_TESTE = [
    (_V, "MONEY LEAK mood, deep blue and red. A big pink-case smartphone in the center seen close: banknotes are leaking out of its screen and dripping down "
         "into a bank vault below. Valeria (LEFT) covers her mouth in shock; Tiao (RIGHT), big and close, points at the phone with a short yellow carpenter "
         "pencil. Leave the top third empty for the title text. No text, no letters, no numbers anywhere (the title goes on later).", "celular-vaza"),
    (_V, "TIME PRESSURE mood, warm yellow and red. A big wall calendar behind them with the day 10 circled in thick red (only the shape of the circle, no numbers). "
         "Valeria (RIGHT) holds an empty wallet open upside down, desperate; Tiao (LEFT), calm, sips from his plain white chipped mug, knowing look. "
         "Leave the top third empty for the title text. No text, no letters, no numbers anywhere (the title goes on later).", "calendario-10"),
    ("tiao-ficha-oficial.jpg", "SHOCK mood, cold blue and red. Tiao alone, big and close on the RIGHT, at his kitchen at night, holding his phone with both hands, "
         "eyes wide open, a drop of sweat, his white chipped mug next to him; the phone light on his face. Leave the left half empty for the title text. "
         "No text, no letters, no numbers anywhere (the title goes on later).", "tiao-susto"),
]
DESC = ("O salário da Valéria é de R$ 8.700, e mesmo assim, todo mês, no dia 10, já tinha acabado. Num domingo, na varanda do Tião, ela passou o dedo "
        "no extrato, linha por linha, e parou numa: juros do cheque especial, R$ 188,25. Todo mês.\n\n"
        "Neste vídeo o Tião mostra, com as regras do Banco Central na mão, o que era aquela linha, por que o saldo do aplicativo mistura o seu dinheiro "
        "com o limite do banco, quanto aquilo levava dela por ano, os serviços que o banco não pode cobrar, e o que ela fez em dez minutos na mesinha. "
        "E o susto que o próprio Tião levou no extrato dele.")
TAGS = ["cheque especial", "juros do cheque especial", "salário acaba", "salário no dia 10", "tarifa bancária", "pacote de serviços", "cesta de serviços",
        "serviços essenciais gratuitos", "limite da conta", "educação financeira", "finanças pessoais", "Tião Poupador", "Tião Conversa"]
PERGUNTA = "Quanto você paga de pacote de serviços por mês? Só o número."
CAP_NOMES = {"Abertura (é um Reels: entende-se sozinha)": "R$ 188,25 todo mês", "A linha": "A linha do extrato",
             "O sábado em que riram do extrato": "Riram do extrato", "O saldo que mentia": "O saldo que mentia",
             "Quanto levava por ano": "Quanto levava por ano", "Os dez minutos na mesinha": "Os dez minutos na mesinha",
             "O meu susto": "O susto do Tião", "O próximo": "A nota da farmácia"}
FORTES = {"extrato", "limite", "juros", "cheque", "salário", "pacote", "tarifa", "valéria", "saldo", "dica", "banco"}
GIF = "foto"
PLAYLIST = "tiao-conversa"
# novela.md 11 e 28: o clima troca a cada 2 ou 3 min, sem repetir faixa
CLIMA = {0: "alerta", 4: "calma", 7: "curiosa", 10: "humor", 13: "tensao", 15: "tensao", 18: "drama", 22: "alerta", 24: "drama", 27: "humor",
         30: "virada", 36: "reflexiva", 37: "curiosa", 40: "tensao", 42: "drama", 45: "humor", 46: "reflexiva", 49: "virada", 50: "final",
         52: "curiosa", 53: "tensao"}
AMB = [("passaros", 4, "^", 20, 0.2), ("passaros", 15, "^", 20, 0.2), ("passaros", 23, "^", 20, 0.2), ("passaros", 30, "^", 20, 0.2),
       ("grilos", 37, "^", 14, 0.2), ("grilos", 40, "^", 25, 0.2)]

# ---------- as pecas que se repetem ----------
def tiao(pose, lado=1): return (RUA, pose, lado)
def extrato(destaque=(), linhas=None):
    linhas = linhas or [("Salário", "+ 8.700,00", True), ("Parcela do carro", "- 4.555,56", False), ("Aluguel", "- 3.900,00", False),
                        ("Pacote de serviços", "- 54,90", False), ("Juros cheque especial", "- 188,25", False)]
    return cel("Extrato · conta do salário", linhas, destaque)
SALDO = cel("Saldo disponível", [("Saldo disponível", "2.444,00", True)], [0])
DETALHE = cel("Toque no número", [("Saldo da conta", "- 3.556,00", False), ("Limite cheque especial", "6.000,00", True),
                                   ("Saldo disponível", "2.444,00", True)], [0])
AUMENTO = cel("Parabéns!", [("Seu limite aumentou para", "6.000,00", True), ("Botão verde", "ACEITAR", True)], [1])
DOM = lambda *g, **kw: dom_larga([TS_D(*g)], **kw)
def dupla(t_pose=("P16", None), v_pose=("P17", None), baloes=()): return dom_larga([TS_D(t_pose), VS_D(v_pose)], baloes)
VE_B = dict(x=110, y=40, larg=1080, rabo=(640, 470))  # balao de quem esta a esquerda (Valeria de perto, vizinho em x=700)
def perto_v(*poses, baloes=(), x=600): return dom_perto([VE(*poses, x=x)], baloes)
def perto_t(*poses, baloes=(), x=1250): return dom_perto([TI(*poses, x=x)], baloes)
def calcada(baloes=(), gente=None):
    return rua_dia(gente or [DE("sandra", 360), DE("rafa", 600), DE("tiao", 1500), P("valeria", 1000, 960, 600, ("R1", None))], baloes)
CIDA_NOITE = lambda b=(): rua_noite([GE("cida", ("P01", None), x=700)], b)

L = {
 # 0. Abertura (Reels)
 0: [("^", "M", nu(188.25, "Juros do cheque especial", "todo mês, no extrato da Valéria", cor=VERM, casas=2, emoji="😱")),
     ("Para o banco", "M", extrato([4])), ("ficou branca", "M", perto_v(("P03", None), baloes=[B("Tião, eu nunca pedi isso.", 0, "Tião", "isso", **VE_B)]))],
 1: [("^", "M", nu(8700, "O salário dela", "e no dia 10 já tinha acabado", emoji="💸")), ("Não era o salário", "C", tiao("P4", 1))],
 2: [("^", "M", ic([("🔍", "o que ela achou na linha", False), ("📅", "quanto levava por ano", False), ("⏱️", "o que ela fez em 10 minutos", False)], "Hoje, três coisas")),
     ("susto", "C", tiao("P4", -1))],
 3: [("^", "C", tiao("P2", 1)), ("puxa a cadeira", "M", dom_larga())],
 # 1. A linha
 4: [("^", "M", perto_t(("P08", None), x=960))],
 5: [("^", "C", tiao("P1", 1)), ("porteiro", "C", tiao("P2", -1)), ("caneca branca", "M", foco(*CANECA_D)), ("papel de pão", "M", DOM(("P17", None)))],
 6: [("^", "M", dupla()), ("puxou do celular", "M", perto_v(("P08", None))), ("parou numa", "M", extrato([4])),
     ("ficou branca", "M", perto_v(("P03", None), baloes=[B("Tião... isso aqui sai todo mês?", 0, "Tião", "mês", **VE_B)]))],
 7: [("^", "M", extrato([4])), ("mês anterior", "M", li(["março", "abril", "maio", "...", "outubro"], 4, "Juros cheque especial: R$ 188,25 todo mês")),
     ("desde março", "C", tiao("P4", 1))],
 8: [("^", "M", perto_v(("P11", None), baloes=[B("Mas eu nunca usei cheque especial, Tião!", 0, "Mas", "Tião", **VE_B)])),
     ("armadilha", "C", tiao("P3", -1)), ("Hoje, cheque especial", "M", fr("Cheque especial = o *limite* que o banco cola na sua conta", "Resolução CMN 4.765/2019, art. 1º"))],
 9: [("^", "C", tiao("P2", 1)), ("sete vírgula", "M", nu(7.53, "Juros médios do cheque especial", "setembro de 2026, Banco Central (SGS 25463)", cor=VERM, casas=2, fmt="num", suf="% ao mês", emoji="🔥")),
     ("cento e trinta e nove", "M", nu(139.02, "No ano", "Banco Central (SGS 20741)", cor=VERM, casas=2, fmt="num", suf="% ao ano", emoji="📈"))],
 # 2. O sabado em que riram do extrato
 10: [("^", "C", tiao("P1", -1)), ("No sábado", "M", calcada()), ("soltei uma frase", "M", calcada([B("Quem lê o extrato no dia que o salário cai nunca é pego de surpresa.", 2, "Gente", "surpresa", x=900, larg=1000)]))],
 11: [("^", "M", rua_dia([GE("sandra", ("P01", None), x=700)], [B("Tião, extrato de porteiro tem duas linhas: entrou e saiu!", 0, "extrato de porteiro", "saiu", **VE_B)])),
      ("rua inteira riu", "M", calcada()), ("Rafa", "M", rua_dia([GE("rafa", ("P02", None), x=700)], [B("Eu nem abro extrato, Tião. Eu olho o saldo e pronto.", 0, "Eu nem abro", "pronto", **VE_B)]))],
 12: [("^", "M", rua_dia([GE("valeria", ("P12", None), x=700)])), ("fiquei quieto", "M", rua_dia([TI(("P19", None), x=1250)], carro=False)),
      ("Dica de porteiro", "C", tiao("P1", 1))],
 13: [("^", "C", tiao("P4", -1)), ("só o saldo", "M", cel("O meu aplicativo", [("Saldo", "olhado de passagem", True)], [0])), ("seis anos", "C", tiao("P4", 1))],
 14: [("^", "C", tiao("P2", -1))],
 # 3. O saldo que mentia
 15: [("^", "M", dupla()), ("aplicativo do banco", "M", perto_v(("P08", None))), ("saldo disponível", "M", SALDO)],
 16: [("^", "M", perto_v(("P02", None), baloes=[B("Olha aqui, Tião. Eu tenho dinheiro!", 0, "Olha", "dinheiro", **VE_B)])),
      ("toquei no número", "M", DETALHE), ("nunca tinha sido", "C", tiao("P4", 1))],
 17: [("^", "C", tiao("P2", -1)), ("engloba", "M", fr("O saldo disponível *engloba* o limite de crédito", "Resolução CMN 3.919/2010, art. 17, site do Banco Central")),
      ("Quer dizer", "C", tiao("P3", 1))],
 18: [("^", "M", perto_v(("P04", None), baloes=[B("Mas o meu limite era de mil reais.", 0, "Mas", "reais", **VE_B)])), ("aviso com confete", "M", AUMENTO),
      ("Achou que era presente", "M", perto_v(("P11", None)))],
 19: [("^", "C", tiao("P3", -1)), ("autorização do cliente", "M", fr("Aumento de limite só com a *autorização do cliente*, a cada oferta", "Resolução CMN 4.765/2019, art. 4º, § 2º, II")),
      ("cinco mil reais", "C", tiao("P4", 1))],
 20: [("^", "C", tiao("P1", -1)), ("Na primeira", "M", ic([("💳", "aluguel no cartão", False), ("🔥", "caiu no rotativo", True)], "Tentativa 1")),
      ("Na segunda", "M", ic([("🔁", "tudo no crédito", False), ("🕳️", "o buraco só mudou de lugar", True)], "Tentativa 2"))],
 21: [("^", "C", tiao("P2", 1)), ("Pois é", "C", tiao("P4", -1))],
 # 4. Quanto levava por ano
 22: [("^", "C", tiao("P4", 1)), ("Cento e oitenta", "M", nu(188.25, "Juros do cheque especial", "todo mês", cor=VERM, casas=2, emoji="😱")),
      ("ficou branca", "M", perto_v(("P03", None), baloes=[B("Tião, eu nunca pedi isso.", 0, "Tião", "isso", **VE_B)]))],
 23: [("^", "M", DOM(("P17", None))), ("vezes doze", "M", nu(2259, "Por ano, só de juros do limite", "R$ 188,25 × 12 meses", cor=VERM, emoji="📅"))],
 24: [("^", "M", perto_v(("P08", None))), ("Duas linhas abaixo", "M", extrato([3])), ("criou perna", "C", tiao("P4", -1))],
 25: [("^", "C", tiao("P2", 1)), ("serviços essenciais", "M", ic([("💳", "cartão de débito", False), ("🏧", "até 4 saques por mês", False), ("🔁", "até 2 transferências no mesmo banco", False),
                                                                  ("🧾", "até 2 extratos por mês", False), ("📱", "consultas pela internet", False)], "De graça por regra (Res. CMN 3.919, art. 2º)")),
      ("pagava por um pacote", "C", tiao("P3", -1))],
 26: [("^", "M", conta("As duas linhas no ano", [("Juros do limite", -2259.00), ("Pacote de serviços", -658.80)], total="Por ano")),
      ("geladeira", "M", nu(2917.80, "Quase três mil reais por ano", "para o banco", cor=VERM, casas=2, emoji="🧊"))],
 27: [("^", "M", dom_larga([TS_D(), VS_D(), P("rafa", 1500, 960, 600, ("R1", None))])),
      ("Tião, consegui", "M", dom_perto([GE("rafa", ("P02", None), x=700)], [B("Tião, consegui! Tenho dois mil no banco!", 0, "consegui", "banco", **VE_B)])),
      ("toca no número", "M", perto_v(("P01", None), baloes=[B("Rafa, toca no número do saldo.", 0, "Rafa", "saldo", **VE_B)])),
      ("Trinta e dois", "M", cel("O saldo do Rafa", [("Saldo da conta", "32,00", True), ("O resto", "é limite", False)], [0])),
      ("Dona Cida riu", "M", rua_dia([GE("cida", ("P02", None), x=700)], carro=False)),
      ("regador", "M", rua_dia([GE("sandra", ("P06", None), x=1300)], carro=False))],
 28: [("^", "M", perto_v(("P15", None), baloes=[B("Tião, me ajuda a desligar isso. Agora.", 0, "me ajuda", "Agora", **VE_B)])),
      ("dez minutos", "M", nu(10, "Minutos na mesinha", cor=VERDE, fmt="int", suf=" min", emoji="⏱️")),
      ("A Sandra riu", "M", rua_dia([GE("sandra", ("P03", None), x=1300)], carro=False))],
 29: [("^", "C", tiao("P2", -1))],
 # 5. Os dez minutos na mesinha
 30: [("^", "M", dupla()), ("Repete", "M", perto_v(("P11", None), baloes=[B("Aquela frase que você falou sábado... Repete.", 0, "Aquela", "Repete", **VE_B)])),
      ("Quem lê o extrato", "M", perto_t(("P10", None)))],
 31: [("^", "M", ic([("🔍", "lê o extrato linha por linha no dia que o salário cai", False)], "Dica 1")), ("Tarifa e juros", "C", tiao("P3", 1))],
 32: [("^", "M", ic([("➖", "o seu saldo é o da conta, sem o limite", False)], "Dica 2")), ("sinal de menos", "M", DETALHE)],
 33: [("^", "M", ic([("✂️", "cancelou o pacote de serviços", False)], "1")), ("direito do cliente", "M", fr("É *prerrogativa do cliente* pagar só os serviços avulsos",
                                                                                                           "Resolução CMN 3.919/2010, art. 9º")),
      ("quase zero", "M", nu(54.90, "A menos, todo mês", cor=VERDE, casas=2, emoji="✅"))],
 34: [("^", "M", ic([("📉", "limite de R$ 6.000 para R$ 4.000", False)], "2")), ("nem um real a mais", "M", perto_v(("P13", None), baloes=[B("Só o que eu já devo, e nem um real a mais.", 0, "Só", "mais", **VE_B)]))],
 35: [("^", "M", ic([("📺", "duas assinaturas canceladas", False)], "3")), ("sessenta e nove", "M", nu(69.80, "Voltaram para ela", "todo mês", cor=VERDE, casas=2, emoji="✅"))],
 36: [("^", "M", dupla(("P16", None), ("P16", None))), ("segundinho", "M", foco("varanda-domingo-perto.jpg", 50, 55, z=1.25)),
      ("buzinou", "M", dom_larga([TS_D(), VS_D(("P03", None))])), ("Obrigada, porteiro", "M", perto_v(("P05", None), baloes=[B("Obrigada, porteiro.", 0, "Obrigada", "porteiro", **VE_B)]))],
 37: [("^", "M", rua_noite()), ("Dona Cida", "M", CIDA_NOITE()), ("virou a minha semana", "C", tiao("P1", -1))],
 38: [("^", "C", tiao("P2", 1))],
 39: [("^", "C", tiao("P2", -1)), ("balanço do mês", "V", "banco:FM:4-balanco/balanco__estilo-donut-despesas__horizontal.mp4"),
      ("Juros e tarifas", "M", ic([("💸", "Juros do cheque especial: R$ 188,25", False), ("🧾", "Pacote de serviços: R$ 54,90", False)], "Juros e tarifas: R$ 243,15 por mês")),
      ("Se a Valéria tivesse", "C", tiao("P3", 1)),
      ("sete dias", "M", nu(7, "Dá para testar o FinMoovi", "link na descrição · www.finmoovi.com", cor=VERDE, fmt="int", suf=" dias", emoji="📱"))],
 # 6. O meu susto
 40: [("^", "M", CIDA_NOITE([B("E o seu? Você leu o seu linha por linha também, ou só ensina?", 0, "E o seu", "ensina", **VE_B)]))],
 41: [("^", "M", rua_noite([TI(("P01", None), x=1250)])), ("Então lê", "M", CIDA_NOITE([B("Então lê.", 0, "Então", "lê", **VE_B)])),
      ("martelando", "C", tiao("P1", 1))],
 42: [("^", "M", cel("O extrato do Tião", [("Salário", "+ ...", True), ("Pacote de serviços", "- 12,90", False)], [1])),
      ("seis anos", "M", li(["2020", "2021", "2022", "2023", "2024", "2025", "2026"], 6, "Pacote de serviços: R$ 12,90 todo mês"))],
 43: [("^", "C", tiao("P4", -1)), ("setenta e dois", "M", nu(928.80, "Seis anos de pacote", "R$ 12,90 × 72 meses", cor=VERM, casas=2, emoji="😳")),
      ("caneca velha", "M", rua_noite([TI(("P04", None), x=1250)]))],
 44: [("^", "C", tiao("P3", 1)), ("contrato específico", "M", fr("Pacote de serviços exige *contrato específico*", "Resolução CMN 3.919/2010, art. 8º")),
      ("cancelei", "C", tiao("P2", -1))],
 45: [("^", "M", rua_dia([GE("sandra", ("P07", None), x=700)], carro=False)),
      ("bem baixinho", "M", rua_dia([GE("sandra", ("P07", None), x=600), TI(("P10", None), x=1350)], [B("Tião, como é que eu vejo se eu pago esse tal pacote?", 0, "como é que", "pacote", x=150, larg=1000)], carro=False)),
      ("trinta e nove", "M", nu(39.90, "O pacote da Sandra", "todo mês", cor=VERM, casas=2, emoji="🤫"))],
 46: [("^", "C", tiao("P3", 1)), ("Dica número três", "M", ic([("🕳️", "o salário não pode chegar devendo: tapa o buraco do limite primeiro", False)], "Dica 3")),
      ("todo santo dia", "C", tiao("P4", -1))],
 47: [("^", "M", conta("O mês da Valéria", [("Dia 5: entra o salário", 8700), ("Tapa o buraco do limite", -3800), ("Dia 8: parcela do carro", -4555.56),
                                             ("Dia 10: aluguel", -3900)], total="No dia 10", passo=1.6))],
 48: [("^", "C", tiao("P4", 1)), ("chegava gasto", "M", fr("O salário *já chegava gasto*, pagando o mês que passou")), ("O problema nunca", "C", tiao("P2", -1))],
 49: [("^", "M", DOM(("P17", None))), ("chave do carrão", "M", foco(*CANECA_D)),
      ("Me ajuda a vender", "M", perto_v(("P15", None), baloes=[B("Me ajuda a vender, Tião.", 0, "Me ajuda", "Tião", **VE_B)])),
      ("Três meses depois", "M", fr("*Três meses* depois")), ("tinha sumido", "M", cel("Extrato · três meses depois", [("Salário", "+ 8.700,00", True), ("Aluguel", "- 2.300,00", False)], [0]))],
 50: [("^", "M", perto_t(("P08", None), x=960))],
 51: [("^", "C", tiao("P2", 1)), ("só o número", "M", fr("Comenta *só o número*: quanto você paga de pacote por mês"))],
 # 7. O proximo
 52: [("^", "C", tiao("P1", -1)), ("farmácia da avenida", "M", fr("No sábado seguinte, na *farmácia* da avenida")),
      ("CPF para o desconto", "C", tiao("P4", 1))],
 53: [("^", "M", perto_v(("P08", None))), ("letra miudinha", "M", cel("A nota da farmácia", [("...", "...", False), ("letra miudinha", "???", False)], [1])),
      ("me puxou", "M", perto_v(("P09", None), baloes=[B("Tião, você sabe o que eles fazem com o nosso CPF?", 0, "você sabe", "CPF", **VE_B)]))],
 54: [("^", "M", fr("Por que a farmácia sempre pede o seu *CPF*?", "Não é o desconto")), ("Clica agora", "C", tiao("P2", 1))],
}
