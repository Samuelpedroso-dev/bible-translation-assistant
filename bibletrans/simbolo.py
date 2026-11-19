"""Cruz de Jerusalem desenhada em vetor, desenho original sem imagem de banco."""
from reportlab.platypus import Flowable
def _rets():
    r = [(42, 12, 16, 76), (12, 42, 76, 16), (30, 6, 40, 10), (30, 84, 40, 10), (6, 30, 10, 40), (84, 30, 10, 40)]
    for cx in (27, 73):
        for cy in (27, 73):
            r += [(cx - 7, cy - 2.5, 14, 5), (cx - 2.5, cy - 7, 5, 14)]
    return r
RETS = _rets()
def svg(cor="currentColor"):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="%s">%s</svg>' % (
        cor, "".join('<rect x="%g" y="%g" width="%g" height="%g"/>' % r for r in RETS))
class Cruz(Flowable):
    def __init__(self, tam):
        super().__init__(); self.tam = tam; self.width = tam; self.height = tam; self.hAlign = "CENTER"
    def draw(self):
        k = self.tam / 100.0
        self.canv.setFillColorRGB(0, 0, 0)
        for x, y, w, h in RETS:
            self.canv.rect(x * k, (100 - y - h) * k, w * k, h * k, stroke=0, fill=1)
