<div align="center">

<img src="docs/simbolo.svg" width="110" alt="Jerusalem cross">

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

## Models in testing
| Model | Language | chrF++ before | chrF++ after | Status |
|---|---|---|---|---|
| Verbum Dinka 1.0 | Dinka (dik) | 18.2 | 49.5 | testing |
| Verbum Kabyle 1.0 | Kabyle (kab) | 32.1 | 37.9 | testing |
| Verbum Wolof 1.0 | Wolof (wol) | 36.8 | 44.6 | testing |

All three are NLLB 200 distilled 600M fine tuned on English (WEB) to New Testament verse pairs, 4 epochs on a free Colab T4. Scores are on 100 held out New Testament verses, so they measure in domain quality only.

**Held out Old Testament evaluation (running).** `bibletrans/treino_at.py` trains on the New Testament only and scores Ruth, Jonah and Genesis 1, which the model never sees, using chrF3 as in the eBible benchmark (Akerman et al., 2023). First languages are Shona (known to NLLB) and Q'eqchi' (unknown to NLLB). Results will be added here.

## Run a model locally
Training happens on Colab, translation runs on your own CPU with no GPU and no internet.

1. On Colab run `python treino.py Wolof-NT wol_Latn`. It trains, converts the model to CTranslate2 int8 (about 600 MB) and writes `modelo_wol_Latn.zip`.
2. Download the zip from the Colab file panel before the session ends, the runtime is erased when it disconnects.
3. Unzip it inside `modelos/wol_Latn/`. The engine finds the files either there or in the `modelo_ct2` folder the zip creates.
4. Run `python app.py`, open http://127.0.0.1:8000, choose the model and type `aprovar wolof`, then `traduzir Rute para wolof`.

## Sources and licensing
Parallel data from the christos-c bible-corpus. Related work and benchmarks in the eBible corpus by SIL and partners. English source text is the World English Bible (public domain), because the ESV does not allow translation into other languages without permission. The Jerusalem cross used by the interface and the PDF cover is an original vector drawing.

## Responsible use
Output is a draft, not a Bible translation. It must be reviewed and approved by native speakers and qualified translators before any use.

See [ROADMAP.md](ROADMAP.md).
