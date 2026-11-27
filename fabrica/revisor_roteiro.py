# Revisor do ROTEIRO, antes da voz (Ed, 09/11/2026: «nao mostra no video em momento algum a mudanca, o que motivou a Sandra
# e o Marcos a irem no mercado com tudo anotado! (...) Tudo, tudo no roteiro e no video tem que fazer sentido. Nao pode
# criar uma cena do nada sem antes ter uma explicacao!»).
# O Claude le o roteiro inteiro como um leitor chato de livro e aponta, com o numero da linha:
#   1. VIRADA sem causa: personagem que muda de atitude sem a cena que mostra POR QUE mudou (o que viu, quem ajudou, o que sentiu);
#   2. cena, objeto, lugar ou pessoa que aparece do nada (sem ter sido apresentado antes);
#   3. salto de tempo ou de lugar sem aviso;
#   4. numero, dia ou fato que nao bate com outra linha;
#   5. promessa sem pagamento (o que foi anunciado e nunca aparece) e personagem que some sem fim de historia;
#   6. frase solta que um espectador novo nao entenderia;
#   7. cliche que a IA da a todo canal (lista em fabrica/cliches.txt, Ed 11/11: «quero ser unico»);
#   8. FUNIL do Joba (Ed 13/11, canal-dark longo.md secao 20): gancho-espelho, "vamos comecar", FinMoovi antes do fim,
#      2 pedidos falados, nunca dizer que acaba, fim = gancho do proximo video.
# Custo: uns US$ 0,20 a 0,30 por roteiro (credito de revisor). Uso: python fabrica/revisor_roteiro.py 02 [arquivo]
import json, os, re, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import chaves
ESQ = {"type": "object", "properties": {"problemas": {"type": "array", "items": {"type": "object", "properties": {
    "linha": {"type": "integer"}, "tipo": {"type": "string", "enum": ["virada sem causa", "do nada", "salto sem aviso", "nao bate", "promessa sem pagamento", "frase solta", "cliche", "funil", "continuidade", "repeticao"]},
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
7. CLICHÊ (o canal quer ser ÚNICO): qualquer item da LISTA DE CLICHÊS abaixo, ou outro recurso que todo canal de finanças feito
   com IA usa. Em como_resolver, troque por algo que só o bairro do Tião teria (um lugar, um objeto, um costume, um bordão nosso).
   Clichê é sempre grave.
8. FUNIL (sempre grave; aponte o que falta, na linha onde devia estar):
   a) a abertura (10 primeiros segundos) tem de ser um trecho chocante que se repete, com as MESMAS palavras, no meio do roteiro;
   b) antes do "vamos começar?" vem um CONVITE COM SENTIDO: "Se você [a situação de quem assiste], fica comigo até o fim que eu vou te
      [a promessa concreta deste vídeo]. Então já puxa a cadeira." Convite solto ("puxa a cadeira, vamos começar?") sem dizer por que ficar
      é falha. Depois da vinheta o Tião cumprimenta ("Chega mais! O café tá passado e hoje tem conta pra fazer.") e diz quem ele é, em 2 ou 3 frases.
      "Ô de casa" e "banquinho" são proibidos (o dono do canal recusou);
   c) o FinMoovi entra no fim do penúltimo capítulo, depois de anunciar o que vem ("mas antes, um recado rápido"), e NUNCA no fim;
      cada vídeo mostra UM recurso do app que os outros vídeos ainda não mostraram e que combina com o tema (o dono do canal,
      23/11/2026: «cada video teria que falar uma funcionalidade diferente»); repetir a «foto da notinha» de novo é falha;
   d) pelo menos 2 pedidos FALADOS de like/inscrição/comentário, cada um colado a um gancho do que vem a seguir;
   e) NUNCA dizer que o vídeo está acabando ("para terminar", "por último", "antes de ir embora", "chegamos ao fim", "resumindo");
   f) as últimas frases são o gancho para o PRÓXIMO vídeo, como um trailer: chama quem assiste pela situação dele (quem já passou
      e quem quer evitar), toca na dor com a causa, promete 2 ou 3 coisas concretas do próximo vídeo (a última sem contar o que é)
      e só então manda clicar ("Clica agora, que o vídeo já está aparecendo aqui na tela!"); o vídeo acaba logo ali.
      Gancho vago ("essa conversa é para você" sem dizer o que vem e para quem) é falha. Nunca "no próximo capítulo" entre partes.
      NOVELA (o dono do canal, 23/11/2026: «nao entregar o ouro (...) como se fosse um escritor de novelas»; sempre GRAVE): o fim
      MOSTRA um pedaço e CORTA antes do principal. Nunca conta o que acontece no próximo vídeo (o pedido, a resposta, a conta, o
      número, a virada). Mostra a porta abrindo, não quem diz o quê; diz que algo aconteceu, não o quê. Cartão na tela com o
      segredo do próximo vídeo também é falha grave;
   g) SEQUÊNCIA (o dono do canal, 19/11/2026: «o video x no final tem que fazer o gancho com o titulo do proximo video»): o gancho
      final repete a pergunta ou as palavras fortes do TÍTULO DO PRÓXIMO VÍDEO, que é: «{PROXIMO}». Se o fim não chama esse título,
      ou promete outro assunto, é falha grave;
   h) a abertura deste vídeo paga o que o FIM DO VÍDEO ANTERIOR prometeu: «{ANTERIOR}». Se o vídeo não entrega o prometido, é falha grave.
