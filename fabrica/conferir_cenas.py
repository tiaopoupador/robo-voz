# Revisor de SINCRONIA das cenas (gratis, sem IA). Roda sozinho no comeco do montar.py e para tudo se achar problema.
# Uso solto: python fabrica/conferir_cenas.py NN
#
# Nasceu a 27/11/2026, do 06 recusado pelo Ed:
#  «aqui no comeco ja mostra um card inacabado e nada a ver para o momento» (um balao com a fala do Marcos sobre a voz do Tiao)
#  «cards q aparecem do nada», «imagens que nao se conectam com o que esta sendo dito».
# O que ele confere em cada fala do cenas.py:
#  1. todo gatilho de cena esta mesmo na fala (senao a cena entra fora de hora ou no comeco);
#  2. o balao de um personagem so aparece se a fala DELE e dita nesta fala do roteiro, com a 1.a e a ultima palavra dentro dela;
#  3. o texto do balao e o que se ouve (as palavras do balao estao na fala, tirando a troca de grafia da voz, ex.: CPF);
#  4. nenhuma cena com menos de 1,2 s entre dois gatilhos seguidos da mesma fala (card que pisca e some), medido em palavras;
#  5. toda fala tem cena.
import sys, re, unicodedata, importlib, os
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, P)
TROCA = {"cpf": "ce pe efe"}

def n(x):
    x = unicodedata.normalize("NFKD", str(x).lower())
    x = "".join(c for c in x if not unicodedata.combining(c))
    for a, b in TROCA.items(): x = re.sub(rf"\b{a}\b", b, x)
    return re.sub(r"[^a-z0-9 ]", " ", x).split()

def pos(lista, alvo, de=0):
    """onde a sequencia de palavras alvo comeca dentro de lista (a partir de de), ou None"""
    for i in range(de, len(lista) - len(alvo) + 1):
        if lista[i:i + len(alvo)] == alvo: return i
    return None

def conferir(NN):
    C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
    F = open(f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
    erros = []
    for k in range(len(F)):
        if k not in C.L: erros.append(f"fala {k}: sem cena nenhuma")
    for k, v in C.L.items():
        if k >= len(F): erros.append(f"fala {k}: o roteiro so tem {len(F)} falas"); continue
        t = n(F[k]); ult = 0; ant = None
        for g, tp, c in v:
            if g != "^":
                i = pos(t, n(g))
                if i is None: erros.append(f"fala {k}: gatilho «{g}» nao esta na fala"); continue
                if ant is not None and 0 <= i - ant < 3: erros.append(f"fala {k}: «{g}» entra {i - ant} palavras depois da cena anterior (pisca e some)")
                ant = i
            else: ant = 0
            if not isinstance(c, dict): continue
            for b in c.get("baloes", []):
                g1, g2 = b.get("g"), b.get("ate")
                if not g1: erros.append(f"fala {k}: balao «{b['texto'][:40]}» sem a palavra de comeco"); continue
                i1 = pos(t, n(g1))
                if i1 is None: erros.append(f"fala {k}: balao «{b['texto'][:40]}» comeca em «{g1}», que nao e dito nesta fala"); continue
                if g2 and pos(t, n(g2), i1) is None: erros.append(f"fala {k}: balao «{b['texto'][:40]}» acaba em «{g2}», que nao e dito depois de «{g1}»")
                falta = [w for w in n(b["texto"]) if w not in t]
                if len(falta) > 1: erros.append(f"fala {k}: o balao diz palavras que ninguem fala: {' '.join(falta[:6])}")
    return erros

if __name__ == "__main__":
    e = conferir(sys.argv[1])
    for x in e: print("ERRO", x)
    print("sincronia das cenas:", "ok" if not e else f"{len(e)} problema(s)")
    sys.exit(1 if e else 0)
