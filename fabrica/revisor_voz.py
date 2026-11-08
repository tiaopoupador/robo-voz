# Revisor da voz (gratis, no PC): ouve cada pedaco gravado com o Whisper e mostra ONDE a fala saiu diferente do roteiro.
# Mais exigente que o narracao.py (que so pega pedaco muito ruim): aqui qualquer troca de palavra aparece, com o trecho.
# Uso: python fabrica/revisor_voz.py 02 teste-vozes/pedacos-video-02   -> fabrica/saida/02-voz-revisao.json
import difflib, json, os, re, sys, unicodedata
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
NN, PASTA = sys.argv[1], sys.argv[2]
textos = open(f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
from faster_whisper import WhisperModel
m = WhisperModel(os.environ.get("WHISPER", "small"), device="cpu", compute_type="int8")
U = "zero um dois tres quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
D = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
C = "_ cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()
def ext(n):  # o Whisper escreve 912; o roteiro diz "novecentos e doze": compara por extenso
    if n < 20: return U[n]
    if n < 100: return D[n // 10] + ("" if n % 10 == 0 else " e " + U[n % 10])
    if n == 100: return "cem"
    if n < 1000: return C[n // 100] + ("" if n % 100 == 0 else " e " + ext(n % 100))
    if n < 1000000:
        m, r = divmod(n, 1000); s = ("" if m == 1 else ext(m) + " ") + "mil"
        return s + ("" if r == 0 else (" e " if r < 100 or r % 100 == 0 else " ") + ext(r))
    return str(n)
def digitos(s):
    s = re.sub(r"(?<=\d)\.(?=\d{3})", "", s); s = re.sub(r"R\$\s*", "", s); s = s.replace("%", " por cento")
    s = re.sub(r"(\d+),(\d+)", lambda m: ext(int(m[1])) + " e " + ext(int(m[2])), s)
    return re.sub(r"\d+", lambda m: ext(int(m[0])), s)
def norm(s):
    s = digitos(s)
    s = unicodedata.normalize("NFKD", s.lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
IGUAIS = {("tchiao", "tiao"), ("fin", "fin"), ("muvi", "moovi"), ("num", "em um"), ("numa", "em uma"), ("journal", "jornal"), ("quilo", "kilo"), ("", "reais"), ("reais", "")}
out = []
SO = {int(x) for x in sys.argv[3].split(",")} if len(sys.argv) > 3 else None
for i, txt in enumerate(textos):
    if SO is not None and i not in SO: continue
    f = f"{PASTA}/p{i}.wav"
    if not os.path.exists(f): out.append({"linha": i, "problema": "faltou o audio"}); continue
    seg, _ = m.transcribe(f, language="pt", beam_size=5, initial_prompt="Tião, FinMoovi, reais")
    ouviu = " ".join(s.text for s in seg).strip()
    a, b = norm(txt.replace("FinMoovi", "Fin Muvi").replace("Tchião", "Tião")), norm(ouviu)
    sm = difflib.SequenceMatcher(None, a, b); trocas = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal": continue
        x, y = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        if (x, y) in IGUAIS or x.replace(" ", "") == y.replace(" ", ""): continue
        trocas.append(f"[{x}] -> [{y}]")
    if trocas and (sm.ratio() < 0.97 or len(trocas) > 1 or any(re.search(r"\d|mil|cent|reais", t) for t in trocas)):
        out.append({"linha": i, "parecido": round(sm.ratio(), 2), "trocas": trocas, "roteiro": txt[:200], "ouviu": ouviu[:200]})
        print(i, round(sm.ratio(), 2), "; ".join(trocas)[:200], flush=True)
json.dump(out, open(f"{P}/fabrica/saida/{NN}-voz-revisao.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("linhas para ouvir:", len(out), "de", len(textos))
