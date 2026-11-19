"""Pesquisa na web sem chave de API, via DuckDuckGo. Devolve titulo, link e resumo."""
def buscar(tema, n=6):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as d:
            return [(r["title"], r["href"], r["body"]) for r in d.text(tema, max_results=n)]
    except Exception as e:
        return [("Falha na pesquisa", "", str(e))]
