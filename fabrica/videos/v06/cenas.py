# Cenas do video 06 MODELADO (Tiao Conversa: 10 Regras do Tiao Para Viver Tranquilo Ganhando Pouco). Roteiro: roteiros/06-dez-regras.md.
# 27/11/2026 (Ed: «quero exatamente o mesmo video que deu muitas views com o nosso jeito de falar»): modelo Edu Investe, 24,8x.
# Sai sem imagem nova: o Tiao fala com quem assiste nas poses P1 a P4 (fundo do 03 e do 04); as lembrancas sao a turma viva
# nos cenarios do 05 (rua de dia e de noite, varanda de domingo). Os numeros vao nos cartoes do kit. So as capas vao ao Ed (Team).
from fabrica.kit import *
from fabrica.videos.v05.cenas import (P, B, T, VE, TI, GE, DE, TS_D, VS_D, dom_larga, dom_perto, rua_dia, rua_noite, foco, cel, conta,
                                      CANECA_D)
from fabrica.videos.v03.cenas import IMG as _I3

RUA = "fundo-banquinho"
IMG = {k: _I3[k] for k in ("fundo-banquinho", "selo-tiao-cafe")}
_V = "valeria-ficha-a.jpg.jpg + tiao-ficha-oficial.jpg"
_T = "tiao-ficha-oficial.jpg"
TITULO = "10 Regras do Tião Para Viver Tranquilo Ganhando Pouco (Salário de R$ 2.000)"
MODELO = {"id": "HIrzIYQCzMU", "canal": "@eduinvesteoficial", "vezes": 24.8}
CAPA_TEXTO = "GANHA POUCO VIVE TRANQUILO"
# 26/11: o texto vai DENTRO do prompt da capa (pedidos.py). Modelagem (27/11): a capa A tem a MESMA composicao do modelo
# (o mesmo homem cansado a esquerda, seta, tranquilo a direita; 2 linhas grandes no alto a esquerda, a 2.a palavra em verde).
CAPA_LETRAS = {"A": ("GANHA POUCO VIVE TRANQUILO", "TRANQUILO", "verde"), "B": ("R$ 2.000 E DORME BEM", "DORME BEM", "verde"),
               "C": ("GANHA O TRIPLO E PEDE EMPRESTADO", "PEDE EMPRESTADO", "vermelho"), "D": ("10 REGRAS ZERO APERTO", "ZERO APERTO", "amarelo")}
VINHETA = 3  # a vinheta entra depois da fala 3 («Vamos começar?»)
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
DESC = ("O Tião ganha R$ 2.000 por mês como porteiro e dorme tranquilo. O Marcos, o vizinho da picape zero, ganha o triplo, e no dia 20 pede "
        "dinheiro emprestado na fila do açougue.\n\n"
        "Neste vídeo o Tião mostra as 10 regras dele, uma por uma, com a conta feita em cima dos dois mil: para onde vai cada real, pagar a si mesmo "
        "primeiro, a casa que manda nas outras contas, o mercado com lista, não parcelar, cortar o que paga e não usa (e a linha do extrato que deixou a "
        "Valéria branca), o carro, o prazer sem culpa, o décimo terceiro e a comparação. Com a lei na mão: o cheque especial (Resolução CMN 4.765), "
        "os serviços bancários grátis (Resolução CMN 3.919), o vale-transporte (Lei 7.418) e o 13º (Lei 4.749).")
TAGS = ["viver tranquilo ganhando pouco", "como viver com salário de 2000 reais", "regras de dinheiro", "como organizar o salário", "pague-se primeiro",
        "orçamento pessoal", "cheque especial", "cesta de serviços", "vale-transporte", "décimo terceiro", "como guardar dinheiro ganhando pouco",
        "educação financeira", "Tião Poupador", "Tião Conversa"]
PERGUNTA = "Qual das 10 regras você começa hoje? Só o número."
CAP_NOMES = {"Abertura (é um Reels: entende-se sozinha)": "Ele ganha o triplo", "Para onde vai cada real": "Regras 1 e 2",
             "A casa e a panela": "Regras 3 e 4", "O dia vinte": "Regra 5 e o dia 20", "A linha do extrato": "Regra 6: a linha do extrato",
             "A picape e o prazer": "Regras 7 e 8", "O que a rua não viu": "Regras 9 e 10", "O próximo": "A mensagem da farmácia"}
