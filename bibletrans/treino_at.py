"""Experimento honesto. Treina so no Novo Testamento e avalia em livros do Antigo
que o modelo nunca viu (Rute, Jonas, Genesis 1), no mesmo protocolo do eBible.

Uso no Colab (GPU):
    python treino_at.py Shona sna_Latn
    python treino_at.py "Q'eqchi'" quy_Latn      # lingua fora do NLLB, usa um token emprestado

Metricas: chrF3 (char 6, beta 3, como no eBible) e chrF++ (word_order 2).
Saida: resultado_<nome>.json com notas e as frases geradas de Rute 1 para revisao.
"""
import sys, re, os, random, json

corp, cod = sys.argv[1], sys.argv[2]
EPOCAS = int(os.environ.get("EPOCAS", "4"))
SECO = os.environ.get("SECO") == "1"
BASE = os.environ.get("CORPUS", "bible-corpus/bibles/")

NT = set("MAT MAR LUK JOH ACT ROM 1CO 2CO GAL EPH PHI COL 1TH 2TH 1TI 2TI TIT PHM "
         "HEB JAM 1PE 2PE 1JO 2JO 3JO JUD REV".split())
PAT = re.compile(r'<seg id="b\.([A-Z0-9]+)\.(\d+)\.(\d+)"[^>]*>(.*?)</seg>', re.S)


def ler(n):
    t = open(BASE + n + ".xml", encoding="utf-8").read()
    return {(m.group(1), int(m.group(2)), int(m.group(3))): re.sub(r"\s+", " ", m.group(4)).strip()
            for m in PAT.finditer(t)}


en, alvo = ler("English-WEB"), ler(corp)
par = lambda ks: [(en[k], alvo[k]) for k in ks if en.get(k) and alvo.get(k)]
chaves = sorted(alvo)
nt = par([k for k in chaves if k[0] in NT])
random.Random(1).shuffle(nt)
teste_nt, treino = nt[:200], nt[200:]
fora = {
    "Rute": par([k for k in chaves if k[0] == "RUT"]),
    "Jonas": par([k for k in chaves if k[0] == "JON"]),
    "Genesis 1": par([k for k in chaves if k[0] == "GEN" and k[1] == 1]),
}
print("idioma", corp, "token", cod, "treino NT", len(treino), "teste NT", len(teste_nt),
      {k: len(v) for k, v in fora.items()}, flush=True)
if SECO:
    sys.exit(0)

import torch, sacrebleu
from transformers import (AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer,
                          Seq2SeqTrainingArguments, DataCollatorForSeq2Seq)
from datasets import Dataset

M = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(M, src_lang="eng_Latn", tgt_lang=cod)
mod = AutoModelForSeq2SeqLM.from_pretrained(M)
dev = "cuda" if torch.cuda.is_available() else "cpu"
mod.to(dev)
CHRF3 = sacrebleu.metrics.CHRF(char_order=6, word_order=0, beta=3)
CHRFPP = sacrebleu.metrics.CHRF(word_order=2)


def gerar(textos):
    mod.eval(); out = []
    for i in range(0, len(textos), 16):
        x = tok(textos[i:i + 16], return_tensors="pt", padding=True, truncation=True, max_length=200).to(dev)
        with torch.no_grad():
            y = mod.generate(**x, forced_bos_token_id=tok.convert_tokens_to_ids(cod),
                             num_beams=4, max_new_tokens=256, max_length=None)
        out += tok.batch_decode(y, skip_special_tokens=True)
    return out


def avaliar(rotulo):
    r = {}
    for nome, ps in [("NT aleatorio", teste_nt[:100])] + list(fora.items()):
        h = gerar([p[0] for p in ps]); ref = [[p[1] for p in ps]]
        r[nome] = {"chrF3": round(CHRF3.corpus_score(h, ref).score, 1),
                   "chrF++": round(CHRFPP.corpus_score(h, ref).score, 1)}
        print(rotulo, nome, r[nome], flush=True)
    return r


antes = avaliar("ANTES")


def prep(e):
    return tok(e["en"], text_target=e["al"], truncation=True, max_length=200)


ds = Dataset.from_list([{"en": a, "al": b} for a, b in treino]).map(prep, remove_columns=["en", "al"])
args = Seq2SeqTrainingArguments(output_dir="out_at", per_device_train_batch_size=8, gradient_accumulation_steps=4,
                                learning_rate=1e-4, optim="adafactor", num_train_epochs=EPOCAS, warmup_steps=50,
                                fp16=torch.cuda.is_available(), logging_steps=50, save_strategy="no", report_to=[])
Seq2SeqTrainer(model=mod, args=args, train_dataset=ds,
               data_collator=DataCollatorForSeq2Seq(tok, model=mod)).train()
depois = avaliar("DEPOIS")

rute1 = [p for p in fora["Rute"]][:22]
amostra = [{"en": a, "referencia": b, "modelo": h} for (a, b), h in zip(rute1, gerar([p[0] for p in rute1]))]
nome = re.sub(r"[^A-Za-z]", "", corp)
json.dump({"idioma": corp, "token": cod, "epocas": EPOCAS, "pares_treino": len(treino),
           "antes": antes, "depois": depois, "rute_1": amostra},
          open("resultado_%s.json" % nome, "w"), ensure_ascii=False, indent=1)
print("RESUMO", corp, json.dumps(depois, ensure_ascii=False), flush=True)
for s in amostra[:3]:
    print("AMOSTRA", s["en"], "=>", s["modelo"], "|| REF", s["referencia"], flush=True)
print("PRONTO resultado_%s.json" % nome, flush=True)
