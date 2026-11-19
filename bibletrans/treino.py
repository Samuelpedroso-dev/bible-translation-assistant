"""Script de treino. Roda no Colab (GPU). Uso: python treino.py Dinka-NT dik_Latn
Aprende com o Novo Testamento alinhado ao ingles WEB (dominio publico)."""
import sys, re, os, random, json, subprocess
corp, cod = sys.argv[1], sys.argv[2]
EPOCAS = int(os.environ.get("EPOCAS", "4"))
BASE = "bible-corpus/bibles/"
PAT = re.compile(r'<seg id="b\.([A-Z0-9]+)\.(\d+)\.(\d+)"[^>]*>(.*?)</seg>', re.S)
def ler(n):
    t = open(BASE + n + ".xml", encoding="utf-8").read()
    return {(m.group(1), int(m.group(2)), int(m.group(3))): re.sub(r"\s+", " ", m.group(4)).strip() for m in PAT.finditer(t)}
en, alvo = ler("English-WEB"), ler(corp)
par = [(en[k], alvo[k]) for k in sorted(alvo) if k in en and en[k] and alvo[k]]
random.Random(1).shuffle(par)
dev, teste, treino = par[:200], par[200:400], par[400:]
print("pares", len(par), "treino", len(treino))
import torch, sacrebleu
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset
M = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(M, src_lang="eng_Latn", tgt_lang=cod)
mod = AutoModelForSeq2SeqLM.from_pretrained(M)
dev_ = "cuda" if torch.cuda.is_available() else "cpu"
def chrf(ps):
    mod.eval(); hip = []
    for i in range(0, len(ps), 16):
        b = [p[0] for p in ps[i:i+16]]
        x = tok(b, return_tensors="pt", padding=True, truncation=True, max_length=128).to(dev_)
        with torch.no_grad():
            y = mod.generate(**x, forced_bos_token_id=tok.convert_tokens_to_ids(cod), max_new_tokens=128, num_beams=4)
        hip += tok.batch_decode(y, skip_special_tokens=True)
    return sacrebleu.corpus_chrf(hip, [[p[1] for p in ps]], word_order=2).score
mod.to(dev_)
antes = chrf(teste[:100]); print("chrF++ antes", antes)
def prep(e):
    return tok(e["en"], text_target=e["al"], truncation=True, max_length=128)
ds = Dataset.from_list([{"en": a, "al": b} for a, b in treino]).map(prep, remove_columns=["en", "al"])
args = Seq2SeqTrainingArguments(output_dir="out", per_device_train_batch_size=8, gradient_accumulation_steps=4,
    learning_rate=1e-4, optim="adafactor", num_train_epochs=EPOCAS, warmup_steps=50, fp16=torch.cuda.is_available(),
    logging_steps=50, save_strategy="no", report_to=[])
Seq2SeqTrainer(model=mod, args=args, train_dataset=ds, data_collator=DataCollatorForSeq2Seq(tok, model=mod)).train()
depois = chrf(teste[:100]); print("chrF++ depois", depois)
os.makedirs("modelo_hf", exist_ok=True); mod.save_pretrained("modelo_hf"); tok.save_pretrained("modelo_hf")
json.dump({"idioma": corp, "codigo": cod, "chrf_antes": antes, "chrf_depois": depois, "pares_treino": len(treino)}, open("modelo_hf/relatorio.json", "w"))
subprocess.run("pip -q install ctranslate2 && ct2-transformers-converter --model modelo_hf --output_dir modelo_ct2 --quantization int8 --force", shell=True, check=True)
subprocess.run("cp modelo_hf/relatorio.json modelo_hf/sentencepiece.bpe.model modelo_ct2/ && zip -rq modelo_%s.zip modelo_ct2" % cod, shell=True, check=True)
print("PRONTO modelo_%s.zip" % cod)
