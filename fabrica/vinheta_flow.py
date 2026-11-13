# Vinheta com o Tião animado do Flow (Ed, 11/11/2026: «quero v1»): o clipe V1 vem com fundo verde; aqui ele é recortado
# e cortado para que a moeda caia na caneca exatamente no "tim" do jingle (1,40 s da Vinheta4).
# Uso: python fabrica/vinheta_flow.py CAMINHO_DO_V1.mp4 SEGUNDO_DO_TIM [--folha]
#   --folha  so faz uma folha de quadros (um a cada 0,25 s) para eu achar o segundo em que a moeda entra na caneca
# Sai: render/public/marca/vinheta-tiao.webm (com transparencia) e marca/vinheta-tiao.json ({"clip": ..., "dur": ...})
import json, os, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; OUT = P + "/render/public/marca"
src = sys.argv[1]; TOM = 1.40; DUR = 4.0
if "--folha" in sys.argv:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "fps=4,scale=320:-1,drawtext=text='%{pts\\:hms}':x=8:y=8:fontcolor=white:box=1:boxcolor=black,tile=6x6",
                    "-frames:v", "1", P + "/fabrica/saida/vinheta-flow-folha.jpg"], check=True)
    print("folha:", P + "/fabrica/saida/vinheta-flow-folha.jpg"); sys.exit()
tim = float(sys.argv[2]); ini = max(0.0, tim - TOM)
# recorte do verde: chromakey + tirar o reflexo verde da borda (despill), saída VP9 com alfa (o Remotion lê com transparent)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.2f}", "-t", f"{DUR:.2f}", "-i", src,
                "-vf", "chromakey=0x00FF00:0.16:0.06,despill=type=green:mix=0.6:expand=0.1,scale=-2:1080,fps=30,format=yuva420p",
                "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "6M", "-auto-alt-ref", "0", "-an", OUT + "/vinheta-tiao.webm"], check=True)
json.dump({"clip": "marca/vinheta-tiao.webm", "inicio_no_original": round(ini, 2), "tim": TOM}, open(OUT + "/vinheta-tiao.json", "w"))
print("ok", OUT + "/vinheta-tiao.webm", "(do segundo", round(ini, 2), "do original)")
