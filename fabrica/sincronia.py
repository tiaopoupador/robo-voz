# Peca do robo (qualquer video). Sincronia: junta o TEXTO DO ROTEIRO (certo) com o TEMPO de cada palavra falada (Whisper).
# Numeros: o roteiro escreve por extenso ("cinco mil setecentos e catorze"); a legenda usa o que o Whisper escreveu em algarismos (R$ 5.714).
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
            if temnum:  # numero: a legenda usa os algarismos do Whisper, com a pontuacao do fim do trecho do roteiro
                fim = re.search(r"[.,!?:;]+$", S[i2 - 1][0]); fim = fim.group(0) if fim else ""
                for n, b in enumerate(range(j1, j2)):
                    w = re.sub(r"[.,!?:;]+$", "", W[b][2]) + (fim if n == j2 - j1 - 1 else "")
                    out.append([W[b][0], W[b][1], w, S[i1][1]])
            else:  # o Whisper ouviu errado: fica o texto do roteiro, espalhado no tempo do trecho
                t0, t1 = W[j1][0], W[j2 - 1][1]; n = i2 - i1
                for q, a in enumerate(range(i1, i2)): out.append([t0 + (t1 - t0) * q / n, t0 + (t1 - t0) * (q + 1) / n, S[a][0], S[a][1]])
        elif op == "delete":  # palavra do roteiro que o Whisper nao pegou: entre a anterior e a seguinte
            t0 = out[-1][1] if out else 0; t1 = W[j1][0] if j1 < len(W) else t0 + 0.3 * (i2 - i1); n = i2 - i1
            for q, a in enumerate(range(i1, i2)): out.append([t0 + (t1 - t0) * q / n, t0 + (t1 - t0) * (q + 1) / n, S[a][0], S[a][1]])
        # insert: palavra que o Whisper ouviu a mais (respiracao, eco): ignora
    for o in out: o[0], o[1] = round(o[0], 2), round(o[1], 2)
    return out

def achar(ALIN, linha, frase):
    """Tempo em que a frase (texto do roteiro, ou algarismos) comeca a ser dita dentro da linha. None se nao achar."""
    alvo = [norm(w) for w in frase.split()]; alvo = [a for a in alvo if a]
    toks = [(o[0], norm(o[2])) for o in ALIN if o[3] == linha]
    for i in range(len(toks) - len(alvo) + 1):
        if all(toks[i + j][1] == alvo[j] for j in range(len(alvo))): return toks[i][0]
    return None
