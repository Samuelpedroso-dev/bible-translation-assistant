import os, json
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(RAIZ, "dados", "estado.json")
def ler():
    return json.load(open(P)) if os.path.exists(P) else {"aprovados": []}
def salvar(e):
    json.dump(e, open(P, "w"), indent=1)
