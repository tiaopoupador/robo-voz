# 25/11/2026: a tela em pé (9:16) dos Shorts do canal, usada pelo reels.py (o gancho) e pelo resumo.py (o resumo de novela).
# Ed: «Teria que ter tipo uma faixa correndo tipo a da plantão do Tião dizendo: Assista a história inteira no canal...»,
#     «A frase ali em cima teria que ser mais ClickBait (...) Talvez até um emoji ali mostrando algo surpreso».
# Tela (1080 x 1920), de cima para baixo:
#   emoji espantado que pulsa · a frase isca (|| = linha nova, *palavra* = amarela) · a imagem do longo (sem a faixa da legenda
#   dele) · a faixa correndo, igual à do Plantão do Tião · a legenda grande, 3 palavras de cada vez · o canto de baixo livre
#   (botões do Instagram e do TikTok). No fim, o cartão com a medalha do Tião e o plim.
# Grátis: só ffmpeg.
import os, re, subprocess
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/..")
AZUL, VERMELHO, AMARELO = "0x0E1A2B", "0xD62828", "0xFFD43B"   # as cores do Plantão (render/src/motion/Plantao.tsx)
FAIXA = "ASSISTA À HISTÓRIA INTEIRA NO CANAL TIÃO POUPADOR   •   SE INSCREVE E DEIXA O SEU LIKE!   •   "
AMAR = r"{\c&H3BD4FF&}"; BRANCO = r"{\c&HFFFFFF&}"
Y_IMG, H_IMG = 650, 506          # a imagem do longo
Y_FAIXA, H_FAIXA = 1180, 84      # a faixa correndo
Y_LEG = 1400                     # a legenda
CARTAO = 3.2

