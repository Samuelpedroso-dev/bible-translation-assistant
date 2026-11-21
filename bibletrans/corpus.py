import re, csv, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.environ.get("BIBLE_CORPUS", os.path.join(RAIZ, "dados", "bible-corpus"))
PAT = re.compile(r'<seg id="b\.([A-Z0-9]+)\.(\d+)\.(\d+)"[^>]*>(.*?)</seg>', re.S)
# idiomas do corpus que o NLLB conhece, com o codigo dele
NLLB = {"Dinka-NT": "dik_Latn", "Kabyle-NT": "kab_Latn", "Wolof-NT": "wol_Latn"}
ALIAS = {"dinka": "Dinka-NT", "dik": "Dinka-NT", "kabyle": "Kabyle-NT", "cabila": "Kabyle-NT", "cabila": "Kabyle-NT", "kab": "Kabyle-NT", "wolof": "Wolof-NT", "uolofe": "Wolof-NT", "wol": "Wolof-NT"}
def ler(nome):
    """devolve dict {(livro,cap,ver): texto}"""
    p = os.path.join(CORPUS, "bibles", nome + ".xml")
    t = open(p, encoding="utf-8").read()
    d = {}
    for m in PAT.finditer(t):
        d[(m.group(1), int(m.group(2)), int(m.group(3)))] = re.sub(r"\s+", " ", m.group(4)).strip()
    return d
def livro(d, cod):
    ks = sorted(k for k in d if k[0] == cod)
    return ks
def idiomas():
    p = os.path.join(CORPUS, "metadata.csv")
    if not os.path.exists(p):
        return []
    out = []
    for r in csv.DictReader(open(p, encoding="utf-8")):
        out.append(r)
    return out
def resolver(nome):
    n = nome.strip().lower()
    return ALIAS.get(n)
