# Medidor do tom (gratis, so numpy). Ed, 19/11/2026: «sem entonação de interrogação... no automático como vamos resolver isso?»
# Mede a altura da voz (o "pitch") quadro a quadro e diz se:
#   pergunta (?)   -> a voz SOBE no fim (o fim fica mais agudo que o meio da frase)
#   exclamacao (!) -> a voz VARIA bastante (fala com emocao, nao reta)
# Usado pelo gerar.py: se o tom nao bater, a frase e regravada com outra semente (ate 5 vezes) e fica a melhor.
import numpy as np

def alturas(x, sr):
    """altura da voz (Hz) a cada 10 ms; 0 onde nao ha voz"""
    j, h = int(0.04 * sr), int(0.01 * sr); lo, hi = int(sr / 350), int(sr / 70)
    ref = np.sqrt((x ** 2).mean()) * 0.5; out = []
    for a in range(0, len(x) - j, h):
        f = x[a:a + j] - x[a:a + j].mean()
        if np.sqrt((f ** 2).mean()) < ref: out.append(0.0); continue
        r = np.correlate(f, f, "full")[j - 1:]
        if r[0] <= 0: out.append(0.0); continue
        k = lo + int(np.argmax(r[lo:hi])); out.append(sr / k if r[k] / r[0] > 0.45 else 0.0)
    return np.array(out)

def tom(x, sr, texto):
    """(ok, numero, motivo). x = audio mono em numpy."""
    p = alturas(np.asarray(x, dtype=np.float64), sr); v = p[p > 0]
    if len(v) < 20: return True, 0.0, "tom: pouca voz para medir"
    fim = texto.strip().rstrip('"»”')[-1:]
    if fim == "?":
        cauda = v[-max(5, len(v) // 5):]
        r = float(np.median(cauda) / np.median(v[: max(10, int(len(v) * 0.7))]))
        return r >= 1.06, round(r, 3), f"tom de pergunta: fim/meio = {r:.2f} (precisa 1,06)"
    if fim == "!":
        r = float(np.percentile(v, 90) / np.percentile(v, 10))
        return r >= 1.45, round(r, 3), f"tom de espanto: variacao = {r:.2f} (precisa 1,45)"
    return True, 0.0, ""
