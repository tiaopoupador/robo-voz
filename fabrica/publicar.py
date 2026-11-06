# Peca do robo (fim da montagem, na nuvem): guarda o video no Drive, prepara a capa, agenda no YouTube e avisa o Ed por e-mail.
# Uso: SUBIR=sim python fabrica/publicar.py 02
# Regra (igual aos longos do FinMoovi): SEM CAPA O VIDEO NAO SOBE. Sem capa, o robo so avisa o Ed.
import importlib, json, os, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
NN = sys.argv[1]; SUBIR = os.environ.get("SUBIR", "sim") == "sim"
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
from fabrica import drive, correio
VID = f"{P}/videos-prontos/VIDEO-{NN}.mp4"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VID]).decode())
link_video = drive.guardar(NN, VID); print("no Drive:", link_video)
mont = json.load(open(f"{P}/montado/_montagem.json", encoding="utf-8")) if os.path.exists(f"{P}/montado/_montagem.json") else {}
# a capa: o arquivo CAPA* que o Ed salvou no Drive
ent = f"{P}/fabrica/videos/v{NN}/entrada"
if not os.path.isdir(ent):
    drive.baixar_tudo(NN)
capas = sorted(f for f in os.listdir(ent) if f.upper().startswith("CAPA") and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))) if os.path.isdir(ent) else []
txt = [f"# Vídeo {NN} montado", "", f"**{C.TITULO}**  ", f"Duração: {int(dur // 60)} min {int(dur % 60)} s  ", f"O vídeo inteiro (para você assistir antes): {link_video}", ""]
txt += [f"- Imagens suas que entraram: **{len(mont.get('do_ed', []))}**",
        f"- Pedidos seus que não chegaram (entrou a imagem do robô no lugar): **{len(mont.get('plano_b', []))}**"]
if mont.get("avisos"): txt += ["", "Avisos da montagem (eu confiro):", *[f"- {a}" for a in mont["avisos"][:15]]]
publicado = None
if not capas:
    txt += ["", "## ⚠️ Falta a capa", "Sem capa o vídeo **não sobe** (regra do canal). Salve a capa com o nome `CAPA.jpg` na pasta do vídeo no Drive e me avise: eu agendo na hora."]
elif SUBIR:
    # a principal e "CAPA..." sem letra; "CAPA-B...", "CAPA-C..." sao as versoes do teste do YouTube (Test & compare)
    import re as _re, shutil as _sh
    extra = [c for c in capas if _re.match(r"(?i)capa-[b-z]", c)]; capas = [c for c in capas if c not in extra] + extra
    teste = []
    for c in extra:
        subprocess.run([sys.executable, f"{P}/capas/preparar-capa.py", f"video-{NN}", f"{ent}/{c}"], check=True)
        d = f"{P}/capas/video-{NN}/teste-{c[5].upper()}.jpg"; _sh.copy(f"{P}/capas/video-{NN}/capa.jpg", d); teste.append(drive.guardar(NN, d))
    subprocess.run([sys.executable, f"{P}/capas/preparar-capa.py", f"video-{NN}", f"{ent}/{capas[0]}"], check=True)
    subprocess.run([sys.executable, f"{P}/youtube/subir.py", f"video-{NN}"], check=True)
    publicado = json.load(open(f"{P}/capas/video-{NN}/publicado.json", encoding="utf-8"))
    drive.guardar(NN, f"{P}/capas/video-{NN}/publicado.json"); drive.guardar(NN, f"{P}/capas/video-{NN}/capa.jpg")
    txt += ["", "## ✅ Agendado no YouTube", f"{publicado['url']}  ", f"Vai ao ar: {C.PUBLICA_TXT}. Até lá fica privado: dá para assistir e mudar o que quiser no Studio."]
    if teste:
        principal = drive.guardar(NN, f"{P}/capas/video-{NN}/capa.jpg")
        txt += ["", "## 🧪 Teste das capas (2 minutos seus)", "O YouTube não deixa um robô ligar o teste: ele só existe no Studio. As capas já estão no tamanho certo:",
                f"- principal: {principal}", *[f"- versão {chr(66 + i)}: {u}" for i, u in enumerate(teste)],
                "Baixe as 3, abra o vídeo no YouTube Studio, clique em **Miniatura**, depois **Testar e comparar**, e suba as 3. Ele testa sozinho quando o vídeo for ao ar."]
else:
    txt += ["", "Montado e guardado no Drive. Não subi no YouTube (pedido para só montar)."]
try:  # o banco: tudo o que o video usou, com nome que diz o que e, para reaproveitar
    from fabrica.banco import guardar_no_banco
    novos, total = guardar_no_banco(NN); txt += ["", f"📦 Banco do Drive: {novos} arquivos novos guardados (Tiao Poupador > banco), {total} na ficha do vídeo."]
except Exception as e:
    txt += ["", f"⚠️ Não consegui guardar no banco agora: {e}"]
open(f"{P}/fabrica/saida/{NN}-resultado.md", "w", encoding="utf-8").write("\n".join(txt))
try:  # o resultado vira recado na tarefa do Apexi Team; com o video agendado, a tarefa fecha
    from fabrica import team
    rec = f"Vídeo {NN} " + ("agendado ✅ " + publicado["url"] if publicado else ("montado, falta a capa ⚠️" if not capas else "montado (não subi)")) + f". Assistir: {link_video}. "
    rec += f"Suas imagens que entraram: {len(mont.get('do_ed', []))}. Faltaram (entrou a do robô): {len(mont.get('plano_b', []))}."
    print("Team:", team.recado(NN, rec, fechar=bool(publicado)))
except Exception as e: print("Team: recado falhou:", e)
correio.enviar(f"Tião Poupador · vídeo {NN}: " + ("agendado ✅" if publicado else ("falta a capa ⚠️" if not capas else "montado")), "\n".join(txt))
print("\n".join(txt))
