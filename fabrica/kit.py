# Atalhos para escrever as cenas (os mesmos do video 01). Importado por fabrica/videos/vNN/cenas.py.
VERDE, VERM, AMAR, AZUL = "#2E9E5B", "#D9443A", "#F2B632", "#3B6EA8"
# motion (tela inteira)
def fr(t, sobre=None, escuro=False): return {"k": "frase", "texto": t, "sobre": sobre, "escuro": escuro}
def nu(v, r=None, e=None, de=0, cor="#1F1B16", fmt="reais", casas=0, suf="", emoji=None): return {"k": "num", "valor": v, "rotulo": r, "embaixo": e, "de": de, "cor": cor, "fmt": fmt, "casas": casas, "suf": suf, "emoji": emoji}
def ci(nome, ano, onde, achado, fonte=None): return {"k": "cita", "nome": nome, "ano": ano, "onde": onde, "achado": achado, "fonte": fonte}
def ba(itens, titulo=None, fmt="reais"): return {"k": "barras", "itens": [{"rotulo": a, "valor": b, "cor": c} for a, b, c in itens], "titulo": titulo, "fmt": fmt}
def li(marcos, ativo, titulo=None): return {"k": "linha", "marcos": marcos, "ativo": ativo, "titulo": titulo}
def ic(itens, titulo=None): return {"k": "icones", "titulo": titulo, "itens": [{"e": e, "r": r, "risca": x} for e, r, x in itens]}
# por cima de imagem
def pl(texto, x=50, y=50, cor="#1F1B16", fundo="#FFFDF8", tam=92, ini=0.5): return {"t": "placa", "texto": texto, "x": x, "y": y, "cor": cor, "fundo": fundo, "tam": tam, "ini": ini}
def et(texto, x=68, y=28, cor=AMAR): return {"t": "etiqueta", "texto": texto, "x": x, "y": y, "cor": cor}
def cb(texto, x=50, y=45, cor=VERDE, ini=0.6): return {"t": "carimbo", "texto": texto, "x": x, "y": y, "cor": cor, "ini": ini}
def bl(texto, x=66, y=24, lado="esq"): return {"t": "balao", "texto": texto, "x": x, "y": y, "lado": lado}
def ft(texto, pos="topo"): return {"t": "frasetopo", "texto": texto, "pos": pos}
def ls(itens, x=72, y=50, riscar=False): return {"t": "lista", "itens": itens, "x": x, "y": y, "riscar": riscar}
def tr(x=50, y=45): return {"t": "trinca", "x": x, "y": y}
# reacoes de filme
def re_(e, x, y, g=None): return {"t": "reacao", "e": e, "x": x, "y": y, "ini": 0.6, **({"g": g} if g else {})}
def br(x, y, g=None): return {"t": "brilho", "x": x, "y": y, "ini": 0.6, **({"g": g} if g else {})}
def xi(x, y, g=None): return {"t": "xis", "x": x, "y": y, "ini": 0.6, **({"g": g} if g else {})}
def ck(x, y, g=None): return {"t": "check", "x": x, "y": y, "ini": 0.6, **({"g": g} if g else {})}
