"""Interpretador de comandos do chat. Regras simples, sem chave de API."""
import os, re, json
from . import corpus, colab, diario, estado, pesquisa, modelos, traduzir as T, diagramar
from .livros import achar, nome, NT
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "saida")
AJUDA = """Comandos
ajuda
idiomas
preparar dinka (ou kabyle)
treinar dinka (gera o caderno do Colab)
importar modelo dinka (depois de treinar, descompacte em modelos/dik_Latn)
aprovar dinka (libera a tradução, só depois de ver os resultados)
traduzir Rute para dinka (livro do Antigo Testamento, fonte inglesa WEB em domínio público)
traduzir texto dinka: In the beginning...
pesquisar <tema>
navegar <url> (abre um navegador real e lê a página, precisa de playwright)
relatorio"""
def _lingua(msg):
    for w in re.findall(r"[a-zA-Zçã]+", msg.lower()):
        r = corpus.resolver(w)
        if r:
            return r
    return None
def responder(msg, modelo=None, feixes=4):
    """devolve (texto, lista de arquivos). modelo e o id do modelo escolhido na interface"""
    m = msg.strip(); l = m.lower()
    mod = modelos.achar(modelo) if modelo else None
    if l in ("ajuda", "help", "oi", "olá", "ola"):
        return AJUDA, []
    if l.startswith("idiomas"):
        return "Idiomas prontos para treino\n" + "\n".join("%s  (%s)" % (k, v) for k, v in corpus.NLLB.items()), []
    if l.startswith("pesquisar"):
        tema = m[9:].strip()
        r = pesquisa.buscar(tema); diario.log("pesquisa", tema=tema)
        return "\n\n".join("%s\n%s\n%s" % x for x in r), []
    if l.startswith("navegar"):
        try:
            from . import agente
            url = m[7:].strip()
            n = agente.Navegador(visivel=False); t = n.ir(url); txt = n.ler(1500); n.fechar()
            diario.log("navegar", url=url)
            return "%s\n\n%s" % (t, txt), []
        except Exception as e:
            return "Navegador indisponível. Instale com pip install playwright e playwright install chromium. Detalhe %s" % e, []
    if l.startswith("relat"):
        p = diario.relatorio_md()
        return "Relatório gerado.", [p]
    c = _lingua(l) or (mod["idioma"] if mod else None)
    if l.startswith("preparar"):
        if not c: return "Diga o idioma, por exemplo preparar dinka.", []
        d = corpus.ler(c); en = corpus.ler("English-WEB")
        n = sum(1 for k in d if k in en)
        diario.log("preparar", idioma=c, versiculos=len(d), pares_com_ingles=n)
        return "%s tem %d versículos, %d alinhados com o inglês WEB. Próximo passo treinar %s." % (c, len(d), n, l.split()[-1]), []
    if l.startswith("treinar"):
        if not c: return "Diga o idioma.", []
        p = colab.gerar(c, corpus.NLLB[c], os.path.join(SAIDA, "treino_%s.ipynb" % corpus.NLLB[c]))
        diario.log("caderno_gerado", idioma=c)
        return "Caderno gerado. Abra no Colab, escolha GPU T4 e execute tudo. Baixe o zip no fim e descompacte em modelos/%s." % corpus.NLLB[c], [p]
    if l.startswith("importar"):
        if not c: return "Diga o idioma.", []
        r = T.relatorio(corpus.NLLB[c])
        if not r: return "Modelo não encontrado em modelos/%s." % corpus.NLLB[c], []
        diario.log("modelo_importado", **r)
        return "Modelo encontrado. chrF++ antes %.1f, depois %.1f. Veja os resultados e então digite aprovar." % (r["chrf_antes"], r["chrf_depois"]), []
    if l.startswith("aprovar"):
        if not c: return "Diga o idioma.", []
        e = estado.ler()
        if c not in e["aprovados"]: e["aprovados"].append(c)
        estado.salvar(e); diario.log("aprovado", idioma=c)
        return "Aprovado para rascunho. Lembrete: nada sai como final sem validação de falantes nativos.", []
    if l.startswith("traduzir"):
        if not c: return "Diga o idioma de destino.", []
        if c not in estado.ler()["aprovados"]: return "Esse idioma ainda não foi aprovado. Treine, confira e digite aprovar.", []
        cod = corpus.NLLB[c]
        if l.startswith("traduzir texto"):
            txt = m.split(":", 1)[-1].strip()
            return T.traduzir(cod, [txt], feixes=feixes)[0], []
        alvo = None
        for tok in re.findall(r"[\wçãéíóúêô]+(?: \d)?", m[8:]):
            alvo = achar(tok) or alvo
        if not alvo:
            mm = re.match(r"traduzir\s+(.+?)\s+para\b", m, re.I); alvo = achar(mm.group(1)) if mm else None
        if not alvo: return "Não reconheci o livro.", []
        if alvo in NT: return "Esse livro do Novo Testamento já existe no idioma. Peça um livro do Antigo Testamento.", []
        en = corpus.ler("English-WEB"); ks = sorted(k for k in en if k[0] == alvo)
        out = T.traduzir(cod, [en[k] for k in ks], feixes=feixes)
        d = dict(zip(ks, out))
        tsv = os.path.join(SAIDA, "rascunho_%s_%s.tsv" % (alvo, cod))
        open(tsv, "w", encoding="utf-8").write("\n".join("%s.%d.%d\t%s\t%s" % (k[0], k[1], k[2], en[k], d[k]) for k in ks))
        pdf = diagramar.pdf(os.path.join(SAIDA, "%s_%s.pdf" % (alvo, cod)), alvo, c, en, d, "English (WEB)", c.split("-")[0])
        diario.log("rascunho", livro=alvo, idioma=c, versiculos=len(ks))
        return "Rascunho de %s pronto, %d versículos. Envie aos revisores nativos." % (nome(alvo), len(ks)), [pdf, tsv]
    if mod:
        if mod["status"] == "nao_treinado":
            return "O modelo %s ainda não foi treinado. Digite treinar para gerar o caderno do Colab." % mod["nome"], []
        if mod["status"] != "aprovado":
            return "O modelo %s está instalado mas ainda não foi aprovado. Confira os números e digite aprovar." % mod["nome"], []
        return T.traduzir(mod["codigo"], [m], feixes=feixes)[0], []
    return "Não entendi. Digite ajuda ou escolha um modelo para traduzir texto livre.", []
