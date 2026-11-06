# A agenda do canal (videos em producao e o calendario dos temas). A verdade mora no Drive (Tiao Poupador/robo/agenda.json),
# para os robos da nuvem poderem escrever nela; fabrica/agenda.json e a copia local.
# Uso: python fabrica/agenda.py em_producao   -> "02 03"   |   python fabrica/agenda.py mostrar
import json, os, sys
P = os.path.dirname(os.path.abspath(__file__)) + "/.."; sys.path.insert(0, P)
LOCAL = f"{P}/fabrica/agenda.json"
def _pasta():
    from fabrica import drive
    return drive.pasta("robo", drive.pasta("Tiao Poupador"))
def ler():
    try:
        from fabrica import drive
        from fabrica.drive import D, api
        for f in drive.listar(_pasta()):
            if f["name"] == "agenda.json": return json.loads(api(f"{D}/{f['id']}?alt=media", bruto=True))
    except Exception as e: print("agenda: Drive fora, uso a copia local:", e, file=sys.stderr)
    return json.load(open(LOCAL, encoding="utf-8"))
def gravar(a):
    json.dump(a, open(LOCAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from fabrica import drive
    from fabrica.drive import D, api
    pai = _pasta()
    for f in drive.listar(pai):
        if f["name"] == "agenda.json": api(f"{D}/{f['id']}", metodo="DELETE", bruto=True)
    drive.subir(LOCAL, pai)
if __name__ == "__main__":
    a = ler()
    if sys.argv[1:] == ["em_producao"]: print(" ".join(a.get("em_producao", [])))
    elif sys.argv[1:] == ["subir"]: gravar(json.load(open(LOCAL, encoding="utf-8"))); print("agenda no Drive")
    else: print(json.dumps(a, ensure_ascii=False, indent=1))
