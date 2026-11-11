# Revisor de imagens (Ed, 07/11/2026: «aparece o Tiao com bracos a mais, pessoas com olhos deformados»).
# O Claude olha cada imagem da Cloudflare e diz se passa: pessoas certas, bracos/maos/olhos, bigode do Tiao, letras
# inventadas, o que cada mao segura. O imagens.py refaz de graca (outra semente) a que nao passar, ate 3 vezes.
# Custo: uns US$ 0,06 por imagem desde 09/11 (Opus 5.5 com zoom; antes US$ 0,003) (creditos de revisor aprovados pelo Ed). Uso solto: python fabrica/revisor_imagens.py 02 [--lote] nome [nome...]
import base64, io, json, os, re, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import chaves
VEREDITO = {"type": "object", "properties": {"passa": {"type": "boolean"}, "problemas": {"type": "array", "items": {"type": "string"}}},
            "required": ["passa", "problemas"], "additionalProperties": False}
QUEM = {"T": "Tião: homem de uns 30 anos, baixo e gordinho, cabelo preto bagunçado, BIGODE preto pequeno (obrigatório, tem de aparecer), polo amarela mostarda, relógio preto, bermuda jeans, chinelo",
        "R": "Sandra: mulher de uns 38, cabelo castanho ondulado comprido, óculos escuros na cabeça, blusa vermelha, jeans, SEM bigode",
        "N": "Marcos: homem alto e magro, cabelo escuro com gel, camisa branca, SEM bigode"}
_cli = None
# 09/11 (Ed: «os olhos das pessoas parecem caolhas... isso jamais poderia passar», «aparece 3 braços», «a picape está
# totalmente deformada», «fala 6 coisas riscadas mas só tem duas», «o carrinho está no meio de uma rua»): o revisor
# antigo era BONZINHO (mandava não reprovar detalhe e aceitar gente simples no fundo) e via a imagem pequena.
# Agora: Opus 5.5 pensando, a imagem inteira + 4 zooms (cada quarto em tamanho dobrado), TODA pessoa conta (também
# a do fundo), na dúvida reprova, e dá nota de 1 a 10: só passa com 8 ou mais e nenhum defeito.
VEREDITO = {"type": "object", "properties": {"nota": {"type": "integer"}, "passa": {"type": "boolean"}, "problemas": {"type": "array", "items": {"type": "string"}}},
            "required": ["nota", "passa", "problemas"], "additionalProperties": False}
