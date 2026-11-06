# Peca do robo: depois de montar, guarda no BANCO do Drive tudo o que o video usou, para reaproveitar e gastar menos.
#   Tiao Poupador/banco/imagens  e  Tiao Poupador/banco/clipes : copia (dentro do Drive, sem baixar) com nome que diz o que e
#   Tiao Poupador/banco/catalogo-video-NN.csv : a ficha de cada arquivo (mesmas colunas do banco/CATALOGO.csv do PC)
# Uso: python fabrica/banco.py 02   (pode rodar de novo: o que ja esta no banco nao se copia outra vez)
import csv, importlib, io, os, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica import drive
from fabrica.drive import D, api
COLS = "arquivo;tipo;categoria;lugar;acao;emocao;hora;personagens;fonte;custo_usd;usado_em_videos;nota".split(";")
QUEM = {"T": "tiao", "R": "sandra", "N": "marcos"}

def guardar_no_banco(NN):
    C = importlib.import_module(f"fabrica.videos.v{NN}.cenas"); NOMES = getattr(C, "NOMES", {})
    import json
    cj = f"{P}/fabrica/saida/{NN}-codigos.json"
    COD = {v: k for k, v in json.load(open(cj)).items()} if os.path.exists(cj) else {}  # M01 -> meta-sandra-ri-lista
    COD["CAPA"] = "capa"
    PASTA = {"imagem": "imagens", "clipe": "clipes"}
    raiz = drive.pasta("Tiao Poupador"); b = drive.pasta("banco", raiz)
    dest = {"imagem": drive.pasta("imagens", b), "clipe": drive.pasta("clipes", b)}
    ja = {f["name"] for k in dest.values() for f in drive.listar(k)}
    linhas, novos = [], 0
    def copiar(f, nome, tipo):
        nonlocal novos
        if nome not in ja: api(f"{D}/{f['id']}/copy", {"name": nome, "parents": [dest[tipo]]}); novos += 1
    # 1) o que o Ed gerou (meta.ai, Flow): o nome ja diz quem_onde_o-que
    e = drive.achar(f"video-{NN}", drive.achar("entrada", raiz))
    for f in (drive.listar(e) if e else []):
        n, ext = os.path.splitext(f["name"]); tipo = "clipe" if ext.lower() in (".mp4", ".mov", ".webm") else "imagem"
        cod = n.split("_")[0]; chave = COD.get(cod.split("-")[0].upper())
        desc = NOMES.get(chave) or "_".join(n.split("_")[1:])  # a descricao sai do roteiro, mesmo se o Ed salvou so o codigo
        partes = [cod] + (desc.split("_") + ["", "", ""])[:3]
        if partes[0].upper().startswith("CAPA"): cat, fonte = "capa", "meta.ai (Ed)"
        else: cat, fonte = ("cena", "Flow (Ed)") if tipo == "clipe" else ("cena", "meta.ai (Ed)")
        nome = f"v{NN}_{cod}" + (f"_{desc}" if desc else "") + ext.lower(); copiar(f, nome, tipo)
        linhas.append({"arquivo": f"{PASTA[tipo]}/{nome}", "tipo": tipo, "categoria": cat, "personagens": partes[1], "lugar": partes[2],
                       "acao": partes[3], "fonte": fonte, "custo_usd": "0", "usado_em_videos": NN})
    # 2) as imagens que o robo gerou na Cloudflare
    v = drive.achar(f"video-{NN}", drive.achar("robo", raiz)); img = drive.achar("img", v) if v else None
    for f in (drive.listar(img) if img else []):
        k = os.path.splitext(f["name"])[0]; spec = C.IMG.get(k) or C.IMG.get("cf-" + k) or ("", "", "")
        refs = spec[1] if isinstance(spec[1], str) else ""
        nome = f"v{NN}_cf_{NOMES.get(k, k)}.jpg"; copiar(f, nome, "imagem")
        linhas.append({"arquivo": f"imagens/{nome}", "tipo": "imagem", "categoria": "cena",
                       "personagens": "-".join(QUEM[r] for r in refs if r in QUEM), "acao": k, "fonte": "cloudflare flux-2-klein",
                       "custo_usd": "0", "usado_em_videos": NN, "nota": str(spec[2])[:300]})
    buf = io.StringIO(); w = csv.DictWriter(buf, COLS, delimiter=";", extrasaction="ignore"); w.writeheader(); w.writerows(linhas)
    cat = f"{P}/fabrica/saida/catalogo-video-{NN}.csv"; open(cat, "w", encoding="utf-8-sig", newline="").write(buf.getvalue())
    for f in drive.listar(b):
        if f["name"] == os.path.basename(cat): api(f"{D}/{f['id']}", metodo="DELETE", bruto=True)
    drive.subir(cat, b)
    print(f"banco: {novos} arquivos novos, {len(linhas)} na ficha do video {NN}")
    return novos, len(linhas)

if __name__ == "__main__":
    guardar_no_banco(sys.argv[1])
