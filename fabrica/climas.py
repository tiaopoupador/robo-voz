# Clima de cada cena, escolhido pela FALA (Ed, 18/11/2026: «quando falar noite chuvosa, ai cai uma chuva, mas tudo com muita
# sutileza, quando fala de algo ruim (...) poeira como de fogo» · «quando se referir ao passado (...) preto e branco ou algo
# semelhante»). Aprovados: chuva, brasas, tensao, brilho, poeira lenta (A), pontos de luz (C) e o passado «lembranca» (7).
# Recusados: neve grossa (B) e cenas alternando com e sem nada (E).
# Ordem de prioridade: passado > chuva > tensao > brasas > brilho > fundo calmo (lenta ou luz).
# No cenas.py de um video, CLIMA = {linha: "chuva", ...} manda por cima da regra.
import re, unicodedata

def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")

REGRAS = [
    # «lembra do...?» e o Tiao a falar com quem assiste, NAO e passado; so conta o passado contado
    ("passado", r"\b(anos atras|antigamente|quando (eu|ela|ele) era (menin|crianc|nov|pequen)|na (minha|sua|tua) infancia|no meu tempo|naquele tempo|em crianca)"),
    ("chuva", r"\b(chuva|chuvos|chovia|chover|temporal|garoa|tempestade)"),
    ("tensao", r"\b(susto|assust|medo|desesper|panico|gelou|gelei|tremeu|tremi|o coracao|nao dormi|estourou|venceu hoje|cortaram a luz)"),
    ("brasas", r"\b(divida|juros|golpe|perdeu|perdi|perder|prejuizo|queim|sumiu|criou perna|caro demais|rombo|negativad|nome sujo|estourad|multa|calote|furo)"),
    ("brilho", r"\b(sobrou|sobrar|economiz|deu certo|conseguiu|bolso cheio|poupou|poupei|poupar|fossem guardados|guardar dinheiro|guardou dinheiro|guardando dinheiro|rendendo|juntou)"),
]
DIA_FORA = r"(rua|portao|quintal|feira|praca|calcada|manha|tarde|sol)"

def escolher(fala, imagem="", nome_cena="", linha_tem_flashback=False):
    """devolve o clima de uma cena: passado, chuva, tensao, brasas, brilho, lenta ou luz.
    linha_tem_flashback: a mesma fala ja tem uma cena de lembranca; entao so ESSA fica no passado (a do presente nao)"""
    f = _sem_acento(fala or ""); img = _sem_acento((imagem or "") + " " + (nome_cena or ""))
    if "flashback" in img: return "passado"
    if linha_tem_flashback: f = re.sub(REGRAS[0][1], " ", f)
    if "chuva" in img: return "chuva"
    if re.search(r"(assust|choque|susto|desesper)", img): return "tensao"
    for clima, rx in REGRAS:
        if re.search(rx, f): return clima
    # fundo calmo: pontos de luz de dia ao ar livre; poeira lenta dentro de casa ou a noite
    return "luz" if re.search(DIA_FORA, img) and "noite" not in img else "lenta"

if __name__ == "__main__":  # ensaio: python fabrica/climas.py 02
    import sys, collections
    P = r"C:\Users\Ed Flávio\Desktop\CLAUDE-CODE\CANAL TIAO POUPADOR"
    linhas = open(f"{P}/robo-voz/roteiro-{sys.argv[1]}.txt", encoding="utf-8").read().splitlines()
    cont = collections.Counter()
    for i, l in enumerate(linhas):
        c = escolher(l); cont[c] += 1
        if c not in ("lenta", "luz"):
            rx = dict(REGRAS)[c]; m = re.search(rx, _sem_acento(l)); print(f"{i:3d} {c:8s} [{m.group(0) if m else ''}] {l[:90]}")
    print(dict(cont))
