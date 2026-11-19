# A boca lida da VOZ (Ed, 19/11/2026: «nao tem como melhorar isso e chegar nuns 9,5?»). De graça, sem IA: só a conta do som.
# Para cada quadro (30 por segundo) sai:
#   abre    0..1  quanto a boca abre (a força da voz, com subida rápida e descida mais lenta, e fecha nas pausas);
#   largura -1..1 boca estreita e redonda («ó», «u»: som grave) ou esticada («i», «é», «s»: som agudo);
#   acento  0..1  a sílaba forte (o pico da voz): a cabeça acompanha e a sobrancelha sobe um pouco.
# A boca abre 2 quadros ANTES do som (os animadores fazem assim: o olho vê a boca e só depois ouve).
# Uso: python fabrica/boca_voz.py fala.wav [saida.json]   (sem saida: grava ao lado, fala.boca.json)
import json, sys, numpy as np
from scipy.io import wavfile
from scipy.signal import stft

FPS, ADIANTA = 30, 2

def ler(caminho):
    sr, x = wavfile.read(caminho); x = x.astype(np.float32)
    if x.ndim > 1: x = x.mean(1)
    return sr, x / (np.abs(x).max() + 1e-9)

def analisar(caminho):
    sr, x = ler(caminho); hop = sr // FPS
    f, t, Z = stft(x, sr, nperseg=hop * 2, noverlap=hop, boundary=None)
    M = np.abs(Z); fala = (f > 80) & (f < 5000)
    rms = np.sqrt((M[fala] ** 2).mean(0)); db = 20 * np.log10(rms + 1e-6)
    piso = np.percentile(db, 20); topo = np.percentile(db, 97)
    a = np.clip((db - piso - 6) / (topo - piso - 6 + 1e-6), 0, 1) ** 0.8
    # subida rápida, descida um pouco mais lenta (a boca não «pisca»)
    s = np.zeros_like(a)
    for i in range(len(a)): s[i] = a[i] if i == 0 else (0.75 * a[i] + 0.25 * s[i - 1] if a[i] > s[i - 1] else 0.45 * a[i] + 0.55 * s[i - 1])
    s[s < 0.06] = 0
    # largura pelo agudo: o centro do som (centroide) contra a mediana da própria voz
    cen = (f[:, None] * M).sum(0) / (M.sum(0) + 1e-9)
    ok = s > 0.1; med = np.median(cen[ok]) if ok.any() else 1500
    lg = np.clip((cen - med) / (med * 0.6), -1, 1) * (s > 0.05)
    lg = np.convolve(lg, np.ones(3) / 3, mode="same")
    # acento: pico local forte, no máximo um a cada 6 quadros
    ac = np.zeros_like(s); ult = -99
    for i in range(2, len(s) - 2):
        if s[i] > 0.55 and s[i] >= s[i - 2:i + 3].max() and i - ult >= 6: ac[i] = 1; ult = i
    ac = np.convolve(ac, [0.3, 0.7, 1, 0.7, 0.4, 0.2], mode="same")[:len(s)]
    # adianta 2 quadros
    pad = lambda v: np.concatenate([v[ADIANTA:], np.zeros(ADIANTA)])
    return dict(fps=FPS, abre=[round(float(v), 3) for v in pad(s)], largura=[round(float(v), 3) for v in pad(lg)],
                acento=[round(float(min(1, v)), 3) for v in pad(ac)])

if __name__ == "__main__":
    r = analisar(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].rsplit(".", 1)[0] + ".boca.json"
    json.dump(r, open(out, "w"), separators=(",", ":")); print(out, len(r["abre"]), "quadros")
