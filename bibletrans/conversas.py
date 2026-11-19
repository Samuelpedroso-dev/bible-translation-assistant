import os, json, time, uuid, threading
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(RAIZ, "dados", "conversas.json"); L = threading.Lock()
def _ler():
    return json.load(open(P, encoding="utf-8")) if os.path.exists(P) else {}
def _gravar(d):
    json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def listar():
    d = _ler()
    r = [dict(id=k, titulo=v["titulo"], fixada=v.get("fixada", False), atualizada=v["atualizada"]) for k, v in d.items()]
    return sorted(r, key=lambda x: -x["atualizada"])
def criar():
    with L:
        d = _ler(); i = uuid.uuid4().hex[:10]
        d[i] = dict(titulo="Nova conversa", fixada=False, atualizada=time.time(), msgs=[]); _gravar(d)
    return i
def obter(i):
    return _ler().get(i)
def adicionar(i, papel, texto, arquivos=None):
    with L:
        d = _ler(); c = d[i]
        c["msgs"].append(dict(papel=papel, texto=texto, arquivos=arquivos or [], quando=time.time()))
        if papel == "user" and c["titulo"] == "Nova conversa":
            c["titulo"] = texto.strip().replace("\n", " ")[:48] or "Nova conversa"
        c["atualizada"] = time.time(); _gravar(d)
def alterar(i, titulo=None, fixada=None):
    with L:
        d = _ler()
        if i not in d: return False
        if titulo is not None: d[i]["titulo"] = titulo.strip()[:80] or d[i]["titulo"]
        if fixada is not None: d[i]["fixada"] = bool(fixada)
        _gravar(d); return True
def excluir(i):
    with L:
        d = _ler(); d.pop(i, None); _gravar(d)
def buscar(q):
    q = q.lower().strip(); out = []
    for k, v in _ler().items():
        trecho = next((m["texto"] for m in v["msgs"] if q in m["texto"].lower()), None)
        if q in v["titulo"].lower() or trecho:
            out.append(dict(id=k, titulo=v["titulo"], trecho=(trecho or "")[:120]))
    return out
