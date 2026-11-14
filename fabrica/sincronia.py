# Peca do robo (qualquer video). Sincronia: junta o TEXTO DO ROTEIRO (certo) com o TEMPO de cada palavra falada (Whisper).
# Numeros: o roteiro escreve por extenso; a legenda converte o PROPRIO roteiro em algarismos (em_algarismos): "trinta e dois e noventa" -> 32,90.
# O Whisper so da o tempo (14/11/2026: ele escreveu "30,2,90"). Numero pequeno solto fica por extenso, salvo se o Whisper o escreveu em algarismo.
# Uso: from sincronia import alinhar, achar ; ALIN = alinhar('02')
import difflib, json, os, re, unicodedata
P = os.path.dirname(os.path.abspath(__file__)) + "/.."

def norm(w):
    w = unicodedata.normalize("NFKD", w.lower()); w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9$]", "", w)

def palavras_whisper(NN):
    W = json.load(open(f"{P}/fabrica/saida/{NN}-palavras.json", encoding="utf-8"))
    out = []  # junta pedacos que o Whisper separa: "R" "$" "3" ".800" -> "R$ 3.800"; "10" "%" -> "10%"; "para" "-choque"
    for s, e, w in W:
        a = out[-1][2] if out else ""
        if out and (w.startswith("-") or w in ("%", "%.", "%,") or (w == "$" and a.endswith("R")) or re.match(r"^[.,]\d", w)):
            out[-1] = [out[-1][0], e, a + w]
        elif out and a.endswith("R$") and w[:1].isdigit(): out[-1] = [out[-1][0], e, a + " " + w]
        else: out.append([s, e, w])
    return out

