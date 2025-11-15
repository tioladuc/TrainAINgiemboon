import os
import pandas as pd
import glob
import random

SOURCE_DATA_DIR = "../../training_datasets/tuesday"

def creating_sample_for_bleu(source_data_dir):
    
    # ---- CONFIG ----
    DATA_FOLDER = "data"
    SAMPLE_SIZE = 100  # number of random rows (edit as needed)
    en_ngiemboon = source_data_dir + "/en_ngiemboon"
    ngiemboon_en = source_data_dir + "/ngiemboon_en"
    bible_en_ngiemboon = source_data_dir + "/bible_en_ngiemboon"
    OUTPUT_FOLDER = "sample"

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    def load_csv_files(folder_path, expected_cols=None, swap=False):
        """Load all CSV files from folder and normalize column order."""
        dataset = []

        for file in glob.glob(os.path.join(folder_path, "*.csv")):
            df = pd.read_csv(file)

            # If expected columns not matching and swap==True, invert the columns
            if expected_cols and list(df.columns) != expected_cols:
                if swap and list(df.columns) == expected_cols[::-1]:
                    df = df[[expected_cols[0], expected_cols[1]]]
                else:
                    print(f"[WARNING] Skipped file with unexpected format: {file}")
                    continue
            
            dataset.append(df)

        return pd.concat(dataset, ignore_index=True) if dataset else pd.DataFrame(columns=expected_cols)

    # ---- LOAD DATASETS ----

    # en → ngiemboon strictly
    en_ng_df = load_csv_files(os.path.join(DATA_FOLDER, en_ngiemboon), expected_cols=["en", "ngiemboon"])

    # ngiemboon → en strictly
    ng_en_df = load_csv_files(os.path.join(DATA_FOLDER, ngiemboon_en), expected_cols=["ngiemboon", "en"])

    # bidirectional folder — use twice (swap direction)
    bis_df = load_csv_files(os.path.join(DATA_FOLDER, bible_en_ngiemboon), expected_cols=["ngiemboon", "en"], swap=True)

    # Create datasets
    en_to_ng = pd.concat([en_ng_df, bis_df.rename(columns={"ngiemboon": "ngiemboon", "en": "en"})], ignore_index=True)
    ng_to_en = pd.concat([ng_en_df, bis_df.rename(columns={"ngiemboon": "ngiemboon", "en": "en"})], ignore_index=True)

    # ---- RANDOM SAMPLING ----
    # If dataset smaller than sample size, use full dataset
    sample_en_ng = en_to_ng.sample(min(SAMPLE_SIZE, len(en_to_ng)), random_state=42)
    sample_ng_en = ng_to_en.sample(min(SAMPLE_SIZE, len(ng_to_en)), random_state=42)

    # ---- SAVE RESULTS ----
    sample_en_ng.to_csv(os.path.join(OUTPUT_FOLDER, "en_ngiemboon.csv"), index=False)
    sample_ng_en.to_csv(os.path.join(OUTPUT_FOLDER, "ngiemboon_en.csv"), index=False)

    print("✔ Sample files generated successfully inside /sample/")
    print(f"- sample/en_ngiemboon.csv ({len(sample_en_ng)} rows)")
    print(f"- sample/ngiemboon_en.csv ({len(sample_ng_en)} rows)")





# ---------- 1️⃣ CONFIG ----------
MODEL_DIR = "../../models/tuesday"
SOURCE_DATA_DIR = "../../training_datasets/tuesday"
TEST_FILE = "./sample/ngiemboon_en.csv"  # Path to your test CSV file
SRC_LANG = "ngiemboon"
TGT_LANG = "en"

# ---------- 2️⃣ LOAD MODEL ----------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = MarianTokenizer.from_pretrained(MODEL_DIR)
model = MarianMTModel.from_pretrained(MODEL_DIR).to(device)
bleu = evaluate.load("sacrebleu")


# ---------- 3️⃣ LOAD TEST DATA ----------
creating_sample_for_bleu(SOURCE_DATA_DIR)
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
with open('./bleu_results_execution.txt', 'a') as file:
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