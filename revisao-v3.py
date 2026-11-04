# Revisao v3 do roteiro 01 (pedido do Ed, 04/11/2026): prender mais, repetir menos.
# Gera roteiro-01-v3.txt, roteiro-01-v3-secoes.json e roteiro-01-v3-fontes.json
# (para cada linha: o arquivo de voz que ja existe com esse texto, ou null = gravar de novo).
import json, os
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
atual = open(P + "/robo-voz/roteiro-01.txt", encoding="utf-8").read().splitlines()
sec = json.load(open(P + "/robo-voz/roteiro-01-secoes.json"))
mapa = json.load(open(P + "/robo-voz/roteiro-01-mapa.json"))

troca = {
 3: "Ninguém naquela rua sabia o que o Tião sabia.",
 4: "Daqui a cinco anos, um caminhão vai parar na frente de uma dessas casas e levar embora a coisa que a rua inteira invejava. Fica comigo, porque o que aconteceu ali acontece com milhões de brasileiros, e quase ninguém conta.",
 5: "Mas antes, conhece o Tião direito. Trinta e poucos anos. Trabalha de carteira assinada, ganha três mil e oitocentos reais por mês. Acorda às cinco, pega dois ônibus quando o carro está na oficina, e volta tarde.",
 12: "São cento e quarenta e dois mil reais só de juros. Dinheiro que não vira picape, não vira casa, não vira nada. Vai para o banco.",
 13: "Mas, da janela, ninguém vê isso. A rua só vê a picape brilhando.",
 14: "Agora, abre comigo a conta do mês da casa do Marcos. Aquela que a rua não vê. Porque é aqui que a vitrine começa a rachar.",
 15: "Entram doze mil reais. Quase metade vai embora logo no começo do mês, só na picape: cinco mil setecentos e catorze. Sobram seis mil duzentos e oitenta e seis. Ainda parece bastante. Agora vem o resto.",
 20: "E antes de você achar que o Marcos é bobo: isso não é burrice. É algo que os estudiosos descreveram há mais de cem anos.",
 29: "Cada lanche no trabalho. Cada prestação pequena, daquelas de quarenta e nove e noventa, que a gente nem lembra que existe. E descobriu uma coisa que ninguém tinha contado pra ele: o problema nunca foi quanto ele ganhava.",
 59: "Pneu de picape não é pneu de carro popular. Três mil e duzentos reais. O Marcos não tinha reserva. Tudo o que sobrava ia para a picape. Então foi no cartão, em dez vezes. Mais uma parcela, em cima da outra parcela.",
 30: "Era para onde o dinheiro escapava. Eram os vazamentos. Pequenos, silenciosos, todo santo dia. Olha a lista daquela noite, do jeito que ele escreveu.",
 38: "Agora marca tudo o que se repete. Todo valor que aparece igualzinho, mês depois de mês. Assinatura, tarifa, seguro. É ali que o dinheiro escapa, porque o que se repete a gente para de enxergar.",
 41: "Cancelou o que não usava, ligou para o banco e tirou o seguro que nunca pediu, passou a levar marmita três vezes por semana. E aquele dinheiro parou de escapar. A segunda decisão: pagar a si mesmo primeiro.",
 42: "No dia em que o salário caía, antes de pagar qualquer conta, ele separava esse dinheiro numa aplicação simples de renda fixa. Não esperava sobrar. Porque, se esperasse sobrar, nunca sobrava.",
 44: "Os economistas Richard Thaler e Shlomo Benartzi mediram isso com trabalhadores americanos. Quando a poupança passou a subir sozinha, sem depender de força de vontade, a parte guardada do salário saiu de três e meio para mais de treze por cento.",
 45: "As pessoas não ficaram mais disciplinadas. Só pararam de precisar ser.",
 46: None,
 47: "E anotar tudo? Nas primeiras semanas foi chato. Teve dia que ele esqueceu. Teve semana que quis largar. A psicóloga Phillippa Lally, da University College London, acompanhou pessoas criando um hábito novo.",
 55: "Só que, no mesmo primeiro ano, uma coisa acontecia sem ninguém ver: a picape perdia valor. Um carro zero quilômetro, no Brasil, costuma perder entre dez e vinte por cento do preço só no primeiro ano.",
 56: "A dívida diminuía devagar. O preço da picape caía rápido. No segundo ano, o aperto começou. Para fechar o mês, a Sandra passou a pagar o mercado no cartão. A fatura não fechava, e eles pagavam só uma parte.",
 61: "No terceiro ano, veio o golpe maior. A empresa do Marcos cortou pessoal, e ele foi um dos demitidos. A renda do casal caiu pela metade.",
 67: "Uma compra de mil reais pode virar uma dívida de até dois mil. E foi isso que aconteceu com os pneus, com o mercado, com a farmácia. Tudo dobrando, devagar, sem barulho.",
 69: [
  "Até que, numa quinta-feira à noite, alguém bateu na porta do Tião. Era o Marcos. Sem a chave da picape na mão, sem sorriso, olhando para o chão.",
  "\"Tião, eu preciso de dois mil emprestados. É só para esse mês, para completar a parcela. Mês que vem eu te devolvo.\"",
  "E o Tião tinha. Nesse quarto ano, ele já tinha uns vinte e dois mil guardados. Mais de seis meses de vida sem salário nenhum. Dois mil não iam fazer falta.",
  "Ele pensou bastante. E disse não. Não por falta de vontade de ajudar. É que dois mil não salvavam a picape. Só empurravam o problema mais trinta dias, e no mês seguinte o Marcos ia estar devendo para mais um.",
  "O Tião disse: \"Dinheiro eu não te empresto. Mas, se quiser, eu te mostro o caderno.\" O Marcos deu um riso sem graça, virou as costas e foi embora. A porta bateu.",
  "Essa oferta ainda vai voltar nessa história.",
 ],
 70: "Agora, um estudo que vai mudar o jeito como você olha para o carro do vizinho. Nos anos noventa, dois pesquisadores americanos, Thomas Stanley e William Danko, passaram anos entrevistando milionários de verdade.",
 76: "Não precisa responder para ninguém. Só guarda o número. Se for menos de um mês, você não está sozinho, e não tem vergonha nenhuma nisso. A boa notícia é que esse número sobe, um pouco por mês.",
 79: ["O Tião está na mesma calçada, com a mesma caneca, lavando o mesmo carro. Do outro lado da rua, um caminhão-guincho está parado na frente da casa do Marcos. Depois de três meses sem pagar, o banco entrou na Justiça.",
      "O Marcos está de pé no portão, olhando a picape subir no guincho. A Sandra não aparece na janela."],
 83: "E o Tião? Nesses cinco anos, guardando trezentos e oitenta reais por mês, ele tinha juntado uns vinte e nove mil reais.",
 84: "Não é fortuna. Mas são mais de oito meses de vida garantida, sem depender de chefe nenhum. É consertar o carro sem fazer dívida.",
 86: "Entregou uma para o Marcos, ficou do lado dele, e, quando o guincho foi embora, disse só uma coisa: \"Aquela oferta continua de pé. Eu também já estive na mesa da cozinha com a mão na cabeça.\"",
 90: "E o Marcos? Dessa vez, ele aceitou ver o caderno. Seis meses depois, numa terça-feira, a luz da cozinha da casa dele ficou acesa até tarde.",
 91: "O Marcos e a Sandra na mesa, com papel, caneta e o extrato do banco aberto. Acharam os vazamentos deles. Quatro streamings, um seguro esquecido, uma academia que ninguém frequentava.",
 96: "O caderno funcionou para o Tião. Mas, como a gente viu, um hábito leva uns dois meses para pegar, e no papel quase todo mundo desiste antes. Por isso eu uso o Fin Múvi.",
}

