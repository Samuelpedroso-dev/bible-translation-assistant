# codigo do corpus, nome em portugues, nome em ingles
LIVROS = [
("GEN","Gênesis","Genesis"),("EXO","Êxodo","Exodus"),("LEV","Levítico","Leviticus"),("NUM","Números","Numbers"),
("DEU","Deuteronômio","Deuteronomy"),("JOS","Josué","Joshua"),("JDG","Juízes","Judges"),("RUT","Rute","Ruth"),
("1SA","1 Samuel","1 Samuel"),("2SA","2 Samuel","2 Samuel"),("1KI","1 Reis","1 Kings"),("2KI","2 Reis","2 Kings"),
("1CH","1 Crônicas","1 Chronicles"),("2CH","2 Crônicas","2 Chronicles"),("EZR","Esdras","Ezra"),("NEH","Neemias","Nehemiah"),
("EST","Ester","Esther"),("JOB","Jó","Job"),("PSA","Salmos","Psalms"),("PRO","Provérbios","Proverbs"),
("ECC","Eclesiastes","Ecclesiastes"),("SON","Cantares","Song of Solomon"),("ISA","Isaías","Isaiah"),("JER","Jeremias","Jeremiah"),
("LAM","Lamentações","Lamentations"),("EZE","Ezequiel","Ezekiel"),("DAN","Daniel","Daniel"),("HOS","Oseias","Hosea"),
("JOE","Joel","Joel"),("AMO","Amós","Amos"),("OBA","Obadias","Obadiah"),("JON","Jonas","Jonah"),
("MIC","Miqueias","Micah"),("NAH","Naum","Nahum"),("HAB","Habacuque","Habakkuk"),("ZEP","Sofonias","Zephaniah"),
("HAG","Ageu","Haggai"),("ZEC","Zacarias","Zechariah"),("MAL","Malaquias","Malachi"),
("MAT","Mateus","Matthew"),("MAR","Marcos","Mark"),("LUK","Lucas","Luke"),("JOH","João","John"),
("ACT","Atos","Acts"),("ROM","Romanos","Romans"),("1CO","1 Coríntios","1 Corinthians"),("2CO","2 Coríntios","2 Corinthians"),
("GAL","Gálatas","Galatians"),("EPH","Efésios","Ephesians"),("PHI","Filipenses","Philippians"),("COL","Colossenses","Colossians"),
("1TH","1 Tessalonicenses","1 Thessalonians"),("2TH","2 Tessalonicenses","2 Thessalonians"),("1TI","1 Timóteo","1 Timothy"),
("2TI","2 Timóteo","2 Timothy"),("TIT","Tito","Titus"),("PHM","Filemom","Philemon"),("HEB","Hebreus","Hebrews"),
("JAM","Tiago","James"),("1PE","1 Pedro","1 Peter"),("2PE","2 Pedro","2 Peter"),("1JO","1 João","1 John"),
("2JO","2 João","2 John"),("3JO","3 João","3 John"),("JUD","Judas","Jude"),("REV","Apocalipse","Revelation"),
]
assert len(LIVROS) == 66
COD = [l[0] for l in LIVROS]
NT = set(COD[39:])
AT = set(COD[:39])
def achar(txt):
    t = txt.strip().lower()
    for c, pt, en in LIVROS:
        if t in (c.lower(), pt.lower(), en.lower()) or t.replace(" ", "") == pt.lower().replace(" ", ""):
            return c
    return None
def nome(c, lang="pt"):
    for cc, pt, en in LIVROS:
        if cc == c:
            return pt if lang == "pt" else en
    return c
