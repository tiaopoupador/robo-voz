# Revisor de CENAS (Ed, 08/11/2026: «o audio diz que ela esta parada (...) mas a cena mostra a Sandra andando»,
# «fala que a Sandra pega um chocolate, mas a imagem nao e a Sandra», «a mao esquerda do Marcos esta deformada»).
# Depois de montar: para CADA imagem e clipe do video (do robo, do Ed e do banco), o Claude ve a imagem junto com a frase
# que toca enquanto ela esta na tela e reprova o que nao bate (pessoa errada, acao errada, quantidade, mao ou rosto
# deformado, letras inventadas). Guarda o que ja viu (fabrica/videos/vNN/cenas-revistas.json): so paga o que mudou.
# Custo: uns US$ 0,004 por cena nova (credito de revisor). Uso: python fabrica/revisor_cenas.py 02
import hashlib, json, os, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
import importlib
from fabrica.revisor_imagens import revisar
from fabrica.rostos import _jpg

def refs_de(q):
    if not q: return []
    s = str(q[1]).lower(); out = [c for c in q[1] if c in "TRN"] if len(str(q[1])) <= 3 else []
    for nome, l in (("tiao", "T"), ("sandra", "R"), ("marcos", "N")):
        if nome in s and l not in out: out.append(l)
    return out

def main(NN):
    C = importlib.import_module(f"fabrica.videos.v{NN}.cenas")
    props = json.load(open(f"{P}/render/public/v{NN}/props.json", encoding="utf-8"))
    from fabrica.sincronia import alinhar
    ALIN = alinhar(NN)
    cad_f = f"{P}/fabrica/videos/v{NN}/cenas-revistas.json"
    cad = json.load(open(cad_f, encoding="utf-8")) if os.path.exists(cad_f) else {}
    cenas = props["cenas"]; ruins, custo = [], 0.0
    for i, c in enumerate(cenas):
        if c["k"] not in ("img", "hib", "vid") or not c.get("src"): continue
        fim = cenas[i + 1]["ini"] if i + 1 < len(cenas) else c["ini"] + 5
        fala = " ".join(o[2] for o in ALIN if c["ini"] - 0.2 <= o[0] < fim)
        k, j = (int(x) for x in c["chave"].split("-"))
        cont = C.L[k][j][2]; nome = cont[0] if isinstance(cont, tuple) else cont
        if isinstance(nome, str) and nome.startswith("banco:FM:"): continue  # tela real do app: as letras sao do app mesmo
        q = C.IMG.get(nome) if isinstance(nome, str) else None
        pedido = (C.PEDIDO.get(nome) if q and q[0] in ("meta", "flow") else (q[2] if q else "")) or ""
        arq = f"{P}/render/public/{c['src']}"
        chave = hashlib.md5(f"{os.path.basename(arq)}|{os.path.getsize(arq)}|{fala}".encode()).hexdigest()
        if chave in cad: v = cad[chave]
        else:
            tmp = f"{P}/fabrica/saida/_cena.jpg"; open(tmp, "wb").write(_jpg(arq))
            try: ok, prob, cu = revisar(tmp, refs_de(q), pedido or "uma cena que mostre o que a narração diz", fala); custo += cu
            except Exception as e: print("revisor falhou nesta cena:", c["chave"], repr(e)[:120], flush=True); continue
            v = cad[chave] = {"cena": c["chave"], "arquivo": os.path.basename(arq), "passa": ok, "problemas": prob}
            json.dump(cad, open(cad_f, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        if not v["passa"]:
            ruins.append({"cena": c["chave"], "tempo": f"{int(c['ini'] // 60)}:{int(c['ini'] % 60):02d}", "imagem": nome, "fala": fala[:160], "problemas": v["problemas"]})
            print(f"RUIM {c['chave']} {ruins[-1]['tempo']} {nome}: {'; '.join(v['problemas'])[:200]}", flush=True)
    json.dump(ruins, open(f"{P}/fabrica/saida/{NN}-cenas-ruins.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"cenas com problema: {len(ruins)} · custo agora: US$ {custo:.3f}")
    return ruins

if __name__ == "__main__": main(sys.argv[1])
