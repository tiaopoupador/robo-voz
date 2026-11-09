# Guarda dos rostos (Ed, 08/11/2026: «o emoji e a placa aparecem por cima do rosto do Tiao e do Marcos :(»).
# 1. rostos(): o Claude olha a imagem (ou um quadro do clipe) e diz onde esta cada rosto, em % da tela. Fica guardado em
#    fabrica/videos/vNN/rostos.json (uma vez por arquivo). Custo: uns US$ 0,003 por imagem (credito de revisor).
# 2. desviar(): antes de montar, cada balao, emoji, placa, etiqueta, carimbo e lista que cairia em cima de um rosto
#    muda para o lugar livre mais perto. Se nao houver lugar livre, vira aviso na montagem.
# Uso solto (para conferir um video inteiro): python fabrica/rostos.py 02
import base64, io, json, math, os, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
ESQUEMA = {"type": "object", "properties": {"rostos": {"type": "array", "items": {"type": "object", "properties": {
    "quem": {"type": "string"}, "x0": {"type": "number"}, "y0": {"type": "number"}, "x1": {"type": "number"}, "y1": {"type": "number"}},
    "required": ["quem", "x0", "y0", "x1", "y1"], "additionalProperties": False}}}, "required": ["rostos"], "additionalProperties": False}
_cli = None; CUSTO = [0.0]

def _jpg(caminho):
    from PIL import Image
    if caminho.lower().endswith((".mp4", ".mov")):  # clipe: o quadro do meio
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", caminho]).decode())
        b = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{d / 2:.2f}", "-i", caminho, "-frames:v", "1", "-f", "image2", "-c:v", "mjpeg", "-"])
        im = Image.open(io.BytesIO(b))
    else: im = Image.open(caminho)
    im = im.convert("RGB"); im.thumbnail((896, 896)); buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
    return buf.getvalue()

