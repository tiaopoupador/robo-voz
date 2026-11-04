# Revisao v4 do roteiro 01 (pedido do Ed, 04/11/2026):
# - lembrar o contexto sempre que a historia volta a uma cena (like, caderno, guincho, dinheiro que sumia)
# - carro do Tiao passa a ser de 2001
# - linhas com picape, setecentos ou IPVA sao regravadas (a pronuncia passa a ser corrigida no gerar.py)
import json, os, re
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
v3 = open(P + "/robo-voz/roteiro-01-v3.txt", encoding="utf-8").read().splitlines()
sec = json.load(open(P + "/robo-voz/roteiro-01-v3-secoes.json"))
f3 = json.load(open(P + "/robo-voz/roteiro-01-v3-fontes.json"))

troca = {
 52: ["E aqui eu quero te pedir uma coisa rápida. Se até aqui essa história está fazendo sentido para você, deixa o seu like.",
      "Porque, agora mesmo, tem alguém do jeito que o Tião estava naquela noite do dia vinte: sentado na mesa da cozinha, com os boletos espalhados na toalha xadrez, a mão na cabeça, sem saber para onde foi o salário.",
      "O seu like ajuda esse vídeo a chegar nessa pessoa."],
 72: ["O Tião disse: \"Dinheiro eu não te empresto. Mas, se quiser, eu te mostro o caderno.\" Era o caderno de capa azul. O mesmo daquela noite na cozinha, quando o salário tinha acabado no dia vinte.",
      "Ali estava cada café, cada taxa, cada assinatura esquecida. Foi nele que o Tião achou o dinheiro que sumia. E era isso que ele estava oferecendo: não dois mil reais, mas o caminho para o Marcos achar o dinheiro dele.",
      "O Marcos deu um riso sem graça, virou as costas e foi embora. A porta bateu."],
 91: "Entregou uma para o Marcos, ficou do lado dele, e, quando o guincho foi embora, disse só uma coisa: \"Aquela oferta do caderno continua de pé. Eu também já estive na mesa da cozinha com a mão na cabeça.\"",
 94: "Saídos de um dinheiro que, lá no começo dessa história, simplesmente sumia antes do dia vinte.",
 95: ["E o Marcos? Dessa vez, ele aceitou. Atravessou a rua, sentou na cozinha do Tião e abriu o caderno de capa azul, página por página.",
     "Seis meses depois, numa terça-feira, a luz da cozinha da casa dele ficou acesa até tarde."],
 101: "O caderno funcionou para o Tião. Mas lembra do estudo da Lally? Um hábito leva uns sessenta e seis dias para pegar, e no papel quase todo mundo desiste antes. Por isso eu uso o Fin Múvi.",
}
PRONUNCIA = re.compile(r"picape|setecentos|IPVA", re.I)

linhas, flags, fontes = [], [], []
for i, t in enumerate(v3):
    novo = troca.get(i, t)
    novo = [x.replace("dois mil e nove", "dois mil e um") for x in (novo if isinstance(novo, list) else [novo])]
    for j, n in enumerate(novo):
        assert "—" not in n and "–" not in n
        # "E aqueles trezentos e oitenta reais por mes?" ganha o contexto de onde vieram
        n = n.replace("E aqueles trezentos e oitenta reais por mês?", "E aqueles trezentos e oitenta reais por mês, que o Tião achou na primeira noite do caderno?")
        linhas.append(n)
        flags.append(sec[i] if j == len(novo) - 1 else False)
        igual = (n == t) and not PRONUNCIA.search(n)
        fontes.append((f3[i] or f"teste-vozes/pedacos-video-01-v3/p{i}.wav") if igual else None)
open(P + "/robo-voz/roteiro-01-v4.txt", "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
json.dump(flags, open(P + "/robo-voz/roteiro-01-v4-secoes.json", "w"))
json.dump(fontes, open(P + "/robo-voz/roteiro-01-v4-fontes.json", "w"))
novos = [i for i, f in enumerate(fontes) if f is None]
w0 = sum(len(x.split()) for x in v3); w = sum(len(x.split()) for x in linhas)
print(len(linhas), "linhas;", len(novos), "para gravar:", json.dumps(novos))
print("palavras", w0, "->", w, "; estimativa", round(1370 / w0 * w / 60, 1), "min")
print("maior linha", max(len(x) for x in linhas))
