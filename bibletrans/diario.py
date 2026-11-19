"""Diario automatico em JSONL e relatorio em markdown para documentar e postar."""
import os, json, datetime
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(RAIZ, "dados")
def log(evento, **kw):
    kw.update(evento=evento, quando=datetime.datetime.now().isoformat(timespec="seconds"))
    open(os.path.join(D, "diario.jsonl"), "a", encoding="utf-8").write(json.dumps(kw, ensure_ascii=False) + "\n")
def ler():
    p = os.path.join(D, "diario.jsonl")
    return [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.exists(p) else []
def relatorio_md():
    linhas = ["# Diário do projeto", ""]
    for e in ler():
        ev = e.pop("evento"); q = e.pop("quando")
        linhas.append("## %s  %s" % (q, ev))
        for k, v in e.items():
            linhas.append("- %s %s" % (k, v))
        linhas.append("")
    p = os.path.join(RAIZ, "saida", "relatorio.md")
    open(p, "w", encoding="utf-8").write("\n".join(linhas))
    return p
