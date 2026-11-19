"""Servidor local. Abre a interface em http://127.0.0.1:8000"""
import os, time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from bibletrans import conversas, modelos, diario, estado, corpus
from bibletrans.chat import responder, SAIDA
RAIZ = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="Tradutor Biblico Assistido")
app.add_middleware(CORSMiddleware, allow_origins=["https://samuelpedroso-dev.github.io", "http://127.0.0.1:8000", "http://localhost:8000"],
                   allow_methods=["*"], allow_headers=["*"])
class Msg(BaseModel):
    conversa: str
    msg: str
    modelo: Optional[str] = None
    feixes: int = 4
class Alt(BaseModel):
    titulo: Optional[str] = None
    fixada: Optional[bool] = None
@app.get("/api/status")
def status():
    return {"ok": True}
@app.get("/api/conversas")
def c_listar():
    return conversas.listar()
@app.post("/api/conversas")
def c_criar():
    return {"id": conversas.criar()}
@app.get("/api/conversas/{i}")
def c_obter(i: str):
    c = conversas.obter(i)
    if not c: raise HTTPException(404)
    return c
@app.patch("/api/conversas/{i}")
def c_alterar(i: str, a: Alt):
    if not conversas.alterar(i, a.titulo, a.fixada): raise HTTPException(404)
    return {"ok": True}
@app.delete("/api/conversas/{i}")
def c_excluir(i: str):
    conversas.excluir(i); return {"ok": True}
@app.get("/api/busca")
def busca(q: str):
    return conversas.buscar(q) if q.strip() else []
@app.post("/api/chat")
def chat(m: Msg):
    if not conversas.obter(m.conversa): raise HTTPException(404)
    conversas.adicionar(m.conversa, "user", m.msg)
    try:
        texto, arqs = responder(m.msg, m.modelo, m.feixes)
    except Exception as e:
        texto, arqs = "Erro ao processar. %s" % e, []
    nomes = [os.path.basename(a) for a in arqs]
    conversas.adicionar(m.conversa, "assistant", texto, nomes)
    return {"texto": texto, "arquivos": nomes}
@app.get("/api/modelos")
def api_modelos():
    return modelos.listar()
@app.get("/api/idiomas")
def idiomas():
    ap = estado.ler()["aprovados"]; out = []
    for k, cod in corpus.NLLB.items():
        try: n = len(corpus.ler(k))
        except Exception: n = 0
        out.append(dict(idioma=k, codigo=cod, versiculos=n, aprovado=k in ap))
    return out
@app.get("/api/arquivos")
def arquivos():
    out = []
    if os.path.isdir(SAIDA):
        for n in sorted(os.listdir(SAIDA)):
            p = os.path.join(SAIDA, n)
            if os.path.isfile(p) and not n.startswith("."):
                out.append(dict(nome=n, tamanho=os.path.getsize(p), quando=os.path.getmtime(p)))
    return sorted(out, key=lambda x: -x["quando"])
@app.get("/api/arquivo/{nome}")
def arquivo(nome: str):
    p = os.path.join(SAIDA, os.path.basename(nome))
    if not os.path.exists(p): raise HTTPException(404)
    return FileResponse(p)
@app.get("/api/diario")
def api_diario():
    return diario.ler()[-200:][::-1]
app.mount("/", StaticFiles(directory=os.path.join(RAIZ, "docs"), html=True), name="web")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
