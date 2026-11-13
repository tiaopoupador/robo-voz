# O som da tela final NOVA (Ed, 13/11/2026), mesma família da vinheta nova (fabrica/vinheta_nova_som.py).
# Tempos iguais a TF em render/src/motion/TelaFinalNova.tsx: a onda entra (vush), o quadro salta (pancada grave),
# a moeda cai e quica (tim, tim, tim), vira a medalha (vupt + grave), CLICA E VÊ AGORA no jingle TI-ÃO POU-PA-DOR
# (4 notas nas palavras, a 5ª no botão INSCREVA-SE, com estrelinhas), a seta (zip), e dois toques leves depois.
# Baixinho: a trilha do vídeo continua por baixo. Uso: python fabrica/tela_final_som.py -> render/public/marca/tela-final-nova.wav
import os, subprocess, sys
import numpy as np
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; SR = 44100; DUR = 10.0
OUT = P + "/render/public/marca"; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(31)
TF = dict(onda=0.0, quadro=0.45, cai=0.95, quica=[1.32, 1.6, 1.76], vira=1.9, pal=[2.45, 2.62, 2.78, 2.96], botao=3.3, seta=3.0,
          cursor=[3.9, 5.3, 6.7, 8.1], clique=[4.5, 5.9, 7.3, 8.7], redesenha=[5.15, 7.95], giraDeNovo=6.05)
# (Ed 13/11: «mais açao»): cursor que voa (vush leve), clique (tic duplo), no vídeo as letras pulam (marimba subindo),
# no INSCREVA-SE o sino toca; a seta se redesenha (zip); a medalha gira de novo (vupt)
HZ = [392.0, 523.25, 659.25, 587.33, 783.99]  # TI-ÃO POU-PA-DOR
t = np.arange(int(SR * DUR)) / SR

def env(t0, ataque, queda):
    x = t - t0
    return np.where(x < 0, 0, np.where(x < ataque, x / max(ataque, 1e-4), np.exp(-np.maximum(x - ataque, 0) / queda)))

def vush(f_ini, f_fim, t0, t1, forca):
    n = rng.standard_normal(len(t)); y = np.zeros(len(t))
    i0, i1 = int(t0 * SR), int(min(DUR, t1) * SR); seg = n[i0:i1]
    q = np.linspace(0, 1, i1 - i0); fc = f_ini + (f_fim - f_ini) * q
    a, b, out = 0.0, 0.0, np.zeros(i1 - i0)
    for k in range(i1 - i0):
        w = 2 * np.pi * fc[k] / SR; r = 0.97
        v = seg[k] + 2 * r * np.cos(w) * a - r * r * b; b, a = a, v; out[k] = v
    out /= np.abs(out).max() + 1e-9
    y[i0:i1] = out * np.sin(np.pi * q) ** 1.5 * forca
    return y

def tim(t0, forca):
    s = sum(a * np.sin(2 * np.pi * f * (t - t0)) * env(t0, 0.001, q) for f, a, q in
            [(2637, 0.55, 0.16), (3951, 0.35, 0.11), (5274, 0.2, 0.08), (1318, 0.2, 0.2)])
    return forca * 0.45 * (s + rng.standard_normal(len(t)) * env(t0, 0.0005, 0.003) * 0.5)

def marimba(t0, f, longa=False, forca=1.0):
    return forca * 0.42 * (np.sin(2 * np.pi * f * (t - t0)) * env(t0, 0.003, 0.5 if longa else 0.2)
                           + 0.30 * np.sin(2 * np.pi * 4 * f * (t - t0)) * env(t0, 0.002, 0.05)
                           + 0.10 * np.sin(2 * np.pi * 10 * f * (t - t0)) * env(t0, 0.001, 0.015))

def grave(t0, forca=1.0):
    f = 98 * (1 + 0.7 * np.exp(-(t - t0).clip(0) / 0.05)); ph = 2 * np.pi * np.cumsum(f) / SR
    return forca * 0.32 * np.sin(ph) * env(t0, 0.004, 0.3)

def estrelas(t0):
    return sum(0.07 * np.sin(2 * np.pi * f * (t - t0 - k * 0.05)) * env(t0 + k * 0.05, 0.002, 0.35) for k, f in enumerate([2093, 2637, 3136, 4186]))

def clique(t0):  # o tic do mouse: dois estalos curtos (desce e sobe)
    return sum(0.35 * np.sin(2 * np.pi * f * (t - t1)) * env(t1, 0.0005, 0.012) for t1, f in ((t0, 3200), (t0 + 0.07, 2600)))

def sino(t0):  # o sino de notificação: parciais de sino, queda longa
    return sum(a * np.sin(2 * np.pi * f * (t - t0)) * env(t0, 0.002, q) for f, a, q in ((1568, 0.22, 0.7), (2349, 0.12, 0.45), (3136, 0.08, 0.3), (4186, 0.05, 0.2)))

x = (vush(400, 1800, TF["onda"], 0.85, 0.32) + grave(TF["quadro"] + 0.08, 0.8)
     + vush(2600, 800, TF["cai"], TF["quica"][0] + 0.02, 0.12)
     + tim(TF["quica"][0], 1.0) + tim(TF["quica"][1], 0.55) + tim(TF["quica"][2], 0.3)
     + vush(800, 3500, TF["vira"] - 0.04, TF["vira"] + 0.28, 0.14) + grave(TF["vira"] + 0.15, 0.7)
     + sum(marimba(q, h) for q, h in zip(TF["pal"], HZ[:4]))
     + vush(1500, 4200, TF["seta"], TF["seta"] + 0.4, 0.08)
     + marimba(TF["botao"], HZ[4], True) + estrelas(TF["botao"] + 0.15)
     + sum(vush(900, 2600, c, c + 0.5, 0.07) for c in TF["cursor"])
     + sum(clique(c) for c in TF["clique"])
     + sum(sum(marimba(c + 0.05 + k * 0.07, h, False, 0.45) for k, h in enumerate(HZ[:4])) for c in TF["clique"][0::2])
     + sum(sino(c + 0.03) for c in TF["clique"][1::2])
     + sum(vush(1500, 4200, r - 0.15, r + 0.35, 0.06) for r in TF["redesenha"])
     + vush(800, 3500, TF["giraDeNovo"], TF["giraDeNovo"] + 0.5, 0.1))
x *= np.clip((DUR - t) / 0.3, 0, 1)
x = np.tanh(1.3 * x) / np.tanh(1.3); x = 0.89 * x / np.abs(x).max()
pcm = (np.stack([x, x], 1) * 32767).astype(np.int16); tmp = OUT + "/_tf.raw"; pcm.tofile(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", tmp,
                "-af", "loudnorm=I=-18:TP=-1.5:LRA=7", "-ar", str(SR), OUT + "/tela-final-nova.wav"], check=True)
os.remove(tmp); print("ok tela-final-nova.wav")