REGRAS = """Você é o diretor de arte MAIS CHATO do mundo revisando um desenho 2D para um vídeo do YouTube. O dono do canal
reprova tudo o que parecer feio ou errado. Você recebe a imagem inteira e 4 zooms (os quatro quartos ampliados). Olhe os zooms
com calma: é neles que se vê olho torto e dedo a mais. Reprove se houver QUALQUER um destes defeitos, em QUALQUER pessoa,
também nas pequenas do fundo:
1. OLHOS: vesgo/caolho, um olho maior ou mais alto que o outro, os dois olhando para lados diferentes, olho borrado, derretido, sem pupila, deformado.
2. ROSTO deformado, torto, derretido, careta exagerada que fica feia, rosto em objeto ou parede.
3. CORPO: braço, mão ou perna a mais ou a menos (conte: cada pessoa tem 2 braços ligados aos ombros), braço saindo das costas,
   mão que segura algo e não está ligada a um braço, alça de bolsa no ombro sem a mão/braço que deveria estar ali, membro cortado sem motivo.
4. MÃOS: dedos tortos, grudados, a mais ou a menos, mão que vira massa.
5. OBJETOS e VEÍCULOS deformados ou incompletos: carro/picape sem porta, roda torta, lataria derretida, carrinho de mercado torto, objeto flutuando.
6. QUANTIDADE: a narração ou o pedido diz um número (seis itens riscados, duas coisas, uma sacola) e a imagem mostra outro. CONTE.
7. LUGAR errado: a cena tem de acontecer onde a história está (dentro do mercado, no corredor, na cozinha, na rua). Carrinho de mercado no meio da rua = reprovado.
8. AÇÃO ou OBJETO que CONTRADIZ a narração deste momento (a fala é sobre a bolsa no carrinho e não há bolsa; aparece produto na mão que ninguém citou).
   NÃO reprove só porque falta uma pessoa ou coisa que a frase cita de passagem: uma imagem mostra um momento, não a frase inteira.
9. A mesma pessoa duas vezes; personagem principal diferente da ficha (Tião SEM bigode ou com bigode GROSSO/grande é reprovado: o bigode dele é pequeno e fino).
10. Letras ou números legíveis inventados em placas, pacotes, papéis, telas (rabisco ondulado é OK).
11. Desenho feio no geral: traço amador, borrado, desproporcional, perspectiva quebrada.
Na dúvida, REPROVE. Não reprove só: lado esquerdo/direito trocado, enquadramento, tipo de embalagem, acessório pequeno da ficha fora de vista (relógio, chinelo), tipo de lápis.
nota: 10 = de cinema, 8 = boa sem nenhum defeito, 5 ou menos = tem defeito que se nota.
Em problemas, cada defeito numa frase curta (até 15 palavras), dizendo ONDE está (ex.: "mulher de verde no fundo: olhos vesgos")."""
def _jpg(im):
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}
def _params(caminho, refs, pedido, fala=None, contexto=None):
    """o pedido ao Claude (o mesmo na revisao solta e no lote)"""
    from PIL import Image
    im = Image.open(caminho).convert("RGB"); w, h = im.size
    inteira = im.copy(); inteira.thumbnail((1568, 1568))
    zooms = [im.crop((x, y, x + w // 2, y + h // 2)).resize((w, h)) for y in (0, h // 2) for x in (0, w // 2)]
    quem = "; ".join(QUEM[r] for r in refs if r in QUEM) or "personagens do bairro"
    txt = (REGRAS + f"\nPersonagens pedidos: {quem}.\nPedido da cena: {pedido[:700]}\n" +
           (f"A história até aqui (para saber o LUGAR e o momento): «{contexto[-700:]}»\n" if contexto else "") +
           (f"Narração enquanto a imagem aparece: «{fala[:400]}»\n" if fala else "") +
           "A 1a imagem é a inteira; depois vêm os zooms: alto-esquerda, alto-direita, baixo-esquerda, baixo-direita.")
    conteudo = [_jpg(inteira)] + [_jpg(z) for z in zooms] + [{"type": "text", "text": txt}]
    return {"model": "claude-opus-5-5", "max_tokens": 16000, "thinking": {"type": "adaptive"},
            "output_config": {"effort": "high", "format": {"type": "json_schema", "schema": VEREDITO}},
            "messages": [{"role": "user", "content": conteudo}]}

def _veredito(msg, metade=False):
    t = next((b.text for b in msg.content if b.type == "text"), None)
    if t is None: raise RuntimeError(f"sem resposta: {msg.stop_reason} {[b.type for b in msg.content]}")
    j = json.loads(t)
    ok = bool(j["passa"]) and j["nota"] >= 8 and not j["problemas"]
    pr = [re.sub(r"\s*[\u2014\u2013]\s*", ", ", x) for x in j["problemas"]] + ([] if ok or j["problemas"] else [f"nota {j['nota']}"])
    c = msg.usage.input_tokens * 5e-6 + msg.usage.output_tokens * 25e-6
    return ok, pr, c / 2 if metade else c

def _cliente():
    global _cli
    import anthropic
    if _cli is None: _cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"])
    return _cli

def revisar(caminho, refs, pedido, fala=None, contexto=None):
    """devolve (passa, problemas, custo_usd). contexto = o que a história contou antes (lugar, momento)."""
    return _veredito(_cliente().messages.create(**_params(caminho, refs, pedido, fala, contexto)))

# Ed, 11/11/2026: «talvez compensaria mudar pra isso» (lote = metade do preço, o mesmo Opus e as mesmas regras).
# Para revisar muitas imagens de uma vez (o lote volta em minutos, as vezes horas). O robo que gera e refaz na hora usa revisar().
def revisar_lote(itens, espera=20, teto_s=6 * 3600):
    """itens = {nome: (caminho, refs, pedido, fala, contexto)} -> {nome: (passa, problemas, custo_usd)}"""
    import time
    cli = _cliente()
    ids = {f"img{i:03d}": n for i, n in enumerate(itens)}
    lote = cli.messages.batches.create(requests=[{"custom_id": k, "params": _params(*itens[n])} for k, n in ids.items()])
    print(f"lote {lote.id}: {len(ids)} imagens, esperando...", flush=True); t0 = time.time()
    while cli.messages.batches.retrieve(lote.id).processing_status != "ended":
        if time.time() - t0 > teto_s: raise RuntimeError(f"lote {lote.id} passou de {teto_s} s")
        time.sleep(espera)
    out = {}
    for r in cli.messages.batches.results(lote.id):
        n = ids[r.custom_id]
        out[n] = _veredito(r.result.message, metade=True) if r.result.type == "succeeded" else (False, [f"revisão falhou: {r.result.type}"], 0.0)
    print(f"lote pronto em {time.time() - t0:.0f} s", flush=True)
    return out

def contexto(NN, C, nome):
    """(fala no momento da imagem, as 2 falas antes): o revisor precisa saber o LUGAR da cena"""
    R = open(f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
    for k in sorted(C.L):
        for g, t, c in C.L[k]:
            n = c[0] if isinstance(c, tuple) else c
            if n == nome or (isinstance(c, dict) and nome in c.get("imgs", [])):
                i = R[k].lower().find(g.lower()) if g != "^" else 0
                return R[k][max(0, i):][:400], " ".join(R[max(0, k - 2):k]) + " " + R[k][:max(0, i)]
    return None, None

if __name__ == "__main__":
    import importlib
    NN = sys.argv[1]; C = importlib.import_module(f"fabrica.videos.v{NN}.cenas"); tot = 0
    nomes = [n for n in sys.argv[2:] if n != "--lote"]
    itens = {n: (f"{P}/fabrica/videos/v{NN}/img/{n}.jpg", list(C.IMG[n][1]), C.IMG[n][2], *contexto(NN, C, n)) for n in nomes}
    res = revisar_lote(itens) if "--lote" in sys.argv else {n: revisar(*itens[n]) for n in nomes}
    for n, (ok, pr, c) in res.items():
        tot += c; print("OK " if ok else "RUIM", n, "; ".join(pr), flush=True)
    print(f"custo: US$ {tot:.3f}")
