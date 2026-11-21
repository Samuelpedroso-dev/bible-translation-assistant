import os, json
from . import estado, traduzir as T
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def registro():
    return json.load(open(os.path.join(RAIZ, "modelos.json"), encoding="utf-8"))
def listar():
    ap = estado.ler()["aprovados"]; out = []
    for m in registro():
        pasta = T.pasta_modelo(m["codigo"]); inst = os.path.exists(os.path.join(pasta, "model.bin"))
        rel = T.relatorio(m["codigo"]) or {}
        st = "aprovado" if inst and m["idioma"] in ap else ("instalado" if inst else "nao_treinado")
        out.append(dict(m, status=st, chrf=rel.get("chrf_depois") or m.get("chrf_depois")))
    return out
def achar(id_):
    return next((m for m in listar() if m["id"] == id_), None)