def ts(s):
    h = int(s // 3600); m = int(s % 3600 // 60); return f"{h}:{m:02d}:{s % 60:05.2f}"
def pinta(txt):  # dinheiro e número em amarelo; *palavra* também
    txt = txt.replace("{", "(").replace("}", ")")
    txt = re.sub(r"(R\$\s?[\d.,]+(?:\s(?:mil|milhão|milhões))?|\b\d[\d.,]*|\bcinquenta\b|\breais\b)", lambda m: AMAR + m[1] + BRANCO, txt, flags=re.I)
    return re.sub(r"\*([^*]+)\*", lambda m: AMAR + m[1] + BRANCO, txt)

def juntar_palavras(W):
    """«R», «$», «50», «mil» viram «R$ 50 mil» numa palavra só (a legenda mostra junto)"""
    out = []
    for w in W:
        if out and ((w[2] == "$" and out[-1][2] == "R") or (out[-1][2] == "R$" and re.match(r"[\d.,]+", w[2]))
                    or (out[-1][2].startswith("R$ ") and re.match(r"(mil|milhão|milhões)\b", w[2]))):
            out[-1] = [out[-1][0], w[1], out[-1][2] + ("" if w[2] == "$" else " ") + w[2]]
        else: out.append(list(w))
    return out

def montar(video, trechos, palavras, T, topo, saida, emoji="1f631", voz=None, pasta=None, musica=None):
    """video: o VIDEO-NN.mp4 · trechos: [(ini, fim)] do longo, em ordem, que somam T segundos · palavras: [[ini, fim, palavra]] já no
    tempo do Short · topo: a frase isca · voz: um áudio novo (resumo) ou None (usa o som do próprio longo, o gancho)"""
    pasta = pasta or os.path.dirname(saida); os.makedirs(pasta, exist_ok=True)
    TOTAL = T + CARTAO
    palavras = juntar_palavras(palavras)
    blocos, cur = [], []
    for w in palavras:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[.!?:]$", w[2]): blocos.append(cur); cur = []
    if cur: blocos.append(cur)
    st = "&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,0,0,0,0,100,100,0,0,1"
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           f"Style: Leg,Baloo 2 Tiao,128,{st},7,3,5,60,60,0,1",
           f"Style: Topo,Baloo 2 Tiao,80,{st},6,2,8,50,50,0,1",
           f"Style: Fim,Baloo 2 Tiao,84,{st},5,2,5,80,80,0,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for i, b in enumerate(blocos):
        a = b[0][0]; z = blocos[i + 1][0][0] if i + 1 < len(blocos) else T
        z = min(z, b[-1][1] + 0.6, T)
        ass.append(f"Dialogue: 0,{ts(a)},{ts(z)},Leg,,0,0,0,,{{\\pos(540,{Y_LEG})\\fscx85\\fscy85\\t(0,120,\\fscx100\\fscy100)}}" + pinta(" ".join(w[2] for w in b)))
    ass.append(f"Dialogue: 0,{ts(0)},{ts(T)},Topo,,0,0,0,,{{\\pos(540,290)\\fad(250,0)}}" + pinta(topo).replace("|", "\\N"))
    ass.append(f"Dialogue: 0,{ts(T)},{ts(TOTAL)},Fim,,0,0,0,,{{\\pos(540,1330)\\fad(200,0)}}A história inteira\\Nestá no canal")
    ass.append(f"Dialogue: 0,{ts(T + 0.35)},{ts(TOTAL)},Topo,,0,0,0,,{{\\pos(540,1470)\\fad(200,0)\\fs96}}{AMAR}TIÃO POUPADOR")
    open(f"{pasta}/legenda.ass", "w", encoding="utf-8").write("\n".join(ass) + "\n")
    open(f"{pasta}/faixa.txt", "w", encoding="utf-8").write(FAIXA * 3)

    rel = lambda x: os.path.relpath(x, P).replace("\\", "/")
    fonte = rel(f"{P}/render/public/marca/fontes/Baloo2-ExtraBold.ttf")
    MED = f"{P}/render/public/marca/tiao-medalha.png"; PLIM = f"{P}/render/public/marca/plim.wav"
    EMO = f"{P}/render/public/marca/emoji/{emoji}.png"
    ent = ["-i", video, "-loop", "1", "-t", f"{CARTAO}", "-i", MED, "-i", PLIM, "-loop", "1", "-t", f"{T:.3f}", "-i", EMO]
    if voz: ent += ["-i", voz, "-ss", f"{musica[1]:.3f}", "-i", musica[0]]  # musica = (trilha.mp3 do longo, segundo de início)
    n = len(trechos)
    fc = "".join(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[t{i}];" for i, (a, b) in enumerate(trechos))
    fc += "".join(f"[t{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,fps=30,split=2[a][b];"
    fc += ("[a]crop=1920:900:0:0,scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.3:saturation=0.8[bg];"
           f"[b]crop=1920:900:0:0,scale=1080:{H_IMG}[fg];"
           f"[bg][fg]overlay=0:{Y_IMG}[c1];"
           # a faixa do Plantão: fundo azul, fio amarelo em cima, texto que corre, e a etiqueta vermelha fixa na esquerda
           f"[c1]drawbox=x=0:y={Y_FAIXA}:w=1080:h={H_FAIXA}:color={AZUL}@1:t=fill,drawbox=x=0:y={Y_FAIXA}:w=1080:h=6:color={AMARELO}@1:t=fill,"
           f"drawtext=fontfile={fonte}:textfile={rel(pasta)}/faixa.txt:fontsize=44:fontcolor=white:y={Y_FAIXA + 6}+({H_FAIXA - 6}-th)/2:x=300-mod(t*85\\,tw/3),"
           f"drawbox=x=0:y={Y_FAIXA + 6}:w=270:h={H_FAIXA - 6}:color={VERMELHO}@1:t=fill,"
           f"drawtext=fontfile={fonte}:text='ASSISTA':fontsize=42:fontcolor=white:y={Y_FAIXA + 6}+({H_FAIXA - 6}-th)/2:x=34[c2];"
           # o emoji espantado, que pulsa
           f"[3:v]scale=210:-1,format=rgba[emo];"
           f"[c2][emo]overlay=x=(W-w)/2:y=40+10*sin(t*6):shortest=1,setsar=1[corpo];"
           f"color=c=0x1d1a2b:s=1080x1920:d={CARTAO}:r=30[fundo];"
           "[1:v]scale=560:560,format=rgba,fade=in:st=0:d=0.3:alpha=1[med];"
           "[fundo][med]overlay=(W-w)/2:470:shortest=1,setsar=1[cart];"
           "[corpo][cart]concat=n=2:v=1:a=0[jun];"
           f"[jun]ass={rel(pasta)}/legenda.ass:fontsdir={rel(os.path.dirname(f'{P}/render/public/marca/fontes/x'))}[v];")
    if voz:
        # o resumo: a voz nova e, por baixo, SÓ a música do longo (a trilha.mp3, sem a narração), num trecho seguido.
        # 25/11 (Ed: «tem dois audios ao mesmo tempo»): antes ia o som do vídeo, com a narração do longo por baixo.
        fc += f"[5:a]atrim=0:{T:.3f},asetpts=PTS-STARTPTS,volume=0.35[fundo_a];"
        fc += f"[4:a]apad[vz];[vz][fundo_a]amix=inputs=2:duration=shortest:normalize=0,afade=t=out:st={T - 0.35:.3f}:d=0.35[voz];"
    else:
        fc += f"[0:a]atrim={trechos[0][0]:.3f}:{trechos[0][1]:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={T - 0.35:.3f}:d=0.35[voz];"
    fc += (f"[2:a]adelay={int(T * 1000 + 150)}|{int(T * 1000 + 150)},volume=0.9[plim];"
           f"[voz][plim]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{TOTAL:.3f}[au]")
    cmd = ["ffmpeg", "-v", "error", "-y", *ent, "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "20",
           "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True, cwd=P)
    return TOTAL
