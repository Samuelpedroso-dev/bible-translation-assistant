"""Gera o caderno do Colab que treina o modelo do idioma escolhido."""
import json, os, base64
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def gerar(corpus_nome, codigo, saida):
    src = open(os.path.join(RAIZ, "bibletrans", "treino.py"), encoding="utf-8").read()
    b64 = base64.b64encode(src.encode()).decode()
    cel = lambda s: {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.splitlines(True)}
    nb = {"nbformat": 4, "nbformat_minor": 5, "metadata": {"accelerator": "GPU", "colab": {"provenance": []}, "kernelspec": {"name": "python3", "display_name": "Python 3"}},
          "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": ["# Treino do idioma %s\n" % corpus_nome, "Runtime > Alterar tipo de ambiente > GPU T4. Depois Executar tudo."]},
            cel("!pip -q install transformers datasets sacrebleu sentencepiece accelerate\n!git clone -q https://github.com/christos-c/bible-corpus"),
            cel("import base64\nopen('treino.py','w').write(base64.b64decode('%s').decode())" % b64),
            cel("!python treino.py %s %s" % (corpus_nome, codigo)),
            cel("from google.colab import files\nfiles.download('modelo_%s.zip')" % codigo)]}
    json.dump(nb, open(saida, "w"), indent=1)
    return saida
