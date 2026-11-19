<div align="center">

<img src="assets/simbolo.png" width="110" alt="Jerusalem cross">

# Bible Translation Assistant

**Machine drafts of Scripture for languages that only have the New Testament.**
Built on Meta's NLLB. Free, local, no API key. Every draft requires validation by native speakers.

</div>

## What it does
- Chat interface that prepares a language, trains a model, and drafts books after your approval.
- Parallel PDF typesetting in the style of classic parallel Bibles, source on the left and draft on the right.
- Training on Google Colab (free T4), inference on your own CPU through CTranslate2.
- Automatic diary and markdown report, ready to document and publish.
- Browser agent layer (Playwright and an optional local LLM) for research.

## Quick start
```
pip install -r requirements.txt
git clone https://github.com/christos-c/bible-corpus dados/bible-corpus
python app.py
```
Open http://127.0.0.1:8000. The same screen is also published as a live page, connected to your local engine when it is running.

Live page https://samuelpedroso-dev.github.io/bible-translation-assistant/
```
In the chat type `prepare dinka` style commands in Portuguese, starting with `ajuda`. Train with `treinar dinka`, open the generated notebook on Colab, download the model, unzip into `modelos/dik_Latn`, then `importar modelo dinka`, `aprovar dinka` and `traduzir Rute para dinka`.

## First results
Dinka, NLLB 600M fine tuned on the New Testament: chrF++ 18.0 before and 48.8 after (different test slices, comparison is indicative). Kabyle baseline 31.2 before training.

## Sources and licensing
Parallel data from the christos-c bible-corpus. English source text is the World English Bible (public domain), because the ESV does not allow translation into other languages without permission. The cross image in `assets` must be replaced by a licensed or original version before any wide publication.

## Responsible use
Output is a draft, not a Bible translation. It must be reviewed and approved by native speakers and qualified translators before any use.

See [ROADMAP.md](ROADMAP.md).
