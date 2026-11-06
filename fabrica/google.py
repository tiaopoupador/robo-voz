# Acesso Google do canal (YouTube, Drive, Gmail) com a chave YT_TOKEN. Le as chaves do acessos.env ou do ambiente (nuvem).
import json, os, urllib.parse, urllib.request
P = os.path.dirname(os.path.abspath(__file__)) + "/.."
def chaves():
    env = dict(os.environ)
    if os.path.exists(P + "/acessos.env"):
        env.update(dict(l.strip().split("=", 1) for l in open(P + "/acessos.env", encoding="utf-8") if "=" in l and not l.startswith("#")))
    return env
_tok = {}
def token():
    if "t" not in _tok:
        e = chaves()
        d = urllib.parse.urlencode({"client_id": e["YT_ID"], "client_secret": e["YT_SEGREDO"], "refresh_token": e["YT_TOKEN"], "grant_type": "refresh_token"}).encode()
        _tok["t"] = json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=d)))["access_token"]
    return _tok["t"]
def api(url, dados=None, metodo=None, tipo="application/json; charset=UTF-8", bruto=False):
    h = {"Authorization": "Bearer " + token()}
    if dados is not None:
        if not isinstance(dados, (bytes, bytearray)): dados = json.dumps(dados).encode()
        h["Content-Type"] = tipo
    r = urllib.request.urlopen(urllib.request.Request(url, data=dados, method=metodo or ("POST" if dados is not None else "GET"), headers=h), timeout=300)
    b = r.read()
    return b if bruto else (json.loads(b) if b else {})