FORTES = {"regra", "salário", "marcos", "valéria", "sandra", "extrato", "reserva", "parcela", "limite", "picape", "aluguel", "mercado", "prazer"}
GIF = "foto"
REELS_TOPO = "Ele ganha o *TRIPLO*|e no dia 20 pede|dinheiro *EMPRESTADO*|na fila do açougue!"  # a frase isca do Short do gancho (fabrica/reels.py)
REELS_EMOJI = "1f631"
PLAYLIST = "tiao-conversa"
# novela.md: o clima troca a cada 2 ou 3 min, sem repetir faixa seguida
CLIMA = {0: "alerta", 4: "calma", 9: "humor", 12: "curiosa", 17: "reflexiva", 21: "humor", 26: "tensao", 32: "drama", 35: "tensao", 40: "virada",
         42: "drama", 45: "curiosa", 49: "calma", 53: "humor", 55: "reflexiva", 59: "drama", 62: "virada", 63: "drama", 66: "final"}
AMB = [("passaros", 4, "^", 20, 0.2), ("passaros", 17, "^", 20, 0.2), ("passaros", 35, "^", 20, 0.2), ("grilos", 42, "^", 14, 0.2)]

# ---------- as pecas que se repetem ----------
def tiao(pose, lado=1): return (RUA, pose, lado)
VE_B = dict(x=110, y=40, larg=1080, rabo=(640, 470))  # balao de quem esta a esquerda
def so(pid, pose, texto=None, g1=None, g2=None, noite=False):
    """um da turma de perto, na rua, com balao opcional"""
    f = rua_noite if noite else rua_dia
    return f([GE(pid, (pose, None), x=700)], [B(texto, 0, g1, g2, **VE_B)] if texto else [], **({} if noite else {"carro": False}))
def perto_v(*poses, baloes=(), x=600): return dom_perto([VE(*poses, x=x)], baloes)
def extrato(destaque=()):
    return cel("Extrato · conta do salário", [("Salário", "+ 8.700,00", True), ("Pacote de serviços", "- 54,90", False),
                                              ("Juros cheque especial", "- 188,25", False)], destaque)
CONTA_TIAO = conta("O mês do Tião", [("Salário", 2000), ("Aluguel", -650), ("Luz, água, gás e internet", -285), ("Mercado", -600),
                                     ("Transporte (vale)", -120), ("Celular", -40), ("Farmácia", -45)], total="Sobram")
def regra(n, texto, emoji): return ic([(emoji, texto, False)], f"Regra {n}")

