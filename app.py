"""Servidor local. Abre a interface em http://127.0.0.1:8000"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from bibletrans.chat import responder, SAIDA
RAIZ = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="Tradutor Biblico Assistido")
app.add_middleware(CORSMiddleware, allow_origins=["https://samuelpedroso-dev.github.io", "http://127.0.0.1:8000", "http://localhost:8000"],
                   allow_methods=["*"], allow_headers=["*"])
class Msg(BaseModel):
    msg: str
@app.get("/api/status")
def status():
    return {"ok": True}
@app.post("/api/chat")
def chat(m: Msg):
    texto, arqs = responder(m.msg)
    return {"texto": texto, "arquivos": [os.path.basename(a) for a in arqs]}
@app.get("/api/arquivo/{nome}")
def arquivo(nome: str):
    p = os.path.join(SAIDA, os.path.basename(nome))
    return FileResponse(p) if os.path.exists(p) else JSONResponse({"erro": "nao encontrado"}, 404)
app.mount("/", StaticFiles(directory=os.path.join(RAIZ, "docs"), html=True), name="web")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
