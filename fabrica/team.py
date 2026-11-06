# Peca do robo: a porta dos robos do Apexi Team (manual: GOAPEXI/docs/impl/porta-dos-robos-manual.md).
# As tarefas "o que gerar a mao" vao para o Team; o Ed anexa la o que gerou; o robo baixa e deixa o recado no fim.
# A chave e APEXI_TEAM_CHAVE (acessos.env no PC, segredo do GitHub na nuvem). Nunca se imprime.
# Uso: python fabrica/team.py ver NN | baixar NN | recado NN "texto" [fechar]
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
    for ch in (chave_unica(NN), chave_unica(NN) + "-extras"):  # a tarefa do video e a dos pedidos extras
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
    elif acao == "recado": print(recado(NN, sys.argv[3], len(sys.argv) > 4 and sys.argv[4] == "fechar"))