L = {
 # 0. Abertura (Reels)
 0: [("^", "M", so("marcos", "P01", "Tião, paga aí, que dia cinco eu te devolvo!", "Eu ganho", "é ele")),
     ("triplo", "M", nu(6000, "O salário do Marcos", "o triplo do meu", emoji="💼")), ("açougue", "C", tiao("P4", 1))],
 1: [("^", "M", cel("Banco · agora", [("Salário recebido", "+ 2.000,00", True)], [0])), ("começo de um plano", "C", tiao("P2", -1)),
     ("picape zero", "M", so("marcos", "P04")), ("vermelho", "M", fr("Dia 20: o Marcos já está no *vermelho*."))],
 2: [("^", "C", tiao("P1", 1)), ("pão-duro", "M", so("sandra", "P01", "Esse Tião é um pão-duro!", "pão-duro", "pão-duro")),
     ("dez regras", "M", fr("*10 regras*. Nenhuma pede para ganhar mais.")),
     ("branca", "M", perto_v(("P03", None), baloes=[B("Tião... isso aqui sai todo mês?", 0, "Tião", "mês", **VE_B)]))],
 3: [("^", "C", tiao("P2", 1)), ("puxa a cadeira", "M", dom_larga())],
 # 1. Para onde vai cada real
 4: [("^", "M", dom_perto([TI(("P08", None), x=960)]))],
 5: [("^", "C", tiao("P1", 1)), ("porteiro", "C", tiao("P2", -1)), ("moro sozinho", "C", tiao("P3", 1)),
     ("filho", "M", fr("Com filho, os *números* mudam.", "A ordem das regras, não."))],
 6: [("^", "M", dom_larga([TS_D(), VS_D(("P18", None))])), ("linha no extrato", "M", extrato([2])), ("susto", "C", tiao("P4", -1))],
 7: [("^", "M", regra(1, "saiba para onde vai cada real", "🧭")), ("Aluguel da casinha", "M", CONTA_TIAO)],
 8: [("^", "M", nu(260, "A minha folga do mês", "R$ 2.000 menos R$ 1.740", cor=VERDE, emoji="🟢")), ("Na portaria", "C", tiao("P3", 1)),
     ("Quanto precisam", "M", fr("Sabem quanto *ganham*.", "Quanto precisam, não."))],
 9: [("^", "M", so("marcos", "P06", "Depende, Tião.", "Depende", "Tião")), ("depende", "C", tiao("P3", -1))],
 10: [("^", "M", ic([("🏠", "essencial", False), ("👟", "desejo", False), ("🧊", "imprevisto", False)], "Cada gasto num grupo")),
      ("onde aquilo entra", "C", tiao("P2", 1))],
 11: [("^", "C", tiao("P1", -1)), ("somem rapidinho", "M", nu(260, "Somem rápido", "se não tiverem destino", cor=VERM, emoji="💨"))],
 12: [("^", "M", regra(2, "pague a você mesmo primeiro", "🐷")), ("cento e cinquenta", "M", cel("Dia 5 · transferência", [("Para: conta da reserva", "- 150,00", False)], [0]))],
 13: [("^", "M", so("marcos", "P05", "Eu guardo o que sobra, Tião.", "Eu guardo", "Tião")), ("Nada", "M", fr("O que sobra no fim do mês dele: *nada*.")),
      ("depois de me pagar", "C", tiao("P2", 1))],
 14: [("^", "C", tiao("P3", -1)), ("agendei", "M", cel("Agendado", [("Todo dia 5", "R$ 150,00", True), ("Repetir", "sempre", True)], [0]))],
 15: [("^", "M", nu(1800, "Em um ano", "R$ 150 por mês", cor=VERDE, emoji="📅")), ("sétimo mês", "M", li(["mês 1", "mês 3", "mês 5", "mês 7"], 3, "Passei dos R$ 1.000")),
      ("outra vida", "C", tiao("P1", 1))],
 16: [("^", "M", ic([("🎉", "R$ 70 para o prazer", False), ("🧰", "R$ 40 para o que der e vier", False)], "Dinheiro com nome")),
      ("like", "C", tiao("P2", -1)), ("mais pesada", "C", tiao("P4", 1))],
 # 2. A casa e a panela
 17: [("^", "M", regra(3, "a casa manda em todas as outras contas", "🏠")), ("seiscentos e cinquenta", "M", nu(650, "O meu aluguel", "abaixo de um terço do salário", emoji="🏠")),
      ("bairros bonitos", "C", tiao("P2", 1)), ("ninguém paga", "C", tiao("P3", -1))],
 18: [("^", "M", so("sandra", "P03", "Olha a varanda, gente! Tem piscina!", "Olha", "piscina")),
      ("outra conta", "M", nu(2150, "A mais que o meu aluguel", "todo mês", cor=VERM, emoji="🏊")),
      ("vinte e cinco mil", "M", nu(25800, "Em um ano", cor=VERM, emoji="📅")), ("caneta", "M", so("marcos", "P06"))],
 19: [("^", "C", tiao("P2", -1)), ("teto", "M", fr("Um *terço* da renda é o teto da casa."))],
 20: [("^", "C", tiao("P1", 1)), ("ganha no sono", "C", tiao("P3", -1))],
 21: [("^", "M", regra(4, "comida feita em casa e mercado com lista", "🛒")), ("seiscentos", "M", nu(600, "Mercado por mês", "uns R$ 20 por dia", emoji="🛒")),
      ("lista no celular", "M", cel("Lista do sábado", [("Arroz", "✓", True), ("Feijão", "✓", True), ("Ovos", "✓", True), ("Frango", "✓", True)], [])),
      ("barriga cheia", "C", tiao("P2", 1))],
 22: [("^", "C", tiao("P4", -1)), ("biscoito", "M", ic([("🍪", "biscoito", True), ("🥤", "refrigerante", True), ("🍕", "comida pronta", True)], "Nada disso estava na lista")),
      ("trava", "C", tiao("P3", 1))],
 23: [("^", "C", tiao("P2", -1)), ("marmita", "M", fr("Uma panela grande = a *marmita* da semana."))],
 24: [("^", "M", so("marcos", "P03", noite=True)), ("dia inteiro", "M", fr("Um pedido do Marcos = o meu *dia inteiro* de comida.")),
      ("Exceção", "C", tiao("P1", 1))],
 25: [("^", "C", tiao("P4", -1))],
 # 3. O dia vinte
 26: [("^", "M", regra(5, "não parcele o que não pode pagar à vista", "💳")), ("doze de cento e vinte", "M", fr("*12 × R$ 120*", "cabe no bolso?")),
      ("preço de não esperar", "M", nu(1440, "O mesmo celular, parcelado", "R$ 240 a mais", cor=VERM, emoji="📱"))],
 27: [("^", "C", tiao("P2", 1)), ("cento e oitenta", "M", nu(180, "Só a tela nova", "à vista", cor=VERDE, emoji="✅"))],
 28: [("^", "M", ic([("⏳", "não cabe à vista? espera 30 dias", False), ("🐷", "ainda quer? junta antes", False), ("💳", "fatura do cartão: paga inteira", False)], "A regra 5 em três partes"))],
 29: [("^", "C", tiao("P4", 1)), ("cheque especial", "M", fr("Cheque especial = o *limite* que o banco cola na sua conta", "Resolução CMN 4.765/2019")),
      ("oito por cento", "M", nu(8, "O teto do cheque especial", "Resolução CMN 4.765/2019, art. 3º", cor=VERM, fmt="int", suf="% ao mês", emoji="🔥")),
      ("sete e meio", "M", nu(7.53, "A média em setembro de 2026", "Banco Central (SGS 25463)", cor=VERM, casas=2, fmt="num", suf="% ao mês", emoji="📈"))],
 30: [("^", "M", ic([("📱", "o celular", False), ("🛋️", "o sofá", False), ("🔥", "a churrasqueira", False), ("🎁", "até o presente da Sandra", False)], "O Marcos parcela tudo")),
      ("se empilham", "M", so("marcos", "P07")), ("amanhã", "C", tiao("P3", 1))],
 31: [("^", "C", tiao("P1", -1)), ("primeiro degrau", "M", fr("Não é bronca. É o *primeiro degrau*."))],
 32: [("^", "C", tiao("P4", 1)), ("triplo", "M", nu(6000, "O salário do Marcos", "o triplo do meu", emoji="💼")),
      ("açougue", "M", so("marcos", "P01", "Tião, paga aí, que dia cinco eu te devolvo!", "açougue", "é ele"))],
 33: [("^", "M", rua_dia([DE("marcos", 700), DE("tiao", 1100), DE("sandra", 1450)], carro=False)),
      ("não passou", "M", cel("Maquininha", [("Cartão", "RECUSADO", False)], [0])),
      ("rindo alto", "M", so("marcos", "P01", "Tião, paga aí a carne do churrasco, que dia cinco eu te devolvo!", "Tião", "devolvo")),
      ("Cem reais", "M", nu(100, "A carne do churrasco", "paga pelo porteiro", emoji="🥩")), ("triplo inteirinho", "C", tiao("P4", -1))],
 34: [("^", "C", tiao("P2", 1)), ("risada", "C", tiao("P3", -1)), ("quase invisível", "C", tiao("P4", 1))],
 # 4. A linha do extrato
 35: [("^", "M", regra(6, "corte o que você paga e não usa", "✂️")), ("Volta comigo", "M", dom_larga([TS_D(), VS_D(("P18", None))])),
      ("passando o dedo", "M", perto_v(("P08", None))), ("parou numa linha", "M", extrato([2])),
      ("Ficou branca", "M", perto_v(("P03", None), baloes=[B("Tião... isso aqui sai todo mês?", 0, "Tião", "mês", **VE_B)]))],
 36: [("^", "M", extrato([2])), ("mês anterior", "M", li(["março", "abril", "maio", "...", "outubro"], 4, "Juros cheque especial: R$ 188,25 todo mês")),
      ("desde março", "C", tiao("P4", 1))],
 37: [("^", "M", perto_v(("P11", None), baloes=[B("Mas eu nunca usei cheque especial, Tião!", 0, "Mas", "Tião", **VE_B)])),
      ("antigamente", "C", tiao("P2", -1)), ("todo dia dez", "M", fr("A conta descia do *zero* todo dia 10."))],
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
      ("cesta de serviços", "M", cel("O extrato do Tião", [("Salário", "+ 2.000,00", True), ("Cesta de serviços", "- 12,90", False)], [1])),
      ("seis anos", "M", li(["2020", "2021", "2022", "2023", "2024", "2025", "2026"], 6, "Cesta de serviços: R$ 12,90 todo mês")),
      ("Novecentos e vinte e oito", "M", nu(928.80, "Seis anos de cesta", "R$ 12,90 × 72 meses", cor=VERM, casas=2, emoji="😳"))],
 43: [("^", "C", tiao("P3", 1)), ("três meses", "M", fr("A cada *3 meses*: um dia só para ler o extrato.")), ("dorme", "C", tiao("P1", -1))],
 44: [("^", "C", tiao("P2", 1)), ("só o número", "M", fr("Comenta *só o número*: quanto era a linha estranha do seu extrato")),
      ("sonho de metade da rua", "C", tiao("P4", -1))],
 # 5. A picape e o prazer
 45: [("^", "M", regra(7, "pense duas vezes antes de ter carro", "🚌")), ("vale-transporte", "M", fr("O patrão paga o que passar de *6% do salário*", "Lei 7.418/1985, art. 4º")),
      ("cento e vinte", "M", nu(120, "O que eu pago de transporte", "6% de R$ 2.000", cor=VERDE, emoji="🚌"))],
 46: [("^", "M", so("marcos", "P08")), ("Parcela", "M", conta("A picape do Marcos, por mês", [("Parcela", -2890), ("Seguro", -380), ("Combustível", -600),
                                                                                              ("Imposto e manutenção", -250)], total="Por mês")),
      ("Mais que o dobro", "C", tiao("P4", 1))],
 47: [("^", "C", tiao("P2", -1)), ("trabalhando para o carro", "C", tiao("P3", 1))],
 48: [("^", "C", tiao("P1", -1)), ("usado, à vista", "M", fr("Um dia: *usado*, à vista e com calma."))],
 49: [("^", "M", regra(8, "separe dinheiro para o prazer e gaste sem culpa", "🍦")), ("setenta reais", "M", nu(70, "Por mês, só para o prazer", cor=VERDE, emoji="🍦"))],
 50: [("^", "M", ic([("🍦", "sorvete na praça", False), ("⚽", "futebol de sábado", False), ("🎬", "cinema no dia da promoção", False)], "Prazer planejado")),
      ("de graça", "M", ic([("🌳", "o parque", False), ("🎪", "a festa de rua", False), ("🎟️", "o evento da prefeitura", False)], "De graça")),
      ("acabou", "C", tiao("P3", 1))],
 51: [("^", "C", tiao("P1", -1)), ("essa regra é sua", "C", tiao("P2", 1)), ("meio termo", "M", fr("O *meio termo* é onde a vida acontece."))],
 52: [("^", "M", so("sandra", "P03")), ("seiscentos", "M", nu(600, "Por mês, para tirar foto", cor=VERM, emoji="📸")), ("estar ali", "C", tiao("P2", -1))],
 53: [("^", "C", tiao("P4", 1)), ("recado rápido", "C", tiao("P2", -1))],
 54: [("^", "C", tiao("P2", 1)), ("balanço", "V", "banco:FM:4-balanco/balanco__estilo-donut-despesas__horizontal.mp4"),
      ("Os juros e as tarifas", "M", ic([("💸", "Juros do cheque especial", False), ("🧾", "Cesta de serviços", False)], "Uma fatia só para eles")),
      ("sete dias", "M", nu(7, "Dá para testar o FinMoovi", "link na descrição · www.finmoovi.com", cor=VERDE, fmt="int", suf=" dias", emoji="📱"))],
 # 6. O que a rua nao viu
 55: [("^", "M", regra(9, "o dinheiro sobe, o padrão fica", "📈")), ("décimo terceiro", "M", fr("1ª metade do *13º*: até 30 de novembro", "Lei 4.749/1965, art. 2º")),
      ("vinte de dezembro", "M", fr("O resto: até *20 de dezembro*", "Lei 4.749/1965, art. 1º")), ("Para mim", "M", nu(1000, "O meu agora", emoji="💰"))],
 56: [("^", "M", ic([("📱", "celular novo", True), ("👕", "roupa nova", True), ("🍽️", "jantar fora", True)], "Em janeiro, nada")), ("sem deixar rastro", "C", tiao("P4", -1))],
 57: [("^", "M", conta("O 13º do Tião", [("Primeira metade", 1000), ("Para a reserva", -500), ("Para viver melhor", -500)], total="Decidido antes", neutro=True)),
      ("cabeça fria", "C", tiao("P3", 1))],
 58: [("^", "M", so("marcos", "P04")), ("cinco mil para seis mil", "M", ba([("Antes", 5000, VERDE), ("Depois do aumento", 6000, VERDE)], "O salário do Marcos")),
      ("vantagem escondida", "C", tiao("P2", -1)), ("mais difícil", "C", tiao("P4", 1))],
 59: [("^", "M", regra(10, "compare-se só com você mesmo, de um ano atrás", "🪞")), ("Sandra posta", "M", so("sandra", "P03")),
      ("peito aperta", "C", tiao("P1", -1)), ("ninguém posta o depois", "M", ic([("🧾", "a fatura", False), ("💢", "a briga", False), ("🌙", "a noite sem dormir", False)], "O que ninguém posta"))],
 60: [("^", "C", tiao("P3", 1))],
 61: [("^", "M", ic([("❓", "não sabia para onde ia o dinheiro", True), ("0️⃣", "zero guardado", True), ("😟", "medo", True)], "Um ano atrás")),
      ("Hoje eu sei", "M", ic([("🧭", "sei para onde vai cada real", False), ("🐷", "tenho reserva", False), ("😴", "durmo", False)], "Hoje")),
      ("única comparação", "C", tiao("P2", -1))],
 62: [("^", "M", nu(650, "A geladeira pifou", "paga à vista, com a reserva", cor=VERDE, emoji="🧊")), ("guardei", "C", tiao("P1", 1)),
      ("Caneca velha", "M", foco(*CANECA_D))],
 63: [("^", "M", rua_dia([DE("marcos", 900)], carro=False)), ("carta do banco", "M", fr("*Parcela da picape*: em atraso")),
      ("de cabeça baixa", "M", so("marcos", "P07", "Tião, me ensina aquela tua conta?", "Tião", "conta"))],
 64: [("^", "M", cel("A conta do Marcos", [("Quanto eu preciso para viver", "?", False)], [0])), ("contrato", "M", so("marcos", "P02", "A Sandra vai me matar.", "A Sandra", "matar")),
      ("Vamos ver", "C", tiao("P3", 1))],
 65: [("^", "M", rua_dia([P("valeria", 1100, 960, 600, ("R4", None)), DE("marcos", 500)], carro=False)),
      ("Boa tarde", "M", so("valeria", "P15", "Boa tarde, Tião.", "Boa", "Tião")), ("primeiro passo", "C", tiao("P1", -1))],
 66: [("^", "C", tiao("P2", 1)), ("distância", "M", fr("Tranquilidade = o que você *ganha* menos o que você *precisa*")),
      ("dorme em paz", "C", tiao("P3", -1))],
 # 7. O proximo
 67: [("^", "M", so("cida", "P01")), ("cê pê éfe", "M", fr("“Me passa o seu *CPF*, que tem desconto.”")),
      ("desconfiou", "M", so("cida", "P04"))],
 68: [("^", "M", cel("Mensagem nova", [("Olá, Dona Cida!", "", True), ("Sobre o seu remédio de pressão...", "", False)], [1])),
      ("sacolinha", "M", so("cida", "P03", "Tião... como é que eles sabem disso?", "Tião", "disso"))],
 69: [("^", "M", fr("Como as farmácias ganham *dinheiro*?", "Não é o remédio")), ("Clica agora", "C", tiao("P2", 1))],
}
