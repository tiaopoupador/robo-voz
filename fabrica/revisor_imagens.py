# Revisor de imagens (Ed, 07/11/2026: «aparece o Tiao com bracos a mais, pessoas com olhos deformados»).
# O Claude olha cada imagem da Cloudflare e diz se passa: pessoas certas, bracos/maos/olhos, bigode do Tiao, letras
# inventadas, o que cada mao segura. O imagens.py refaz de graca (outra semente) a que nao passar, ate 3 vezes.
# Custo: uns US$ 0,003 por imagem (creditos de revisor aprovados pelo Ed). Uso solto: python fabrica/revisor_imagens.py 02 nome [nome...]
import base64, io, json, os, re, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import chaves
VEREDITO = {"type": "object", "properties": {"passa": {"type": "boolean"}, "problemas": {"type": "array", "items": {"type": "string"}}},
            "required": ["passa", "problemas"], "additionalProperties": False}
QUEM = {"T": "Tião: homem de uns 30 anos, baixo e gordinho, cabelo preto bagunçado, BIGODE preto pequeno (obrigatório, tem de aparecer), polo amarela mostarda, relógio preto, bermuda jeans, chinelo",
        "R": "Sandra: mulher de uns 38, cabelo castanho ondulado comprido, óculos escuros na cabeça, blusa vermelha, jeans, SEM bigode",
        "N": "Marcos: homem alto e magro, cabelo escuro com gel, camisa branca, SEM bigode"}
_cli = None
def revisar(caminho, refs, pedido):
    """devolve (passa, problemas, custo_usd)"""
    global _cli
    import anthropic
    from PIL import Image
    if _cli is None: _cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"])
    im = Image.open(caminho).convert("RGB"); im.thumbnail((896, 896)); buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
    quem = "; ".join(QUEM[r] for r in refs if r in QUEM) or "personagens do bairro"
    txt = ("Você é o revisor chato de um desenho 2D para um vídeo do YouTube. Reprove se houver QUALQUER um destes defeitos:\n"
           "1. alguém com braço, mão ou perna a mais ou a menos, mão saindo de lugar errado, braço que sai das costas ou cruza o corpo sem ligar no ombro certo, objeto flutuando sem mão;\n"
           "2. rosto ou olhos deformados, olho maior que o outro, rosto derretido, rosto em objeto ou parede;\n"
           "3. a mesma pessoa desenhada duas vezes;\n"
           "4. letras ou palavras legíveis ou inventadas em placas, pacotes, papéis ou telas (rabisco ondulado é OK);\n"
           "5. o personagem principal diferente da descrição (no Tião: SEM BIGODE é reprovado);\n"
           "6. a cena mostra outra coisa que não a AÇÃO principal do pedido, ou a QUANTIDADE errada (pediu UMA sacola e aparecem duas = reprovado).\n"
           "NÃO reprove por detalhe pequeno: mão esquerda e direita trocadas, relógio ou chinelo fora do quadro, corpo um pouco mais magro, "
           "olhar para outro lado, enquadramento um pouco diferente, tipo de embalagem. Só reprove o que um espectador notaria em 2 segundos.\n"
           f"Personagem: {quem}.\nPedido da cena: {pedido[:600]}\n"
           "Pessoas pequenas no fundo podem ser simples. Responda passa=true só se estiver limpa; em problemas, frases curtas.")
    r = _cli.messages.create(model="claude-sonnet-5-5", max_tokens=800, output_config={"format": {"type": "json_schema", "schema": VEREDITO}},
                             messages=[{"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}, {"type": "text", "text": txt}]}])
    t = next((b.text for b in r.content if b.type == "text"), None)
    if t is None: raise RuntimeError(f"sem resposta: {r.stop_reason} {[b.type for b in r.content]}")
    j = json.loads(t)
    return j["passa"], [re.sub("\\s*[\u2014\u2013]\\s*", ", ", x) for x in j["problemas"]], r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6

if __name__ == "__main__":
    import importlib
    NN = sys.argv[1]; C = importlib.import_module(f"fabrica.videos.v{NN}.cenas"); tot = 0
    for n in sys.argv[2:]:
        q = C.IMG[n]; ok, pr, c = revisar(f"{P}/fabrica/videos/v{NN}/img/{n}.jpg", list(q[1]), q[2]); tot += c
        print("OK " if ok else "RUIM", n, "; ".join(pr), flush=True)
    print(f"custo: US$ {tot:.3f}")
