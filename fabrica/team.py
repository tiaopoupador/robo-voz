# Peca do robo: a porta dos robos do Apexi Team (manual: GOAPEXI/docs/impl/porta-dos-robos-manual.md).
# As tarefas "o que gerar a mao" vao para o Team; o Ed anexa la o que gerou; o robo baixa e deixa o recado no fim.
# A chave e APEXI_TEAM_CHAVE (acessos.env no PC, segredo do GitHub na nuvem). Nunca se imprime.
# Uso: python fabrica/team.py ver NN | baixar NN | recado NN "texto" [fechar] | recados chave1 [chave2 ...]
import json, os, sys, urllib.error, urllib.request
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import chaves
BASE = "https://api.goapexi.com/v1/team/robo"
# 28/11 (Ed: «exclua aquele do team e coloque um novo atual com as devidas correcoes»): a API nao apaga tarefa; a velha fecha-se
# com um recado e a nova nasce com outra chave (o sufixo daqui). Todo o resto (baixar, recados) ja usa a chave nova.
SUFIXO = {"06": "-r2"}
def chave_unica(NN): return f"tiao-v{NN}-imagens" + SUFIXO.get(f"{int(NN):02d}", "")

def _pedir(caminho, dados=None, bruto=False):
    k = chaves().get("APEXI_TEAM_CHAVE")
    if not k: raise RuntimeError("sem a chave APEXI_TEAM_CHAVE")
    h = {"Authorization": "Bearer " + k, "User-Agent": "robo-tiao-poupador"}
    if dados is not None: h["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + caminho, data=None if dados is None else json.dumps(dados).encode(), headers=h,
                                 method="POST" if dados is not None else "GET")
    b = urllib.request.urlopen(req, timeout=120).read()
    return b if bruto else (json.loads(b) if b else {})

def ver(NN):
    """a tarefa do video, ou None se ainda nao existe"""
    try: return _pedir(f"/tarefas/{chave_unica(NN)}")
    except urllib.error.HTTPError as e:
        if e.code == 404: return None
        raise

# ---- REGRA DE TODA TAREFA MANUAL (Ed, 19/11/2026: «essas tarefas sao manuais e preciso da sua maxima ajuda pra me
# facilitar ao maximo tudo!» · «vc nao esta com visao de um diretor chato (...) tem muita informacao repetida»).
# Cada coisa aparece UMA vez so, no passo:
#   1. o formato (16:9, 9:16, 1:1) vai DENTRO do prompt: o meta.ai e os outros nao tem onde escolher;
#   2. a ficha (e todo link de referencia) e um link que ABRE numa aba nova (Ed: «quero que ja abra a ficha direto»);
#   3. a pasta onde salvar e uma caixa «📁 Salvar nessa pasta» com o CAMINHO no PC (G:\Meu Drive\...), nunca http;
#   4. o botao do prompt chama-se so «Prompt». O passo a passo fica uma vez, na descricao da tarefa.
#   5. o TITULO do passo no molde B (Ed, 19/11: «B»): «7 de 18 · 🖼️ Imagem no meta.ai · Tiao acenando tchau · 📱 em pe».
#      Sai sozinho quando o passo traz tipo ("imagem", "video", "gif"), onde ("meta.ai", "Flow") e o_que.
# Campos nossos (nao vao ao Team): passo["formato"], passo["pasta"], passo["tipo"], passo["onde"], passo["o_que"]
# e tarefa["pasta"] = {"rotulo", "url"}.
FORMATOS = {"16:9": "ASPECT RATIO 16:9, horizontal widescreen image (1920x1080), never square, never vertical. ",
            "9:16": "ASPECT RATIO 9:16, vertical portrait image (1080x1920), never square, never horizontal. ",
            "1:1": "ASPECT RATIO 1:1, square image (1080x1080), never vertical, never horizontal. "}
def _formato(p):
    if p.get("formato"): return p["formato"]
    for f in FORMATOS:
        if f in p.get("texto", ""): return f