def perguntar(caminho):
    """[{quem, x0, y0, x1, y1}] em % da largura e da altura (cabeca inteira, com cabelo)"""
    global _cli
    import anthropic
    from fabrica.google import chaves
    if _cli is None: _cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"])
    txt = ("Esta imagem vai ocupar a tela inteira de um vídeo 16:9. Marque CADA rosto de pessoa ou personagem visível (a cabeça inteira, com o cabelo), "
           "inclusive de pessoas pequenas no fundo se o rosto for maior que 3% da largura. Dê x0, y0 (canto de cima à esquerda) e x1, y1 (canto de baixo à direita) "
           "em PORCENTAGEM da largura e da altura (0 a 100). Em quem, até 3 palavras. No máximo 12 rostos (os maiores). Sem rosto nenhum (só objetos, prateleiras, embalagens): lista vazia.")
    r = _cli.messages.create(model="claude-sonnet-5-5", max_tokens=2500, output_config={"format": {"type": "json_schema", "schema": ESQUEMA}},
                             messages=[{"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(_jpg(caminho)).decode()}}, {"type": "text", "text": txt}]}])
    CUSTO[0] += r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6
    t = next((b.text for b in r.content if b.type == "text"), None)
    if t is None: raise RuntimeError(f"sem resposta ({r.stop_reason})")
    return json.loads(t)["rostos"]

class Caderno:
    """rostos.json de um video: {nome do arquivo: {"tam": bytes, "rostos": [...]}}"""
    def __init__(self, NN):
        self.f = f"{P}/fabrica/videos/v{NN}/rostos.json"
        self.d = json.load(open(self.f, encoding="utf-8")) if os.path.exists(self.f) else {}
    def de(self, caminho):
        k = os.path.basename(caminho); tam = os.path.getsize(caminho)
        if k in self.d and self.d[k]["tam"] == tam: return self.d[k]["rostos"]
        self.d[k] = {"tam": tam, "rostos": perguntar(caminho)}
        json.dump(self.d, open(self.f, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        return self.d[k]["rostos"]

# ---- o tamanho de cada coisa por cima, em % da tela (1920 x 1080), igual ao render/src/motion ----
W, H = 19.2, 10.8  # px por 1%
def _limpo(t): return len(t.replace("*", ""))
def caixa(o, x=None, y=None):
    """(x0, y0, x1, y1) em % que a coisa ocupa"""
    t, x, y = o["t"], o.get("x", 50) if x is None else x, o.get("y", 50) if y is None else y
    n = _limpo(o.get("texto", ""))
    if t == "balao":
        lin = max(1, math.ceil(n / 19)); w = min(680, n * 32 + 80); h = lin * 64 + 48 + 46
        return (x - w / 2 / W, y - (h - 46) / 2 / H, x + w / 2 / W, y + (h - 46) / 2 / H + 46 / H)
    if t == "reacao": s = 330; return (x - s / 2 / W, y - s / 2 / H, x + s / 2 / W, y + s / 2 / H)
    if t in ("check", "xis", "brilho", "voa"): s = 240; return (x - s / 2 / W, y - s / 2 / H, x + s / 2 / W, y + s / 2 / H)
    if t == "placa":
        tam = o.get("tam", 92); w = n * tam * 0.6 + 84; h = tam * 1.15 + 28
        return (x - w / 2 / W, y - h / 2 / H, x + w / 2 / W, y + h / 2 / H)
    if t == "etiqueta": w = n * 84 * 0.58 + 92; h = 84 * 1.15 + 28; return (x - w / 2 / W, y, x + w / 2 / W, y + h / H)
    if t == "carimbo": w = n * 110 * 0.62 + 104; h = 110 * 1.15 + 40; return (x - w / 2 / W, y - h / 2 / H, x + w / 2 / W, y + h / 2 / H)
    if t == "lista":
        its = o.get("itens", []); w = max([len(i) for i in its] or [4]) * 56 * 0.55 + 68; h = len(its) * 84 + (len(its) - 1) * 18
        return (x - w / 2 / W, y - h / 2 / H, x + w / 2 / W, y + h / 2 / H)
    if t == "frasetopo":
        pos = o.get("pos", "topo")
        if pos == "topo":
            w = min(1700, n * 76 * 0.55 + 108); lin = max(1, math.ceil(n * 76 * 0.55 / 1600)); h = lin * 87 + 44
            return (50 - w / 2 / W, 56 / H, 50 + w / 2 / W, (56 + h) / H)
        lin = max(1, math.ceil(n / 16)); h = lin * 74 + 52; x0 = 60 / W if pos == "esq" else 100 - 700 / W
        return (x0, 14, x0 + 640 / W, 14 + h / H)
    return None

def _cruza(a, r, folga=2.5):
    """quanto do rosto r (inflado pela folga, por causa da camera que anda) a caixa a cobre, de 0 a 1"""
    rx0, ry0, rx1, ry1 = r["x0"] - folga, r["y0"] - folga, r["x1"] + folga, r["y1"] + folga
    ix = max(0, min(a[2], rx1) - max(a[0], rx0)); iy = max(0, min(a[3], ry1) - max(a[1], ry0))
    return ix * iy / max(1e-6, (rx1 - rx0) * (ry1 - ry0))
def _cruza_caixa(a, b): return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1])) > 0
def _dentro(a): return a[0] >= 1.5 and a[1] >= 1.5 and a[2] <= 98.5 and a[3] <= 80  # abaixo de 80% fica a legenda

def desviar(ov, rostos, nome=""):
    """muda de lugar o que cai em cima de rosto. Devolve a lista de avisos (o que mudou e o que nao deu)."""
    avisos, postos = [], []
    for o in ov:
        a = caixa(o)
        if a is None: continue
        ruim = [r for r in rostos if _cruza(a, r) > 0.04]
        if not ruim and not any(_cruza_caixa(a, b) for b in postos): postos.append(a); continue
        if o["t"] == "frasetopo":
            for pos in ("topo", "esq", "dir"):
                b = caixa({**o, "pos": pos})
                if not any(_cruza(b, r) > 0.04 for r in rostos) and not any(_cruza_caixa(b, c) for c in postos):
                    avisos.append(f"{nome}: frase '{o['texto'][:24]}' saiu do rosto ({o.get('pos', 'topo')} -> {pos})"); o["pos"] = pos; postos.append(b); break
            else: avisos.append(f"{nome}: frase '{o['texto'][:24]}' fica em cima de um rosto (nao achei lugar)")
            continue
        x0, y0, melhor = o.get("x", 50), o.get("y", 50), None
        for x in range(6, 95, 2):
            for y in range(6, 80, 2):
                b = caixa(o, x, y)
                if not _dentro(b) or any(_cruza(b, r) > 0.0 for r in rostos) or any(_cruza_caixa(b, c) for c in postos): continue
                d = (x - x0) ** 2 + (y - y0) ** 2
                if melhor is None or d < melhor[0]: melhor = (d, x, y, b)
        if melhor:
            avisos.append(f"{nome}: {o['t']} '{o.get('texto', o.get('e', ''))[:24]}' saiu do rosto ({x0},{y0} -> {melhor[1]},{melhor[2]})")
            o["x"], o["y"] = melhor[1], melhor[2]; postos.append(melhor[3])
        elif o["t"] in ("reacao", "check", "xis", "brilho", "voa"):  # sem lugar livre: o emoji sai, nunca cobre o rosto
            avisos.append(f"{nome}: {o['t']} '{o.get('e', '')}' tirado (nao havia lugar fora dos rostos)"); o["t"] = "fora"
        else: avisos.append(f"{nome}: {o['t']} '{o.get('texto', '')[:24]}' fica em cima de um rosto (nao achei lugar livre)"); postos.append(a)
    return avisos

if __name__ == "__main__":  # confere so: le o props.json montado e diz o que cai em cima de rosto
    NN = sys.argv[1]; cad = Caderno(NN)
    props = json.load(open(f"{P}/render/public/v{NN}/props.json", encoding="utf-8"))
    for c in props["cenas"]:
        if c.get("ov"):
            ros = cad.de(f"{P}/render/public/{c['src']}")
            for o in c["ov"]:
                a = caixa(o)
                if a and any(_cruza(a, r) > 0.04 for r in ros): print("EM CIMA DO ROSTO", c["chave"], o["t"], o.get("texto", o.get("e", "")))
    print(f"custo: US$ {CUSTO[0]:.3f}")
