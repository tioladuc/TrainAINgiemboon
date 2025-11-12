import os
import pandas as pd
import torch
from transformers import MarianMTModel, MarianTokenizer
import evaluate
from datetime import datetime
import os

# ---------- 1️⃣ CONFIG ----------
MODEL_DIR = "./models/ngiemboon_en_bilingual_vendredi"
TEST_FILE = "./BLEU/vendredi_bleu.csv"  # Path to your test CSV file
SRC_LANG = "ngiemboon"
TGT_LANG = "en"

# ---------- 2️⃣ LOAD MODEL ----------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = MarianTokenizer.from_pretrained(MODEL_DIR)
model = MarianMTModel.from_pretrained(MODEL_DIR).to(device)
bleu = evaluate.load("sacrebleu")

# ---------- 3️⃣ LOAD TEST DATA ----------
df = pd.read_csv(TEST_FILE).dropna(subset=[SRC_LANG, TGT_LANG])
src_texts = df[SRC_LANG].astype(str).tolist()
ref_texts = df[TGT_LANG].astype(str).tolist()

# ---------- 4️⃣ GENERATE TRANSLATIONS ----------
pred_texts = []

for text in src_texts:
    # Add your direction tag
    input_text = f">>en<< {text}"  # Translate Ngiemboon → English
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model.generate(**inputs, max_length=256, num_beams=4)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    pred_texts.append(translation)

# ---------- 5️⃣ COMPUTE BLEU ----------
results = bleu.compute(predictions=pred_texts, references=[[ref] for ref in ref_texts])

print("✅ BLEU Evaluation Complete")
print(f"BLEU score: {results['score']:.2f}")
print(f"Precisions: {results['precisions']}")
print(f"BP (brevity penalty): {results['bp']:.3f}")
# print(f"Length ratio: {results['ratio']:.3f}")


# Open the file in append mode ('a')
# The 'with' statement ensures the file is properly closed even if errors occur.
with open('./BLEU/bleu_data_lundi.txt', 'a') as file:
    # Write the data to the file.
    # Add a newline character '\n' if you want each piece of data on a new line.
    
    file.write("\n\n*******************************************************\n")
    file.write(str(datetime.now()) + " " + os.path.basename(__file__))
    file.write(f"\nBLEU score: {results['score']:.2f}\n")
    file.write(f"Precisions: {results['precisions']}\n")
    file.write(f"BP (brevity penalty): {results['bp']:.3f}\n")
    # file.write(f"Length ratio: {results['ratio']:.3f}\n")
    file.write(str(results))
    
    file.write("\n\n\n ")
