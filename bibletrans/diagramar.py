"""Diagramacao em PDF no estilo de Biblia paralela: esquerda fonte em ingles, direita rascunho."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, NextPageTemplate, KeepTogether
from xml.sax.saxutils import escape
from .livros import nome
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "fonts")
pdfmetrics.registerFont(TTFont("Serif", os.path.join(F, "DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("Serif-B", os.path.join(F, "DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Serif-I", os.path.join(F, "DejaVuSerif-Italic.ttf")))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
SIMBOLO = os.path.join(RAIZ, "assets", "simbolo.png")
S = dict(
 tit=ParagraphStyle("t", fontName="Serif-B", fontSize=26, leading=32, alignment=TA_CENTER),
 sub=ParagraphStyle("s", fontName="Serif", fontSize=12, leading=16, alignment=TA_CENTER),
 aviso=ParagraphStyle("a", fontName="Serif-I", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#444444")),
 livro=ParagraphStyle("l", fontName="Serif-B", fontSize=20, leading=24, alignment=TA_CENTER, spaceBefore=6, spaceAfter=10),
 cap=ParagraphStyle("c", fontName="Serif-B", fontSize=13, leading=16, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4),
 v=ParagraphStyle("v", fontName="Serif", fontSize=8.6, leading=11.2),
)
def _p(num, txt):
    return Paragraph('<font size="6.5"><super>%s</super></font> %s' % (num, escape(txt)), S["v"])
def pdf(saida, cod, lang_nome, esq, dir_, titulo_esq="English (WEB)", titulo_dir=None):
    """esq e dir_ sao dicts {(livro,cap,ver): texto}. Gera PDF de um livro."""
    titulo_dir = titulo_dir or lang_nome
    chaves = sorted(set(k for k in esq if k[0] == cod) | set(k for k in dir_ if k[0] == cod))
    W, H = A4
    doc = BaseDocTemplate(saida, pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=22*mm, bottomMargin=20*mm,
                          title="%s, %s" % (nome(cod), lang_nome), author="Projeto de traducao assistida")
    def capa(c, d):
        pass
    def corpo(c, d):
        c.saveState(); c.setFont("Serif", 8)
        c.drawString(16*mm, H-14*mm, "%s  ·  %s" % (nome(cod, "pt"), lang_nome))
        c.drawRightString(W-16*mm, H-14*mm, "RASCUNHO NÃO VALIDADO")
        c.line(16*mm, H-16*mm, W-16*mm, H-16*mm)
        c.drawCentredString(W/2, 11*mm, str(d.page))
        c.restoreState()
    fc = Frame(16*mm, 20*mm, W-32*mm, H-40*mm, id="c"); fb = Frame(16*mm, 20*mm, W-32*mm, H-42*mm, id="b")
    doc.addPageTemplates([PageTemplate("capa", [fc], onPage=capa), PageTemplate("corpo", [fb], onPage=corpo)])
    el = [Spacer(1, 30*mm)]
    if os.path.exists(SIMBOLO):
        im = Image(SIMBOLO); r = im.imageWidth / im.imageHeight; h = 70*mm
        im.drawHeight = h; im.drawWidth = h*r; im.hAlign = "CENTER"; el.append(im)
    el += [Spacer(1, 12*mm), Paragraph(nome(cod, "pt"), S["tit"]), Spacer(1, 4*mm),
           Paragraph("%s  ·  %s" % (titulo_esq, titulo_dir), S["sub"]), Spacer(1, 40*mm),
           Paragraph("Rascunho produzido por modelo de tradução automática. Não é uma tradução da Bíblia. "
                     "Todo o texto precisa ser revisado e aprovado por falantes nativos e tradutores qualificados antes de qualquer uso.", S["aviso"]),
           NextPageTemplate("corpo"), PageBreak(), Paragraph(nome(cod, "pt").upper(), S["livro"])]
    caps = sorted(set(k[1] for k in chaves))
    colw = (W - 32*mm) / 2
    for cp in caps:
        el.append(Paragraph("Capítulo %d" % cp, S["cap"]))
        linhas = [[Paragraph("<b>%s</b>" % escape(titulo_esq), S["v"]), Paragraph("<b>%s</b>" % escape(titulo_dir), S["v"])]]
        for k in [k for k in chaves if k[1] == cp]:
            linhas.append([_p(k[2], esq.get(k, "")), _p(k[2], dir_.get(k, ""))])
        t = Table(linhas, colWidths=[colw, colw], repeatRows=1, splitByRow=1)
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEAFTER", (0, 0), (0, -1), 0.4, colors.grey),
                               ("LINEBELOW", (0, 0), (-1, 0), 0.4, colors.grey), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 1), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 1), (-1, -1), 1.5)]))
        el.append(t)
    doc.build(el)
    return saida
