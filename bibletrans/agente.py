"""Camada de agente. O NLLB so traduz, entao o 'mouse' e a pesquisa ficam aqui.
Navegador real controlado por Playwright (gratuito, local). O planejamento pode usar
um LLM local pequeno via Ollama. Sem Ollama, usa so comandos diretos."""
import os, json, urllib.request
OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODELO = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")
class Navegador:
    def __init__(self, visivel=True):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self.b = self._pw.chromium.launch(headless=not visivel)
        self.p = self.b.new_page()
    def ir(self, url):
        self.p.goto(url, wait_until="domcontentloaded", timeout=30000)
        return self.p.title()
    def ler(self, limite=4000):
        return self.p.inner_text("body")[:limite]
    def links(self, n=20):
        return [(a.inner_text().strip()[:60], a.get_attribute("href")) for a in self.p.query_selector_all("a")[:n]]
    def clicar(self, seletor):
        self.p.click(seletor, timeout=8000)
    def digitar(self, seletor, texto):
        self.p.fill(seletor, texto)
    def foto(self, caminho):
        self.p.screenshot(path=caminho); return caminho
    def fechar(self):
        self.b.close(); self._pw.stop()
def perguntar_llm(prompt):
    """LLM local opcional. Devolve texto ou None se o Ollama nao estiver rodando."""
    try:
        req = urllib.request.Request(OLLAMA + "/api/generate", json.dumps({"model": MODELO, "prompt": prompt, "stream": False}).encode(), {"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=120).read())["response"]
    except Exception:
        return None
def planejar(objetivo, pagina):
    """Pede ao LLM local o proximo passo em JSON. Acoes ir, clicar, digitar, ler, fim."""
    p = "Objetivo %s\nPagina atual\n%s\nResponda so JSON com acao e argumentos." % (objetivo, pagina[:1500])
    r = perguntar_llm(p)
    try:
        return json.loads(r[r.index("{"):r.rindex("}") + 1])
    except Exception:
        return {"acao": "fim"}
def executar(objetivo, url_inicial, max_passos=6, visivel=True):
    from . import diario
    n = Navegador(visivel); log = []
    try:
        log.append("abriu " + n.ir(url_inicial))
        for _ in range(max_passos):
            a = planejar(objetivo, n.ler())
            diario.log("agente_passo", acao=json.dumps(a, ensure_ascii=False))
            if a.get("acao") == "fim": break
            if a["acao"] == "ir": n.ir(a["url"])
            elif a["acao"] == "clicar": n.clicar(a["seletor"])
            elif a["acao"] == "digitar": n.digitar(a["seletor"], a["texto"])
            log.append(str(a))
        return log, n.ler()
    finally:
        n.fechar()
