# A vinheta sonora do canal, 2 s (Ed, 11/11/2026: «crie uma vinheta de 2 s, mas tem que ser muito top»).
# Feita do zero em numpy (som nosso, ninguém mais tem): moeda caindo (zum), "tim" da moeda na caneca do Tião, e o
# jingle de 5 notas no ritmo do nome: TI-ÃO POU-PA-DOR (Sol Dó Mi Ré Sol). Duas versões:
#   a = marimba (alegre, de desenho animado)     b = o Tião assobiando (gente simples, do bairro)
# Uso: python fabrica/vinheta_som.py   -> render/public/marca/vinheta-{a,b}.wav (2 s), vinheta4-{a,b}.wav (4 s, com o Tião) e plim.wav
# 11/11 (Ed: «algo mais lento e talvez uns 4 s, e que apareça o Tião»): a de 4 s tem as notas mais espaçadas, um acorde
# suave na entrada do Tião e um sininho quando aparece o bordão. O plim (0,7 s) é a assinatura curta: barra Plantão e tela final.
import os, subprocess
import numpy as np
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; SR = 44100
OUT = P + "/render/public/marca"; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

HZ = [392.0, 523.25, 659.25, 587.33, 783.99]  # Sol Dó Mi Ré Sol: TI-ÃO POU-PA-DOR
VERSOES = {  # nome: (duração, quando a moeda bate, tempos das 5 sílabas, duração da última, extras)
    "vinheta": (2.0, 0.48, [0.62, 0.78, 0.94, 1.08, 1.24], 0.70, False),
    "vinheta4": (4.0, 1.40, [1.60, 1.88, 2.16, 2.40, 2.66], 1.00, True),   # o Vinheta4 do render usa os mesmos tempos
}
def fazer(nome, DUR, TOM, SIL, ULT, extras):
    global t
    t = np.arange(int(SR * DUR)) / SR
    NOTAS = [(q, h, SIL[i + 1] - q - 0.02) for i, (q, h) in enumerate(zip(SIL[:-1], HZ[:-1]))] + [(SIL[-1], HZ[-1], ULT)]  # assobio ligado, sem buraco
    def env(t0, ataque, queda, dur=None):
        x = t - t0; e = np.where(x < 0, 0, np.where(x < ataque, x / ataque, np.exp(-(x - ataque) / queda)))
        if dur: e *= np.clip((t0 + dur + 0.08 - t) / 0.08, 0, 1)
        return e

    def zum():  # a moeda caindo: ruído com um tom que sobe
        q = np.clip((t - (TOM - 0.8)) / 0.78, 0, 1); f = 500 + 2600 * q ** 2
        ph = 2 * np.pi * np.cumsum(f) / SR
        e = q ** 2 * (t < TOM - 0.01)
        return 0.10 * e * (np.sin(ph) * 0.5 + rng.standard_normal(len(t)) * 0.35)

    def tim(t0, forca=1.0):  # moeda batendo na caneca de louça: parciais inarmônicos, metal com louça
        s = sum(a * np.sin(2 * np.pi * f * (t - t0)) * env(t0, 0.001, q) for f, a, q in
                [(2637, 0.55, 0.22), (3951, 0.35, 0.16), (5274, 0.22, 0.11), (6810, 0.14, 0.07), (1318, 0.25, 0.30)])
        clique = rng.standard_normal(len(t)) * env(t0, 0.0005, 0.004) * 0.6
        return forca * 0.5 * (s + clique)

    def marimba(t0, f, d):
        return 0.42 * (np.sin(2 * np.pi * f * (t - t0)) * env(t0, 0.003, 0.18 if d < 0.5 else 0.45)
                       + 0.30 * np.sin(2 * np.pi * 4 * f * (t - t0)) * env(t0, 0.002, 0.05)
                       + 0.10 * np.sin(2 * np.pi * 10 * f * (t - t0)) * env(t0, 0.001, 0.015))

    def assobio():  # uma linha só, com escorregão entre as notas e vibrato de gente assobiando
        f = np.zeros(len(t)); a = np.zeros(len(t))
        for i, (t0, hz, d) in enumerate(NOTAS):
            i0, i1 = int(t0 * SR), int(min(DUR, t0 + d + 0.03) * SR)
            f[i0:i1] = hz * 2; a[i0:i1] = 1.0
            if i: ant = NOTAS[i - 1][1] * 2; g = int(0.035 * SR); f[i0:i0 + g] = np.linspace(ant, hz * 2, g)  # escorrega da nota anterior
        fim = int((NOTAS[-1][0] + 0.25) * SR); f[fim:] *= 1 + 0.05 * np.clip((t[fim:] - t[fim]) / 0.35, 0, 1)  # "fiu" no fim, sobe um pouquinho
        f *= 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 1.3) / 0.2, 0, 1)
        a = np.convolve(a, np.ones(int(0.025 * SR)) / int(0.025 * SR), "same") * np.clip((DUR - 0.05 - t) / 0.4, 0, 1)
        ph = 2 * np.pi * np.cumsum(f) / SR
        sopro = np.convolve(rng.standard_normal(len(t)), np.ones(8) / 8, "same") * 0.06
        return 0.38 * a * (np.sin(ph) + 0.08 * np.sin(2 * ph) + sopro)

    def baixo(t0):  # a pancada grave do final, com o tom caindo
        f = 98 * (1 + 0.6 * np.exp(-(t - t0).clip(0) / 0.05)); ph = 2 * np.pi * np.cumsum(f) / SR
        return 0.30 * np.sin(ph) * env(t0, 0.004, 0.28)

    def brilho(t0):  # estrelinhas no acorde final (Dó Mi Sol bem agudos, sininho)
        return sum(0.07 * np.sin(2 * np.pi * f * (t - t0 - k * 0.045)) * env(t0 + k * 0.045, 0.002, 0.35) for k, f in enumerate([2093, 2637, 3136, 4186]))

    base = zum() + tim(TOM) + tim(TOM + 0.09, 0.35) + baixo(SIL[-1]) + brilho(SIL[-1] + 0.02)
    if extras:  # acorde suave quando o Tião entra (Dó maior grave, ataque lento) e um sininho no bordão
        base = base + sum(0.07 * np.sin(2 * np.pi * h * t) * np.clip(t / 0.6, 0, 1) * np.clip((1.5 - t) / 0.5, 0, 1) for h in (130.81, 164.81, 196.0, 261.63))
        base = base + 0.25 * np.sin(2 * np.pi * 880 * (t - 0.22)) * env(0.22, 0.002, 0.06) + brilho(3.05) * 0.8
    for v, mel in (("a", sum(marimba(t0, f, d) for t0, f, d in NOTAS)), ("b", assobio())):
        x = base + mel
        x *= np.clip((DUR - t) / 0.12, 0, 1)                             # sem corte seco no fim
        x = np.tanh(1.3 * x) / np.tanh(1.3)                                 # cola tudo como um som só
        x = 0.89 * x / np.abs(x).max()
        pcm = (np.stack([x, x], 1) * 32767).astype(np.int16)
        tmp = f"{OUT}/_{nome}-{v}.raw"; pcm.tofile(tmp)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", tmp,
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", str(SR), f"{OUT}/{nome}-{v}.wav"], check=True)
        os.remove(tmp); print("ok", f"{nome}-{v}.wav")

for nome, cfg in VERSOES.items(): fazer(nome, *cfg)
# o plim: TI-ÃO-DOR em marimba bem rápida (0,7 s), a assinatura curta do canal
t = np.arange(int(SR * 0.7)) / SR
def _e(t0, q): x = t - t0; return np.where(x < 0, 0, np.exp(-x.clip(0) / q) * np.clip(x / 0.003, 0, 1))
x = sum(0.4 * (np.sin(2 * np.pi * h * (t - q)) * _e(q, 0.16) + 0.3 * np.sin(2 * np.pi * 4 * h * (t - q)) * _e(q, 0.04)) for q, h in ((0.0, 783.99), (0.09, 1046.5), (0.18, 1567.98)))
x = 0.89 * x / np.abs(x).max() * np.clip((0.7 - t) / 0.1, 0, 1)
(np.stack([x, x], 1) * 32767).astype(np.int16).tofile(OUT + "/_plim.raw")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", OUT + "/_plim.raw", "-af", "loudnorm=I=-16:TP=-2", "-ar", str(SR), OUT + "/plim.wav"], check=True)
os.remove(OUT + "/_plim.raw"); print("ok plim.wav")
