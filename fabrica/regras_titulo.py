# As regras de TITULO e CAPA do robo (o mesmo metodo de ~/.claude/skills/canal-dark/referencias/titulo-e-capa.md).
# Ed, 07/11/2026: «o titulo tem que ter misterio, gancho, tem que causar alguma coisa que a pessoa vai ter que assistir pra descobrir».
# Usado por temas.py (e depois pelo escritor do roteiro). revisar() e o "diretor chato": da nota e reescreve o que nao passar.
import json, re

REGRAS = """COMO ESCREVER O TÍTULO E A CAPA (medido nos canais que vigiamos):
REGRA-MÃE: o título faz a PERGUNTA, o vídeo dá a RESPOSTA, a capa dá o VEREDITO ou a provocação. Os três nunca dizem a mesma coisa.
O título NUNCA conta o final. Errado: "Você Pagou R$ 3.000 no Cruzeiro e Gastou o Dobro a Bordo" (já diz que gastou o dobro: ninguém precisa assistir).
Certo (o modelo, 508 mil views): "Como os Cruzeiros Te Enganam em Cada Nível" + capa "A ARMADILHA DO CRUZEIRO": promete o mecanismo escondido, ninguém conta qual é.

As famílias que ganham (views reais):
1. BASTIDOR de algo que a pessoa usa (a mais forte): "Como Resorts All-Inclusive Ganham Dinheiro" 1,2 mi; "How Banks Treat You at Every Level of Wealth" 1,18 mi; "Como Buffets Livres Ganham Dinheiro? (Não É Comida)" 420 mil. Só com coisa do dia a dia (empresa distante perde).
2. PARADOXO: "Por Que Parecer Pobre É TÃO Importante" 855 mil; "Por Que Pessoas Com Menos Dinheiro Sempre Têm Mais Que Você" 629 mil.
3. VOCÊ FEZ X E ALGO ESTRANHO ACONTECEU (fim no ar): "Você Escapou da Corrida dos Ratos e Ninguém Percebeu" 555 mil; "...Então as Coisas Ficaram Estranhas"; "...Tudo Mudou".
4. SITUAÇÃO ABSURDA: "Você Ganhou na Loteria e Apareceu no Trabalho no Dia Seguinte" 455 mil.
5. ESCADA "em cada nível" / "de R$ 0 a R$ 25 mi": a pessoa quer achar o próprio degrau.
6. "O QUE ACONTECE SE...": medo concreto, resposta escondida.
7. LISTA com adjetivo forte: "11 PEQUENOS NEGÓCIOS Com Margens de Lucro Gigantescas".
O que perde: título que dá a resposta; matemática seca de investidor; notícia; "psicologia/neurociência"; cópia RÁPIDA e fraca (o Edu fez "loteria" e "buffets" poucos dias depois do original: 305 e 193 views).
O que funciona: o TEMA de um campeão de 1 a 3 meses atrás (ou um campeão em inglês ainda sem versão brasileira), com o mesmo molde de título e palavras nossas: o Tuco pegou "Corrida dos Ratos e Ninguém Percebeu" 48 dias depois e fez 555 mil; o Edu pegou "Parecer Pobre" 73 dias depois e fez 499 mil.

Forma do título: até 60 caracteres; "Você" ou um personagem; no máximo 1 ou 2 palavras em MAIÚSCULAS para ênfase; número em reais só se ele aumentar a pergunta, nunca se for a resposta; parênteses de reviravolta servem ("(Não É Comida)", "(Veja Como)"); sem travessão; nunca prometer o que o vídeo não entrega.
Capa: 2 a 4 palavras gigantes que completam o título sem repetir: um veredito ("ALL INCLUSIVE É ROUBADA", "A ARMADILHA DO CRUZEIRO"), uma provocação ("PAREÇA POBRE?!", "NÃO É O SALÁRIO") ou uma pergunta com número ("CASAS DE R$600.000!?"). A cena tem um personagem com emoção forte, uma seta para o que importa e, se servir, etiquetas com números que abrem curiosidade sem explicar (a escada de preços R$ 300 > R$ 900 > R$ 7.000 no navio). Nunca mostra o final."""

NOTA = {"type": "object", "properties": {"itens": {"type": "array", "items": {"type": "object", "properties": {
    "i": {"type": "integer"}, "misterio": {"type": "integer"}, "emocao": {"type": "integer"}, "vida_da_pessoa": {"type": "integer"},
    "clareza": {"type": "integer"}, "longe_do_modelo": {"type": "integer"}, "problema": {"type": "string"},
    "titulo": {"type": "string"}, "capa_texto": {"type": "string"}},
    "required": ["i", "misterio", "emocao", "vida_da_pessoa", "clareza", "longe_do_modelo", "problema", "titulo", "capa_texto"],
    "additionalProperties": False}}}, "required": ["itens"], "additionalProperties": False}
CRIT = ("misterio", "emocao", "vida_da_pessoa", "clareza", "longe_do_modelo")

def limpa(t): return re.sub(r"\s*[—–]\s*", ", ", t).strip()

def revisar(cli, itens, voltas=3):
    """itens: [{titulo, capa_texto, o_que_esconde, modelo}]. O diretor chato da nota de 1 a 10 em cada criterio;
    o que nao passar de 8 em todos volta reescrito. Devolve (itens, custo, notas)."""
    custo, notas = 0.0, {}
    for _ in range(voltas):
        txt = REGRAS + "\n\nVocê é o DIRETOR CHATO do canal. Dê nota de 1 a 10 a cada título e capa em: misterio (esconde a resposta? se só de ler o título eu já sei o fim, nota baixa), emocao (medo, raiva, inveja, vontade de revanche, curiosidade forte), vida_da_pessoa (é o dinheiro de quem assiste?), clareza (entende em 1 segundo no celular), longe_do_modelo (não é cópia da frase do modelo). Em \"problema\" diga o defeito em 1 frase. Em \"titulo\" e \"capa_texto\": se alguma nota for menor que 8, REESCREVA melhor (mantendo o tema e o que o vídeo entrega); se tudo for 8 ou mais, repita igual.\n\n" + "\n".join(
            json.dumps({"i": i, "titulo": x["titulo"], "capa_texto": x["capa_texto"], "o_que_o_video_revela": x.get("o_que_esconde", ""), "titulo_do_modelo": x.get("modelo", "")}, ensure_ascii=False) for i, x in enumerate(itens))
        r = cli.messages.create(model="claude-sonnet-5-5", max_tokens=2000, messages=[{"role": "user", "content": txt}],
                                output_config={"format": {"type": "json_schema", "schema": NOTA}})
        custo += r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6
        ruins = 0
        for n in json.loads(next(b.text for b in r.content if b.type == "text"))["itens"]:
            if not 0 <= n["i"] < len(itens): continue
            notas[n["i"]] = {k: n[k] for k in CRIT} | {"problema": n["problema"], "reescrito": False}
            if min(n[k] for k in CRIT) < 8:
                ruins += 1; notas[n["i"]]["reescrito"] = True; itens[n["i"]]["titulo"] = limpa(n["titulo"]); itens[n["i"]]["capa_texto"] = limpa(n["capa_texto"])
        if not ruins: break
    return itens, custo, notas
