# O som da vinheta NOVA (Ed, 13/11/2026, modelo RoboNuggets: um "vush" e uma melodia curta subindo, baixinha).
# Feito do zero em numpy, com os MESMOS tempos de render/src/motion/VinhetaNova.tsx (objeto T):
#   raio (vush que desce), leque abre (vush largo), fecha (zip), solta (tic), 3 quiques da moeda (tim, tim, tim),
#   vira (vupt + grave), jingle TI-AO POU-PA-DOR em marimba (a assinatura do canal) com estrelinhas, onda (vush que passa).
# Uso: python fabrica/vinheta_nova_som.py  -> render/public/marca/vinheta-nova.wav (4,5 s)
import os, subprocess
import numpy as np
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; SR = 44100; DUR = 4.5
OUT = P + "/render/public/marca"; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(13)
T = dict(raio=0.0, abre=0.32, fecha=0.82, solta=1.28, quica=[1.62, 1.9, 2.06], vira=2.28, sil=[2.62, 2.78, 2.96, 3.1, 3.24], onda=3.78)
HZ = [392.0, 523.25, 659.25, 587.33, 783.99]  # Sol Dó Mi Ré Sol: TI-ÃO POU-PA-DOR (o mesmo jingle de sempre)
t = np.arange(int(SR * DUR)) / SR

def env(t0, ataque, queda):
    x = t - t0
    return np.where(x < 0, 0, np.where(x < ataque, x / max(ataque, 1e-4), np.exp(-(x - ataque) / queda)))

def ruido_filtrado(f_ini, f_fim, t0, t1, forca):  # vush: ruído passado por um passa-banda que varre de f_ini a f_fim
    n = rng.standard_normal(len(t)); y = np.zeros(len(t))
    i0, i1 = int(t0 * SR), int(min(DUR, t1) * SR); seg = n[i0:i1]
    q = np.linspace(0, 1, i1 - i0); fc = f_ini + (f_fim - f_ini) * q
    # filtro de 2 polos simples, com a frequência mudando amostra a amostra
    a, b, out = 0.0, 0.0, np.zeros(i1 - i0)
    for k in range(i1 - i0):
        w = 2 * np.pi * fc[k] / SR; r = 0.97
        v = seg[k] + 2 * r * np.cos(w) * a - r * r * b; b, a = a, v; out[k] = v
    out /= np.abs(out).max() + 1e-9
    y[i0:i1] = out * np.sin(np.pi * q) ** 1.5 * forca
    return y

def tim(t0, forca):  # a moeda quicando no chão: metal claro, curto
    s = sum(a * np.sin(2 * np.pi * f * (t - t0)) * env(t0, 0.001, q) for f, a, q in
            [(2637, 0.55, 0.16), (3951, 0.35, 0.11), (5274, 0.2, 0.08), (1318, 0.2, 0.2)])
    return forca * 0.45 * (s + rng.standard_normal(len(t)) * env(t0, 0.0005, 0.003) * 0.5)

def marimba(t0, f, longa=False):
    return 0.42 * (np.sin(2 * np.pi * f * (t - t0)) * env(t0, 0.003, 0.5 if longa else 0.2)
                   + 0.30 * np.sin(2 * np.pi * 4 * f * (t - t0)) * env(t0, 0.002, 0.05)
                   + 0.10 * np.sin(2 * np.pi * 10 * f * (t - t0)) * env(t0, 0.001, 0.015))

def grave(t0):  # pancada grave quando a moeda vira medalha
    f = 98 * (1 + 0.7 * np.exp(-(t - t0).clip(0) / 0.05)); ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.32 * np.sin(ph) * env(t0, 0.004, 0.3)

def estrelas(t0):
    return sum(0.07 * np.sin(2 * np.pi * f * (t - t0 - k * 0.05)) * env(t0 + k * 0.05, 0.002, 0.35) for k, f in enumerate([2093, 2637, 3136, 4186]))

x = (ruido_filtrado(3000, 700, T["raio"], T["abre"] + 0.05, 0.26)          # o raio desce: o tom cai
     + ruido_filtrado(500, 2200, T["abre"], T["fecha"] + 0.05, 0.3)         # o leque abre
     + ruido_filtrado(2400, 4500, T["fecha"], T["solta"], 0.1)             # fecha numa linha: zip agudo
     + 0.3 * np.sin(2 * np.pi * 1760 * (t - T["solta"])) * env(T["solta"], 0.001, 0.03)  # tic: a linha solta
     + tim(T["quica"][0], 1.0) + tim(T["quica"][1], 0.55) + tim(T["quica"][2], 0.3)
     + ruido_filtrado(800, 3500, T["vira"] - 0.04, T["vira"] + 0.26, 0.14) + grave(T["vira"] + 0.14)
     + sum(marimba(q, h, i == 4) for i, (q, h) in enumerate(zip(T["sil"], HZ))) + estrelas(T["sil"][4] + 0.15)
     + ruido_filtrado(400, 1800, T["onda"], DUR, 0.32))                     # a onda passa
# a cama: um acorde de Dó bem baixinho por baixo de tudo (dá o "clima" de abertura de programa)
x = x + sum(0.035 * np.sin(2 * np.pi * h * t) for h in (130.81, 196.0, 261.63)) * np.clip((t - 0.3) / 0.8, 0, 1) * np.clip((DUR - t) / 0.7, 0, 1)
x *= np.clip((DUR - t) / 0.12, 0, 1)
x = np.tanh(1.3 * x) / np.tanh(1.3); x = 0.89 * x / np.abs(x).max()
pcm = (np.stack([x, x], 1) * 32767).astype(np.int16); tmp = OUT + "/_vn.raw"; pcm.tofile(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", tmp,
                "-af", "loudnorm=I=-15:TP=-1.5:LRA=7", "-ar", str(SR), OUT + "/vinheta-nova.wav"], check=True)
os.remove(tmp); print("ok vinheta-nova.wav")