def alinhar(NN):
    """Devolve lista de [inicio, fim, palavra, linha] com o texto do roteiro e o tempo da fala."""
    linhas = open(f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
    # o nome do app na voz se escreve "Fin Múvi"/"Fin Móvi" (para a pronuncia); na LEGENDA e sempre FinMoovi
    S = [(w, k) for k, l in enumerate(linhas) for w in re.sub(r"Fin\s*M[óúuo]+vi", "FinMoovi", l, flags=re.I).split()]
    W = palavras_whisper(NN)
    ns, nw = [norm(w) for w, _ in S], [norm(w[2]) for w in W]
    sm = difflib.SequenceMatcher(None, ns, nw, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for a, b in zip(range(i1, i2), range(j1, j2)): out.append([W[b][0], W[b][1], S[a][0], S[a][1]])
        elif op == "replace":
            temnum = any(re.search(r"\d", W[b][2]) for b in range(j1, j2))
            if True:  # 14/11/2026: fica SEMPRE o texto do roteiro; os numeros viram algarismos no fim (_numeros). Antes vinham do Whisper ("30,2,90").
                t0, t1 = W[j1][0], W[j2 - 1][1]; n = i2 - i1
                dig = any(re.search(r"\d", W[b][2]) for b in range(j1, j2))  # o Whisper escreveu em algarismos: o numero pequeno tambem vai em algarismo
                for q, a in enumerate(range(i1, i2)): out.append([t0 + (t1 - t0) * q / n, t0 + (t1 - t0) * (q + 1) / n, S[a][0], S[a][1]] + ([1] if dig else []))
        elif op == "delete":  # palavra do roteiro que o Whisper nao pegou: entre a anterior e a seguinte
            t0 = out[-1][1] if out else 0; t1 = W[j1][0] if j1 < len(W) else t0 + 0.3 * (i2 - i1); n = i2 - i1
            for q, a in enumerate(range(i1, i2)): out.append([t0 + (t1 - t0) * q / n, t0 + (t1 - t0) * (q + 1) / n, S[a][0], S[a][1]])
        # insert: palavra que o Whisper ouviu a mais (respiracao, eco): ignora
    out = [o[:4] for o in _numeros(out)]
    for o in out: o[0], o[1] = round(o[0], 2), round(o[1], 2)
    return out

def achar(ALIN, linha, frase):
    """Tempo em que a frase (texto do roteiro, ou algarismos) comeca a ser dita dentro da linha. None se nao achar."""
    alvo = [norm(w) for w in frase.split()]; alvo = [a for a in alvo if a]
    toks = [(o[0], norm(o[2])) for o in ALIN if o[3] == linha]
    for i in range(len(toks) - len(alvo) + 1):
        if all(toks[i + j][1] == alvo[j] for j in range(len(alvo))): return toks[i][0]
    return None

# ---- numeros por extenso -> algarismos (a transcricao escreve "58,30"; o gatilho vem escrito "cinquenta e oito") ----
_U = {"zero": 0, "um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10,
      "onze": 11, "doze": 12, "treze": 13, "catorze": 14, "quatorze": 14, "quinze": 15, "dezesseis": 16, "dezessete": 17, "dezoito": 18, "dezenove": 19,
      "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90,
      "cem": 100, "cento": 100, "duzentos": 200, "trezentos": 300, "quatrocentos": 400, "quinhentos": 500, "seiscentos": 600,
      "setecentos": 700, "oitocentos": 800, "novecentos": 900}
def numero_falado(frase):
    """le o numero do comeco da frase ("cinquenta e oito reais" -> 58); None se nao comeca com numero"""
    tot, parte, achou = 0, 0, False
    for w in frase.split():
        n = norm(w)
        if n in _U: parte += _U[n]; achou = True
        elif n == "e" and achou: continue
        elif n == "mil" and achou: tot += (parte or 1) * 1000; parte = 0
        elif n in ("milhao", "milhoes") and achou: tot += (parte or 1) * 1000000; parte = 0
        else: break
    return (tot + parte) if achou else None

def _fmt(n): return f"{n:,}".replace(",", ".")
def em_algarismos(palavras, digito=False):
    """troca os numeros por extenso de um trecho do roteiro por algarismos, mantendo as outras palavras e a pontuacao.
    "trinta e dois e noventa." -> ["32,90."]; "cinco mil setecentos e catorze" -> ["5.714"]; "dez por cento" -> ["10%"];
    "cinquenta e oito reais e trinta centavos" -> ["R$ 58,30"]. Devolve None se nao achou numero nenhum."""
    out, i, achou = [], 0, False
    N = [norm(w) for w in palavras]
    def numero(i):  # le um numero a partir de i: (valor, proximo i, pontuacao do fim) ou None
        tot, parte, j, ok, ult = 0, 0, i, False, i
        while j < len(N):
            n = N[j]
            if n in _U:
                v = _U[n]
                if ok and v < 100 and ((parte % 100 and v >= 10) or (parte % 10 and v < 10)): break  # "trinta e dois | e noventa"
                parte += v; ok = True; ult = j; j += 1
            elif n == "e" and ok and j + 1 < len(N) and N[j + 1] in _U: j += 1
            elif n == "mil" and (ok or j == i): tot += (parte or 1) * 1000; parte = 0; ok = True; ult = j; j += 1
            else: break
            if re.search(r"[.,!?:;]$", palavras[ult]) and ult == j - 1: break  # a frase acabou no meio
        if not ok: return None
        return tot + parte, ult + 1
    while i < len(N):
        r = numero(i) if (N[i] in _U or N[i] == "mil") else None
        if r and not digito and N[i] in ("um", "uma") and r[1] == i + 1 and not (r[1] < len(N) and N[r[1]] in ("real", "reais", "por")): r = None  # "uma cestinha"
        if not r: out.append(palavras[i]); i += 1; continue
        v, j = r; achou = True; txt = _fmt(v); fim = palavras[j - 1]
        if j < len(N) and N[j] in ("real", "reais"):  # "cinquenta e oito reais (e trinta centavos)"
            fim = palavras[j]; j += 1; txt = "R$ " + txt
            if j + 2 < len(N) + 1 and j < len(N) and N[j] == "e":
                c = numero(j + 1) if j + 1 < len(N) and N[j + 1] in _U else None
                if c and c[0] < 100: k = c[1]; txt += f",{c[0]:02d}"; fim = palavras[k - 1]; j = k
                if j < len(N) and N[j] in ("centavo", "centavos"): fim = palavras[j]; j += 1
        elif j + 1 < len(N) + 1 and j < len(N) and N[j] == "e" and j + 1 < len(N) and N[j + 1] in _U:  # "dezoito e noventa": centavos
            c = numero(j + 1)
            if c and c[0] < 100: txt += f",{c[0]:02d}"; fim = palavras[c[1] - 1]; j = c[1]
        if j + 1 < len(N) and N[j] == "por" and N[j + 1] == "cento": txt += "%"; fim = palavras[j + 1]; j += 2
        if "," in txt and not txt.startswith("R$") and j + 1 < len(N) and N[j] == "da" and N[j + 1] in ("manha", "tarde", "noite") or ("," in txt and i > 0 and N[i - 1] == "as" and not txt.startswith("R$")): txt = txt.replace(",", "h")  # "nove e dez da manha" -> 9h10
        if txt.isdigit() is False and re.fullmatch(r"1\.9\d\d|2\.0\d\d", txt) and i > 0 and N[i - 1] in ("de", "em", "ano"): txt = txt.replace(".", "")  # ano: 1999
        so_palavra = not digito and txt.isdigit() and int(txt) <= 10 and not (i > 0 and N[i - 1] in ("numero", "nota"))
        if so_palavra:  # 14/11: numero pequeno solto fica por extenso ("duas coisas", "tres regras"), como sempre foi
            out.extend(palavras[i:j]); i = j; continue
        p = re.search(r"[.,!?:;\"”»)]+$", fim); out.append(txt + (p.group(0) if p else "")); i = j
    return out if achou else None

_NUMW = set(_U) | {"e", "mil", "real", "reais", "centavo", "centavos", "por", "cento", "da", "manha", "tarde", "noite"}
def _numeros(out):
    """junta cada sequencia de palavras-numero do roteiro (mesma linha) e troca por algarismos, no tempo da sequencia inteira"""
    res, i = [], 0
    while i < len(out):
        if norm(out[i][2]) not in _U and norm(out[i][2]) != "mil": res.append(out[i]); i += 1; continue
        j = i
        while j < len(out) and out[j][3] == out[i][3] and norm(out[j][2]) in _NUMW: j += 1
        ws = [o[2] for o in out[i:j]]; ant = res[-1][2] if res and res[-1][3] == out[i][3] else ""
        conv = em_algarismos(([ant] if ant else []) + ws, any(len(o) > 4 for o in out[i:j]))
        if conv and ant: conv = conv[1:]
        if not conv: res.extend(out[i:j]); i = j; continue
        # o que sobrou sem converter no fim do trecho ("da manha", "e") fica como palavra
        t0, t1, n = out[i][0], out[j - 1][1], len(conv)
        for q, w in enumerate(conv): res.append([t0 + (t1 - t0) * q / n, t0 + (t1 - t0) * (q + 1) / n, w, out[i][3]])
        i = j
    return res

_achar = achar
def achar(ALIN, linha, frase):
    t = _achar(ALIN, linha, frase)
    if t is not None: return t
    alvo = [norm(w) for w in frase.split()]
    # o numero pode estar no comeco ou depois de palavras ("Deu novecentos")
    for c in range(len(alvo)):
        n = numero_falado(" ".join(frase.split()[c:]))
        if n is None: continue
        dig = str(n).rstrip("0") or "0"; antes = alvo[:c]  # "treze mil" -> 13 (bate com 13.175)
        toks = [(o[0], norm(o[2])) for o in ALIN if o[3] == linha]
        for i, (t0, w) in enumerate(toks):
            if re.sub(r"\D", "", w).startswith(dig) and all(i - len(antes) + j >= 0 and toks[i - len(antes) + j][1] == antes[j] for j in range(len(antes))):
                return toks[i - len(antes)][0] if antes else t0
        for t0, w in toks:  # sem conferir as palavras de antes
            if re.sub(r"\D", "", w).startswith(dig): return t0
        break
    return None
