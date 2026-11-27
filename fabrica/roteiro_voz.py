# Peca do robo: tira do roteiro (.md) o texto da voz.
# Uso: python fabrica/roteiro_voz.py 03   -> robo-voz/roteiro-03.txt (uma fala por linha) e roteiro-03-secoes.json
# Regras: comeca no "## 0."; para no "## Ficha de fontes"; [marcas], titulos "## " e linhas "---" nao entram na voz;
# cada paragrafo = uma fala. secoes[i] = True quando a fala i e a ULTIMA da sua parte (o narracao.py poe a pausa
# longa depois dela e o descricao.py comeca o capitulo seguinte na fala i+1).
import json, os, re, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
NN = sys.argv[1]
# 27/11/2026 (Ed recusou o 06: «o roteiro foi mal feito (...) feito as pressas sem pensar», «antes de escrever o proximo roteiro
# tem que ler o que foi o video anterior», «olhar como os concorrentes criam historias (...) quais sao as regras (...) e partir
# dai», «do que adianta ter regras se voce nao segue?»): sem a ficha de preparo, a voz NAO sai. Regra em canal-dark novela.md, secao 0.
_prep = f"{P}/roteiros/{NN}-preparo.md"
_partes = ["## Continuidade", "## Concorrentes", "## Regras relidas", "## Não repetir", "## O fim"]
if int(NN) >= 6:
    if not os.path.exists(_prep): raise SystemExit(f"ERRO: falta roteiros/{NN}-preparo.md (ler o anterior linha por linha, 3 concorrentes, as regras, o que nao repetir, o fim). canal-dark novela.md secao 0")
    _t = open(_prep, encoding="utf-8").read()
    _f = [x for x in _partes if x not in _t or len(_t.split(x, 1)[1].split(chr(10) + "## ")[0].strip()) < 200]
    if _f: raise SystemExit(f"ERRO: a ficha de preparo do {NN} esta incompleta (cada parte com pelo menos 200 letras): {', '.join(_f)}")
md = open(next(f"{P}/roteiros/{f}" for f in sorted(os.listdir(P + "/roteiros")) if f.startswith(f"{NN}-") and f.endswith(".md") and "pedidos" not in f and "fontes" not in f and "preparo" not in f), encoding="utf-8").read()
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
SIGLA_OK = {"CPF", "SMS", "PIX", "WHATSAPP", "SUV"}  # SUV: o gerar.py soletra «ésse u vê» (20/11)
avisos = []
for i, f in enumerate(falas):
    if re.search(r"\bhein\b", f, re.I): avisos.append(f"fala {i}: tem 'hein' (a voz le 'rein'): tirar")
    for w in re.findall(r"\b(Ih|Eita|Ué|Uai|Hum)\b", f): avisos.append(f"fala {i}: interjeicao '{w}' (Ed 23/11: a voz fala estranho): tirar")
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

# Guarda do FinMoovi (Ed, 23/11/2026: «cada video teria que falar uma funcionalidade diferente»): o recado do app
# mostra um recurso que nenhum outro video mostrou (lista em fabrica/finmoovi_recursos.json; marcar o "usado" la).
REC = json.load(open(f"{P}/fabrica/finmoovi_recursos.json", encoding="utf-8"))["recursos"]
fm = " ".join(f for f in falas if "FinMoovi" in f).lower()
achados = [r for r in REC if any(w in fm for w in r["palavras"])]
if fm and not achados: print("AVISO o recado do FinMoovi nao cita nenhum recurso da lista finmoovi_recursos.json")
for r in achados:
    outros = [v for v in r["usado"] if v != NN]
    if outros: print(f"AVISO FinMoovi repetido: '{r['recurso']}' ja apareceu no video {', '.join(outros)}: escolher outro recurso")
    elif NN in r["usado"]: print(f"FinMoovi: {r['recurso']} (so neste video)")
    else: print(f"FinMoovi: {r['recurso']} (novo: marcar {NN} em 'usado')")

# Guarda da repeticao (Ed, 27/11/2026: «os videos longos estao comecando a ficar sem graca... sempre repete as mesmas falas,
# das dicas, 3 dicas, papel de pao, etc»): o que apareceu nos 3 longos anteriores e volta aqui da AVISO.
FORMULAS = ["papel de pão", "Dica número um", "mesinha", "lápis", "linha por linha", "fiz a conta", "caneca", "extrato", "três dicas", "na ponta do lápis"]
ant = [v["nn"] for v in cal if v["nn"] < NN][-3:]
txt_ant = {a: open(f"{P}/robo-voz/roteiro-{a}.txt", encoding="utf-8").read().lower() for a in ant if os.path.exists(f"{P}/robo-voz/roteiro-{a}.txt")}
eu = " ".join(falas).lower()
for fo in FORMULAS:
    em = [a for a, t in txt_ant.items() if fo.lower() in t]
    if fo.lower() in eu and len(em) >= 2: print(f"AVISO repetido: '{fo}' ({eu.count(fo.lower())}x aqui) ja esteve nos videos {', '.join(em)}: trocar")
