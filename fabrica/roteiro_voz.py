# Peca do robo: tira do roteiro (.md) o texto da voz.
# Uso: python fabrica/roteiro_voz.py 03   -> robo-voz/roteiro-03.txt (uma fala por linha) e roteiro-03-secoes.json
# Regras: comeca no "## 0."; para no "## Ficha de fontes"; [marcas], titulos "## " e linhas "---" nao entram na voz;
# cada paragrafo = uma fala. secoes[i] = True quando a fala i e a ULTIMA da sua parte (o narracao.py poe a pausa
# longa depois dela e o descricao.py comeca o capitulo seguinte na fala i+1).
import json, os, re, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
NN = sys.argv[1]
md = open(next(f"{P}/roteiros/{f}" for f in sorted(os.listdir(P + "/roteiros")) if f.startswith(f"{NN}-") and f.endswith(".md") and "pedidos" not in f and "fontes" not in f), encoding="utf-8").read()
md = md.split("## Ficha de fontes")[0]
md = md[md.index("## 0."):]
falas, fim = [], []
for bloco in re.split(r"\n\s*\n", md):
    b = bloco.strip()
    if not b: continue
    if b.startswith("## "):
        if falas: fim.append(len(falas) - 1)
        continue
    b = re.sub(r"\[[^\]]*\]", "", b).strip()
    if not b or set(b) <= set("-"): continue
    falas.append(" ".join(b.split()))
fim.append(len(falas) - 1)
secoes = [i in fim for i in range(len(falas))]
open(f"{P}/robo-voz/roteiro-{NN}.txt", "w", encoding="utf-8").write("\n".join(falas) + "\n")
json.dump(secoes, open(f"{P}/robo-voz/roteiro-{NN}-secoes.json", "w"))
print(f"{len(falas)} falas, {len(fim)} partes -> robo-voz/roteiro-{NN}.txt")

# Guarda de graca (Ed, 19/11/2026: «tem que deixar humanizado como se fosse um humano real»): avisa antes de gravar a voz
SIGLA_OK = {"CPF", "SMS", "PIX", "WHATSAPP"}
avisos = []
for i, f in enumerate(falas):
    if re.search(r"\bhein\b", f, re.I): avisos.append(f"fala {i}: tem 'hein' (a voz le 'rein'): tirar")
    for s in set(re.findall(r"\b[A-Z]{2,6}\b", f)) - SIGLA_OK: avisos.append(f"fala {i}: sigla {s}: dizer o nome inteiro")
    if re.search(r"\b(está escrito|no site)\b[.!]", f, re.I): avisos.append(f"fala {i}: 'está escrito'/'no site' sem dizer onde")
for a in avisos: print("AVISO", a)
if not avisos: print("fala de gente: nenhum aviso")

# Guarda da sequencia (Ed, 19/11/2026: «o video x no final tem que fazer o gancho com o titulo do proximo video»):
# o gancho final (as 2 ultimas falas) tem de trazer as palavras fortes do TITULO do proximo video na agenda.json.
import unicodedata
def _sem_acento(s): return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
FRACAS = set("a o as os um uma de da do das dos no na nos nas em e que se seu sua por para pra ao com nao sem te ja ou ela ele voce mais tem foi isso esse essa quem por que porque como".split())
NUM = {"10": "dez", "50": "cinquenta", "1990": "noventa", "7": "sete"}
cal = json.load(open(f"{P}/fabrica/agenda.json", encoding="utf-8"))["calendario"]
prox = next((v for v in cal if v["nn"] > NN), None)
if prox:
    fimtxt = _sem_acento(" ".join(falas[-2:]))
    fortes = [w for w in re.findall(r"[\w$]+", _sem_acento(prox["titulo"])) if w not in FRACAS and len(w) > 2 or w in NUM]
    faltam = [w for w in fortes if (NUM.get(w, w)[:5] not in fimtxt)]
    tem = len(fortes) - len(faltam)
    print(f"gancho do proximo ({prox['nn']}: {prox['titulo']}): {tem} de {len(fortes)} palavras do titulo no fim")
    if tem < max(2, len(fortes) // 2): print(f"AVISO o fim nao chama o titulo do {prox['nn']}: faltam {', '.join(faltam)}")
