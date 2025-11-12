import pandas as pd
# Make sure WordNet is downloaded
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

input_file = "other_words_ngiemboon.csv"
output_file = "other_words_ngiemboon_syn.csv"

def get_synonyms_array(word):
    synonyms = set()
    if " " in word.strip() :
        return [word]
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

# --- 2. Load data ---
df = pd.read_csv(input_file)

# --- 3. Prepare new expanded rows ---
new_rows = []

for _, row in df.iterrows():
    ng = row["ngiemboon"]
    en_text = str(row["en"]).strip()
    array_en = get_synonyms_array(en_text)

    for english in array_en:
        new_rows.append({"ngiemboon": ng, "en": english})


# --- 4. Create new DataFrame ---
expanded_df = pd.DataFrame(new_rows)

# --- 5. Save new CSV ---
expanded_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"✅ Expanded CSV saved to: {output_file}")
print(f"Total lines before: {len(df)}, after: {len(expanded_df)}")
