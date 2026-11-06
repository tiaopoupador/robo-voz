# Peca do robo: escreve capas/video-NN/YOUTUBE.md (titulo, descricao com capitulos medidos na voz, fontes, creditos, tags, data).
# Uso: python fabrica/descricao.py 02     (depois do montar.py, que mede os tempos e lista as musicas usadas)
import datetime, importlib, json, os, re, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
NN = sys.argv[1]
C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
from fabrica.sincronia import alinhar
md = open(next(f"{P}/roteiros/{f}" for f in os.listdir(P + "/roteiros") if f.startswith(f"{NN}-") and f.endswith(".md") and "pedidos" not in f), encoding="utf-8").read()
secoes = json.load(open(f"{P}/robo-voz/roteiro-{NN}-secoes.json"))
titulos = [t.strip() for t in re.findall(r"^## \d+[a-z]?\.\s*(.+)$", md.split("## Ficha de fontes")[0], re.M)]
ALIN = alinhar(NN); ini = {}
for o in ALIN: ini.setdefault(o[3], o[0])
comeco = [0] + [i + 1 for i, s in enumerate(secoes[:-1]) if s]  # primeira linha de cada secao
caps = []
NOMES = getattr(C, "CAP_NOMES", {})
for t, l in zip(titulos, comeco):
    t = NOMES.get(t, t)
    s = 0 if not caps else int(ini.get(l, 0))
    caps.append(f"{s // 60:02d}:{s % 60:02d} {re.sub(r'^Armadilha (\d): ', r'Armadilha \1: ', t)}")
fontes = []
for linha in md.split("## Ficha de fontes")[1].splitlines():
    c = [x.strip() for x in linha.strip("|").split("|")]
    if len(c) == 2 and not c[1].startswith(("Fonte", "---", "Valores", "Conta própria")) and c[0] != "Dado no roteiro":
        f = re.sub(r"\s*\(\[.*$", "", c[1]); f = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", f)
        if f not in fontes: fontes.append(f)
mont = json.load(open(f"{P}/fabrica/saida/{NN}-montagem.json", encoding="utf-8"))
mus = ", ".join(m.replace("---", " ").replace("-", " ") for m in mont["musicas"])
quando = datetime.datetime.strptime(C.PUBLICA, "%Y-%m-%d %H:%M")
DIA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"][quando.weekday()]
desc = f"""{C.DESC}

📱 O FinMoovi, o app que o Tião usaria hoje: tira foto da notinha do mercado, lê tudo sozinho e mostra para onde foi cada real do mês. Teste 7 dias sem pagar nada:
https://finmoovi.com/?utm_source=youtube&utm_medium=tiao-poupador&utm_campaign=video{NN}

⏱️ Capítulos
""" + "\n".join(caps) + """

📚 Fontes
""" + "\n".join(fontes) + f"""

🎵 Músicas: Kevin MacLeod (incompetech.com), licença CC BY 4.0 (creativecommons.org/licenses/by/4.0): {mus}.
Efeitos sonoros: Kenney (kenney.nl), CC0.

Os personagens e a história são fictícios, para ensinar. Os números e as pesquisas são reais. Isto não é recomendação de investimento.

{C.PERGUNTA} Conta aqui nos comentários.

#dinheiro #educacaofinanceira #financaspessoais"""
for t in ("—", "–"): desc = desc.replace(t, ",")
assert len(desc) < 5000 and len(C.TITULO) <= 100
D = f"{P}/capas/video-{NN}"; os.makedirs(D, exist_ok=True)
open(f"{D}/YOUTUBE.md", "w", encoding="utf-8").write(f"""# Vídeo {NN}: o que vai no YouTube (feito pelo robô)

- **Arquivo do vídeo:** `videos-prontos/VIDEO-{NN}.mp4`
- **Capa:** `capas/video-{NN}/capa.jpg` (1280x720)
- **Quando:** agendar para **{DIA}, {quando:%d/%m/%Y, %H:%M}** (horário de Brasília)

## Título
{C.TITULO}

## Descrição
```
{desc}
```

## Tags
{", ".join(C.TAGS)}

## Outros campos
- Público: não é conteúdo para crianças · Idioma: Português (Brasil) · Categoria: Educação · Promoção paga: não
""")
print("\n".join(caps)); print(len(desc), "letras ->", f"{D}/YOUTUBE.md")
