"""Traducao local na CPU com CTranslate2 (modelo exportado pelo Colab)."""
import os, json
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def pasta_modelo(cod):
    p = os.path.join(RAIZ, "modelos", cod)
    sub = os.path.join(p, "modelo_ct2")
    return sub if os.path.exists(os.path.join(sub, "model.bin")) else p
def carregar(cod):
    import ctranslate2, sentencepiece as spm
    p = pasta_modelo(cod)
    return ctranslate2.Translator(p, device="cpu", inter_threads=1, intra_threads=os.cpu_count() or 2), spm.SentencePieceProcessor(os.path.join(p, "sentencepiece.bpe.model"))
def traduzir(cod, textos, lote=8, feixes=4):
    tr, sp = carregar(cod)
    saida = []
    for i in range(0, len(textos), lote):
        b = textos[i:i+lote]
        toks = [["eng_Latn"] + sp.encode(t, out_type=str) + ["</s>"] for t in b]
        r = tr.translate_batch(toks, target_prefix=[[cod]] * len(b), beam_size=feixes, max_decoding_length=200)
        for x in r:
            h = x.hypotheses[0]
            h = [t for t in h if t != cod]
            saida.append(sp.decode(h))
    return saida
def relatorio(cod):
    p = os.path.join(pasta_modelo(cod), "relatorio.json")
    return json.load(open(p)) if os.path.exists(p) else None
