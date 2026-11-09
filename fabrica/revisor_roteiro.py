# Revisor do ROTEIRO, antes da voz (Ed, 09/11/2026: «nao mostra no video em momento algum a mudanca, o que motivou a Sandra
# e o Marcos a irem no mercado com tudo anotado! (...) Tudo, tudo no roteiro e no video tem que fazer sentido. Nao pode
# criar uma cena do nada sem antes ter uma explicacao!»).
# O Claude le o roteiro inteiro como um leitor chato de livro e aponta, com o numero da linha:
#   1. VIRADA sem causa: personagem que muda de atitude sem a cena que mostra POR QUE mudou (o que viu, quem ajudou, o que sentiu);
#   2. cena, objeto, lugar ou pessoa que aparece do nada (sem ter sido apresentado antes);
#   3. salto de tempo ou de lugar sem aviso;
#   4. numero, dia ou fato que nao bate com outra linha;
#   5. promessa sem pagamento (o que foi anunciado e nunca aparece) e personagem que some sem fim de historia;
#   6. frase solta que um espectador novo nao entenderia.
# Custo: uns US$ 0,20 a 0,30 por roteiro (credito de revisor). Uso: python fabrica/revisor_roteiro.py 02 [arquivo]
import json, os, re, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import chaves
ESQ = {"type": "object", "properties": {"problemas": {"type": "array", "items": {"type": "object", "properties": {
    "linha": {"type": "integer"}, "tipo": {"type": "string", "enum": ["virada sem causa", "do nada", "salto sem aviso", "nao bate", "promessa sem pagamento", "frase solta"]},
    "grave": {"type": "boolean"}, "problema": {"type": "string"}, "como_resolver": {"type": "string"}},
    "required": ["linha", "tipo", "grave", "problema", "como_resolver"], "additionalProperties": False}}},
    "required": ["problemas"], "additionalProperties": False}
PEDIDO = """Você é o leitor mais chato do mundo, lendo este roteiro de vídeo do YouTube como se fosse um LIVRO, do começo ao fim,
sem nunca ter visto outro vídeo do canal. O dono do canal exige que TUDO faça sentido e seja explicado nos mínimos detalhes.
Aponte cada lugar onde a história falha:
1. VIRADA SEM CAUSA (o mais grave): um personagem muda de atitude (passa a fazer lista, para de zombar, aprende algo) e o roteiro
   não MOSTRA, em cena, o que o fez mudar: o que ele viu, o que sentiu, com quem falou, quando e onde. Contar só o resultado é falha.
   Cada personagem que muda precisa da sua própria cena de causa (se dois mudam, os dois).
2. DO NADA: cena, objeto, lugar ou pessoa que aparece sem ter sido apresentado (ex.: "o caderno de capa azul" sem dizer o que é).
3. SALTO SEM AVISO: troca de tempo ou de lugar que o espectador não acompanha.
4. NÃO BATE: número, dia, quantidade ou fato que contradiz outra linha (faça as contas).
5. PROMESSA SEM PAGAMENTO: o que é anunciado e nunca aparece; personagem que some sem fim de história.
6. FRASE SOLTA: frase de efeito que um espectador novo não entenderia.
Não aponte estilo, ritmo ou gosto. Só lógica da história. "grave" = o espectador notaria e ficaria confuso.
Em como_resolver, proponha a cena que falta, concreta (quem, onde, o que acontece), em uma ou duas frases.
No máximo 12 problemas, os mais importantes primeiro; cada texto com até 60 palavras.
O roteiro, uma linha por número:
"""

def revisar(NN, arq=None):
    import anthropic
    L = open(arq or f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
    txt = PEDIDO + "\n".join(f"[{i}] {l}" for i, l in enumerate(L))
    cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"])
    with cli.messages.stream(model="claude-sonnet-5-5", max_tokens=32000, thinking={"type": "adaptive"},
                             output_config={"format": {"type": "json_schema", "schema": ESQ}},
                             messages=[{"role": "user", "content": txt}]) as s:
        r = s.get_final_message()
    t = next(b.text for b in r.content if b.type == "text")
    if r.stop_reason != "end_turn": raise RuntimeError(f"resposta cortada ({r.stop_reason}): aumentar max_tokens")
    pr = json.loads(t)["problemas"]
    for p in pr:
        for k in ("problema", "como_resolver"): p[k] = re.sub("\\s*[\u2014\u2013]\\s*", ", ", p[k])
    custo = r.usage.input_tokens * 3e-6 + r.usage.output_tokens * 15e-6
    return pr, custo

if __name__ == "__main__":
    NN = sys.argv[1]; pr, custo = revisar(NN, sys.argv[2] if len(sys.argv) > 2 else None)  # 2o: outro arquivo (ex.: a versao antiga, para testar)
    json.dump(pr, open(f"{P}/fabrica/saida/{NN}-roteiro-problemas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for p in sorted(pr, key=lambda p: (not p["grave"], p["linha"])):
        print(f"{'GRAVE' if p['grave'] else 'leve '} [{p['linha']}] {p['tipo']}: {p['problema']}\n        -> {p['como_resolver']}")
    print(f"problemas: {len(pr)} (graves: {sum(p['grave'] for p in pr)}) · custo: US$ {custo:.3f}")