# REFERENCIAS FIXAS (Ed, 19/11: «sempre que for referencias ao tiao pra ficar com mais consistencia eu uso essa:
# tiao-ficha-oficial e essa: tiao-frente-sozinho (...) Pro Marcos essas duas: marcos-neutro, marcos-referencia»).
# Ed, 19/11 (mais tarde): «tiao-frente-sozinho.jpg nao precisa mais anexar essa! Sempre que for fazer referencia ao TIAO
# colocar somente a tiao-ficha-oficial». O Marcos segue com as duas.
REFERENCIAS = {"tiao": ["tiao-ficha-oficial.jpg"],
               "marcos": ["marcos-neutro.jpg", "marcos-referencia.jpg"]}
TROCA = {"tiao-frente-sozinho.jpg": "tiao-ficha-oficial.jpg"}  # cenas antigas que ainda pedem a outra foto do Tiao
SEM_REFS = "Não é preciso anexar imagem de referência nenhuma!"  # Ed, 19/11: «tem que informar quando nao tem nada pra anexar»
def completar_refs(nomes):
    """nomes de arquivos de referencia -> a mesma lista com as de cada personagem fixo (sem repetir, sem nome vazio)"""
    out = []
    for n in [TROCA.get(x.strip(), x.strip()) for x in nomes if x and x.strip()]:
        for par in REFERENCIAS.values():
            if n in par: out += [x for x in par if x not in out]; break
        else:
            if n not in out: out.append(n)
    return out
def caminho(pasta):
    """a pasta como o Ed a ve no PC (Google Drive para computador, disco G:), nunca o link http (Ed, 19/11:
    «nao dve ser um http, tem q ser o caminho da pasta, tipo assim: G:/Meu Drive/Tiao Poupador/banco/poses/tiao (com barras invertidas)»)"""
    if pasta.get("caminho"): return pasta["caminho"]
    r = pasta.get("rotulo", "")
    if r.startswith("Google Drive > "): return "G:\\Meu Drive\\" + "\\".join(x.strip() for x in r.split(">")[1:])
    return pasta["url"]
TIPOS = {"imagem": "🖼️ Imagem", "video": "🎬 Vídeo", "gif": "🎞️ GIF animado"}
JEITO = {"9:16": "📱 em pé", "16:9": "🖥️ deitado", "1:1": "⬜ quadrado"}
def mastigar(tarefa):
    t = dict(tarefa); pasta_geral = t.pop("pasta", None); avisos = []
    passos = []; total = len(t.get("passos", []))
    for n, p in enumerate(t.get("passos", []), 1):
        p = dict(p); fmt = _formato(p); p.pop("formato", None); pasta = p.pop("pasta", None) or pasta_geral
        tipo, onde, o_que = p.pop("tipo", None), p.pop("onde", None), p.pop("o_que", None)
        if tipo and onde and o_que:
            p["texto"] = f"{n} de {total} · {TIPOS.get(tipo, tipo)} no {onde} · {o_que}" + (f" · {JEITO[fmt]}" if fmt in JEITO else "")
        cop = p.pop("copias", None) or ([{"rotulo": "Prompt", "texto": p["copiar"]}] if p.get("copiar") else [])
        p.pop("copiar", None)
        if fmt in FORMATOS:  # o formato dentro do prompt
            for c in cop:
                if ("prompt" in c["rotulo"].lower() or "pedido" in c["rotulo"].lower()) and "ASPECT RATIO" not in c["texto"].upper():
                    c["texto"] = FORMATOS[fmt] + c["texto"]
        p["links"] = [l for l in p.get("links", []) if (l.get("rotulo") or "").rstrip(" -").split(" - ")[-1].strip() not in ("", "Anexar junto ao Prompt")]
        if tipo in ("imagem", "video", "gif") and not p["links"] and cop:  # nada para anexar: diz-se com todas as letras
            cop.insert(0, {"rotulo": "📎 Referências", "texto": SEM_REFS})
        if p.pop("varios", False) or p.get("ficheiro"):  # varios: um passo que salva varios arquivos (2 imagens + GIF)
            if pasta:
                cop.append({"rotulo": "📁 Salvar nessa pasta", "texto": caminho(pasta)})
                p["links"] = [l for l in p.get("links", []) if l.get("url") != pasta["url"]]
            else: avisos.append(p.get("codigo", "?"))
        if cop: p["copias"] = cop[:10]
        passos.append(p)
    if passos: t["passos"] = passos
    if avisos: print(f"⚠️ Team: {len(avisos)} passos com arquivo e SEM pasta onde salvar ({', '.join(avisos[:5])}...). Ponha passo['pasta'] ou tarefa['pasta'].")
    return t

