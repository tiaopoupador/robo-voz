# Peca do robo: a porta dos robos do Apexi Team (manual: GOAPEXI/docs/impl/porta-dos-robos-manual.md).
# As tarefas "o que gerar a mao" vao para o Team; o Ed anexa la o que gerou; o robo baixa e deixa o recado no fim.
# A chave e APEXI_TEAM_CHAVE (acessos.env no PC, segredo do GitHub na nuvem). Nunca se imprime.
# Uso: python fabrica/team.py ver NN | baixar NN | recado NN "texto" [fechar] | recados chave1 [chave2 ...]
import json, os, sys, urllib.error, urllib.request
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
from fabrica.google import chaves
BASE = "https://api.goapexi.com/v1/team/robo"
def chave_unica(NN): return f"tiao-v{NN}-imagens"

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

def mandar(tarefa):
    return _pedir("/tarefas", tarefa)

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