9. FALA DE GENTE (o dono do canal, 19/11/2026: «tem que deixar humanizado como se fosse um humano real»; sempre grave):
   a) sigla sem dizer o que é (diga o nome inteiro: "Fundo de Garantia de Operações", não "FGO");
   b) "hein" (a voz lê "rein"): proibido; interjeição solta que a voz lê estranho ("Ih", "Eita", "Ué", "Uai", "Hum") também (o dono do canal, 23/11/2026);
   c) frase solta sem contexto: "está escrito" sem dizer ONDE (site oficial de quem), "no site" sem dizer qual, fala de personagem
      curta demais para quem chegou agora entender;
   d) pergunta ou espanto escrito sem "?" ou "!" (a voz só sobe o tom com a pontuação);
   e) lista de dicas sem "Dica número um", "Dica número dois"...;
   f) frase complicada que um amigo não diria na mesa da cozinha;
   g) o gancho final vago: tem de dizer o que o próximo vídeo vai explicar, para quem ele é, e mandar clicar.
   h) RETOMADA SEM O QUÊ (o dono do canal, 25/11/2026: «Ela ainda nao pediu... está sem contexto... ela nao pediu o que?»): frase que
      volta a algo dito minutos antes ("ela ainda não pediu", "ele nunca contou", "aquilo") sem repetir O QUÊ. A volta diz a coisa
      com todas as letras ("a desculpa, ela ainda não pediu") e acrescenta o sentimento ou o porquê, para quem esqueceu ou chegou agora;
   i) QUEBRA-CABEÇA DO DINHEIRO E DOS OBJETOS (o dono do canal, 25/11/2026: «o Tião diz que nao emprestaria os 50 reais (...) mas
      depois fica parecendo que ele emprestou, tanto é que a Valéria devolveu os 50 reais»): quem deu o quê a quem, quanto e por quê
      tem de ficar claro em CADA passo. Se alguém devolve, o roteiro mostra antes o que foi dado e diz, na hora da devolução, o que
      está sendo devolvido ("os 50 reais que ele não emprestou, mas pagou em passagens"). Aponte toda conta, empréstimo ou objeto
      que o espectador pode entender ao contrário.
10. CONTINUIDADE (o dono do canal, 27/11/2026, recusou um vídeo por isto; sempre GRAVE): o ROTEIRO ANTERIOR INTEIRO vem no fim
   deste pedido. Aponte tudo o que contradiz o anterior, e tudo o que o anterior já contou e este conta DE NOVO como se fosse
   novidade (ex.: no anterior a personagem já decidiu vender o carro, e este volta a explicar a parcela do carro).
11. REPETIÇÃO (o dono do canal, 27/11/2026: «sempre repete as mesmas falas, das dicas, 3 dicas, papel de pão»; grave): a mesma
   fórmula do anterior (o mesmo formato de dicas, o mesmo objeto, o mesmo lugar, a mesma cena de conta) usada de novo.
   E o FIM: tem de ser capítulo de novela, com drama e mistério; fim morno é grave.
Não aponte estilo, ritmo ou gosto. Só lógica da história, clichê, funil e fala de gente. "grave" = o espectador notaria e ficaria confuso.
Em como_resolver, proponha a cena que falta, concreta (quem, onde, o que acontece), em uma ou duas frases.
No máximo 12 problemas, os mais importantes primeiro; cada texto com até 60 palavras.
O roteiro, uma linha por número:
"""

def revisar(NN, arq=None):
    import anthropic
    L = open(arq or f"{P}/robo-voz/roteiro-{NN}.txt", encoding="utf-8").read().splitlines()
    cl = [x.strip() for x in open(f"{P}/fabrica/cliches.txt", encoding="utf-8") if x.strip() and not x.startswith("#")]
    lista = "LISTA DE CLICHÊS (Ed, 11/11/2026):\n" + "\n".join("- " + x for x in cl) + "\n\nO roteiro, uma linha por número:"
    # a sequencia: o titulo do proximo (agenda.json) e as 2 ultimas falas do anterior (se ja tem voz)
    cal = json.load(open(f"{P}/fabrica/agenda.json", encoding="utf-8"))["calendario"]
    prox = next((v["titulo"] for v in cal if v["nn"] > NN), "(ainda sem próximo na agenda: ignore o item 8g)")
    ant = [v["nn"] for v in cal if v["nn"] < NN]
    arq_ant = f"{P}/robo-voz/roteiro-{ant[-1]}.txt" if ant else ""
    anterior = " ".join(open(arq_ant, encoding="utf-8").read().splitlines()[-2:]) if arq_ant and os.path.exists(arq_ant) else "(o roteiro anterior ainda não existe: ignore o item 8h)"
    pedido = PEDIDO.replace("{PROXIMO}", prox).replace("{ANTERIOR}", anterior)
    txt = pedido.replace("O roteiro, uma linha por número:", lista) + "\n".join(f"[{i}] {l}" for i, l in enumerate(L))
    # 27/11: o roteiro anterior INTEIRO (itens 10 e 11), uns US$ 0,03 a mais
    if arq_ant and os.path.exists(arq_ant): txt += "\n\nO ROTEIRO ANTERIOR INTEIRO (só para os itens 10 e 11, não o revise):\n" + open(arq_ant, encoding="utf-8").read()
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
