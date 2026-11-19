# Peca do robo: o video em outros idiomas (Ed, 14/11/2026: «pode ir com sua sugestao!»).
# 1) legenda em portugues (do TEXTO DO ROTEIRO, com o tempo da voz) -> fabrica/saida/NN-legenda-pt-BR.srt  (gratis)
# 2) traducao da legenda, do titulo e da descricao para espanhol e ingles (Claude, PAGO: dizer o custo antes) -> NN-legenda-es.srt, NN-legenda-en.srt, NN-idiomas.json
# 3) sobe tudo no YouTube: as 3 legendas e o titulo/descricao em cada idioma (gratis)
# Uso: python fabrica/idiomas.py 02 legenda | traduzir | subir
import json, os, re, sys, uuid
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.sincronia import alinhar
NN, ACAO = sys.argv[1], sys.argv[2]
SAI = f"{P}/fabrica/saida"; IDIOMAS = {"es": "espanhol (América Latina)", "en": "inglês (Estados Unidos)"}
MODELO = "claude-sonnet-5-5"  # o mesmo do posts.py; US$ 2 / US$ 10 por milhao de tokens
# 14/11: no 02 custou US$ 0,47 (o "pensar" do modelo dobrou a saida); effort "low" para traduzir. Esperado: uns US$ 0,25 por video.

def blocos():
    """frases curtas (ate ~12 palavras ou 6 s) com o tempo da fala; o texto e o do roteiro (numeros ja em algarismos)"""
    out, cur = [], []
    for o in alinhar(NN):
        o = list(o); o[2] = re.sub(r"Fin\s*M[óúuo]+vi", "FinMoovi", o[2], flags=re.I).replace("*", "")
        if cur and (o[3] != cur[-1][3]): out.append(cur); cur = []
        cur.append(o)
        if re.search(r"[.!?]\W*$", o[2]) or len(cur) >= 12 or cur[-1][1] - cur[0][0] > 6: out.append(cur); cur = []
    if cur: out.append(cur)
    return [(b[0][0], b[-1][1], " ".join(w[2] for w in b)) for b in out]

def hms(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
def srt(cues, textos): return "\n".join(f"{i + 1}\n{hms(a)} --> {hms(b)}\n{t}\n" for i, ((a, b, _), t) in enumerate(zip(cues, textos)))

def youtube_md():
    md = open(f"{P}/capas/video-{NN}/YOUTUBE.md", encoding="utf-8").read()
    return (re.search(r"## Título[^\n]*\n(.+)", md).group(1).strip(), re.search(r"## Descrição\n```\n(.*?)\n```", md, re.S).group(1).strip())

cues = blocos()
if ACAO == "legenda":
    open(f"{SAI}/{NN}-legenda-pt-BR.srt", "w", encoding="utf-8").write(srt(cues, [c[2] for c in cues]))
    print(len(cues), "legendas;", sum(len(c[2].split()) for c in cues), "palavras")

elif ACAO == "traduzir":
    import anthropic
    from fabrica.google import chaves
    cli = anthropic.Anthropic(api_key=chaves()["CLAUDE_TIAO"]); titulo, desc = youtube_md(); res, custo = {}, 0.0
    ESQ = {"type": "object", "additionalProperties": False, "required": ["titulo", "descricao", "linhas"],
           "properties": {"titulo": {"type": "string"}, "descricao": {"type": "string"}, "linhas": {"type": "array", "items": {"type": "string"}}}}
    for lg, nome in IDIOMAS.items():
        numeradas = "\n".join(f"{i + 1}. {c[2]}" for i, c in enumerate(cues))
        msg = (f"Traduza para {nome} o título, a descrição e as {len(cues)} linhas de legenda de um vídeo do YouTube do canal brasileiro 'Tião Poupador' "
               "(desenho animado sobre dinheiro do dia a dia). Tom natural e falado, frases curtas como numa legenda. Mantenha: os nomes das pessoas "
               "(Tião, Sandra, Marcos), 'FinMoovi', os valores em R$ como estão, os links, as hashtags e as quebras de linha da descrição. "
               "O título até 100 caracteres, com o mesmo mistério do original. Nunca use travessão. "
               f"Devolva exatamente {len(cues)} linhas, na mesma ordem, sem os números.\n\n"
               f"TÍTULO:\n{titulo}\n\nDESCRIÇÃO:\n{desc}\n\nLINHAS:\n{numeradas}")
        with cli.messages.stream(model=MODELO, max_tokens=64000, output_config={"effort": "low", "format": {"type": "json_schema", "schema": ESQ}},
                                 messages=[{"role": "user", "content": msg}]) as s:
            r = s.get_final_message()
        custo += r.usage.input_tokens * 2e-6 + r.usage.output_tokens * 10e-6
        d = json.loads(next(b.text for b in r.content if b.type == "text"))
        if len(d["linhas"]) != len(cues): raise SystemExit(f"{lg}: voltaram {len(d['linhas'])} linhas, esperava {len(cues)}")
        d["linhas"] = [re.sub(r"\s*[\u2013\u2014]\s*", ", ", l) for l in d["linhas"]]  # sem travessao, nunca
        res[lg] = d; open(f"{SAI}/{NN}-legenda-{lg}.srt", "w", encoding="utf-8").write(srt(cues, d["linhas"]))
        print(f"{lg}: ok ({r.usage.input_tokens} entrada, {r.usage.output_tokens} saida) custo ate agora US$ {custo:.3f}")
    json.dump(res, open(f"{SAI}/{NN}-idiomas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"custo total: US$ {custo:.3f}")
    import datetime; open(f"{P}/gastos-claude.csv", "a", encoding="utf-8").write(f"{datetime.date.today()},video {NN} traducao es e en (Sonnet),{custo:.3f}\n")  # o livro dos gastos (CLAUDE.md, regras de custo)

elif ACAO == "subir":
    from fabrica.google import api
    vid = json.load(open(f"{P}/capas/video-{NN}/publicado.json", encoding="utf-8"))["id"]
    res = json.load(open(f"{SAI}/{NN}-idiomas.json", encoding="utf-8"))
    v = api(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,localizations&id={vid}")["items"][0]
    sn = v["snippet"]; sn["defaultLanguage"] = "pt-BR"; sn["defaultAudioLanguage"] = "pt-BR"
    loc = v.get("localizations", {}); loc.update({lg: {"title": d["titulo"][:100], "description": d["descricao"][:5000]} for lg, d in res.items()})
    api("https://www.googleapis.com/youtube/v3/videos?part=snippet,localizations", {"id": vid, "snippet": {k: sn[k] for k in ("title", "description", "categoryId", "tags", "defaultLanguage", "defaultAudioLanguage") if k in sn}, "localizations": loc}, "PUT")
    print("titulo e descricao em", ", ".join(res))
    ja = {c["snippet"]["language"] for c in api(f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={vid}").get("items", [])}
    for lg, nome in [("pt-BR", "Português"), ("es", "Español"), ("en", "English")]:
        if lg in ja: print(lg, "ja tinha"); continue
        meta = json.dumps({"snippet": {"videoId": vid, "language": lg, "name": nome, "isDraft": False}}).encode()
        corpo = open(f"{SAI}/{NN}-legenda-{lg}.srt", "rb").read(); b = uuid.uuid4().hex
        dados = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode() + meta +
                 f"\r\n--{b}\r\nContent-Type: application/x-subrip\r\n\r\n".encode() + corpo + f"\r\n--{b}--".encode())
        api("https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet", dados, "POST", f"multipart/related; boundary={b}")
        print("legenda", lg, "no ar")