# de onde vem a voz de cada linha que ja existe
def arquivo(i):
    return f"teste-vozes/pedacos-video-01-v1/p{mapa[i]}.wav" if mapa[i] is not None else f"teste-vozes/pedacos-video-01-v2/p{i}.wav"

linhas, flags, fontes = [], [], []
for i, t in enumerate(atual):
    novo = troca.get(i, t)
    if novo is None: continue
    bloco = novo if isinstance(novo, list) else [novo]
    for j, n in enumerate(bloco):
        assert "—" not in n and "–" not in n
        linhas.append(n)
        flags.append(sec[i] if j == len(bloco) - 1 else False)
        fontes.append(arquivo(i) if n == t else None)
open(P + "/robo-voz/roteiro-01-v3.txt", "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
json.dump(flags, open(P + "/robo-voz/roteiro-01-v3-secoes.json", "w"))
json.dump(fontes, open(P + "/robo-voz/roteiro-01-v3-fontes.json", "w"))
novos = [i for i, f in enumerate(fontes) if f is None]
w0 = sum(len(x.split()) for x in atual); w = sum(len(x.split()) for x in linhas)
print(len(linhas), "linhas;", len(novos), "para gravar:", novos)
print("palavras", w0, "->", w, "; estimativa", round(1347 / w0 * w / 60, 1), "min")
txt = " ".join(linhas).lower()
for p in ["parcela", "caderno", "trezentos e oitenta", "vazamento", "deixa eu", "em silêncio", "né?", "imprevisto", "simplesmente sumia"]:
    print(f"  {p}: {txt.count(p)}")
print("maior linha", max(len(x) for x in linhas))