def mandar(tarefa):
    return _pedir("/tarefas", mastigar(tarefa))

def baixar(NN, sai=None):
    """baixa os anexos que o Ed pos no Team para fabrica/videos/vNN/entrada (antes de olhar o Drive)"""
    sai = sai or f"{P}/fabrica/videos/v{NN}/entrada"; os.makedirs(sai, exist_ok=True)
    anexos = []
    for ch in (chave_unica(NN), chave_unica(NN) + "-extras", chave_unica(NN) + "-refazer", f"tiao-v{NN}-capas"):  # a tarefa do video, a dos extras e a das refeitas
        try: t = _pedir(f"/tarefas/{ch}")
        except urllib.error.HTTPError as e:
            if e.code != 404: print("Team:", ch, e.code)
            continue
        except Exception as e: print("Team fora do ar agora:", e); return 0
        anexos += t.get("anexos", [])
    n = 0
    for a in anexos:
        nome = os.path.basename(a.get("nome") or f"{a.get('codigo', 'anexo')}-{a['id']}")
        if a.get("codigo") and not nome.upper().startswith(a["codigo"].split("-")[0].upper()): nome = f"{a['codigo']}_{nome}"  # o montador acha pelo codigo
        dst = f"{sai}/{nome}"
        if os.path.exists(dst): continue
        open(dst, "wb").write(_pedir(f"/anexos/{a['id']}", bruto=True)); n += 1
    print(f"Team: {n} anexos baixados ({len(anexos)} nas tarefas)"); return n

def recados(chaves_unicas):
    """o que o Ed escreveu nas tarefas anteriores: a nota de cada passo e a conversa (sem as mensagens do robo).
    Manual secao 3 (Ed, 13/11): ler SEMPRE antes da tarefa seguinte e seguir o que la estiver."""
    out = []
    for ch in chaves_unicas:
        try: t = _pedir(f"/tarefas/{ch}")
        except urllib.error.HTTPError as e:
            if e.code != 404: print("Team:", ch, e.code)
            continue
        except Exception as e: print("Team fora do ar agora:", e); break
        for p in t.get("passos", []):
            if (p.get("nota") or "").strip(): out.append(f"[{ch} · passo {p.get('codigo')}] {p['nota'].strip()}")
        for c in t.get("conversa", []):
            tx = (c.get("texto") or "").strip()
            if tx and not tx.startswith("🤖"):
                an = [a.get("nome") for a in c.get("anexos", []) if a.get("nome")]
                out.append(f"[{ch} · conversa {(c.get('em') or '')[:10]}] {tx}" + (f" (anexou: {', '.join(an)})" if an else ""))
    return out

def recado(NN, texto, fechar=False):
    try: return _pedir(f"/tarefas/{chave_unica(NN)}/recado", {"texto": texto, "fechar": fechar})
    except Exception as e: print("recado no Team falhou:", e)

if __name__ == "__main__":
    acao, NN = sys.argv[1], sys.argv[2]
    if acao == "ver":
        t = ver(NN)
        if not t: print("sem tarefa"); sys.exit()
        print(json.dumps({k: v for k, v in t.items() if k != "passos"}, ensure_ascii=False)[:600])
        for p in t.get("passos", []): print(" ", p.get("codigo"), "feito" if p.get("feito") else "-")
    elif acao == "baixar": baixar(NN)
    elif acao == "recados":  # python fabrica/team.py recados chave1 [chave2 ...]
        for r in recados(sys.argv[2:]) or ["(nenhum recado do Ed)"]: print(r)
    elif acao == "recado": print(recado(NN, sys.argv[3], len(sys.argv) > 4 and sys.argv[4] == "fechar"))
