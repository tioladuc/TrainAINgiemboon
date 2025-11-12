import pandas as pd

# --- 1. Input & output files ---
input_file = "financial_ngiemboon.csv"
output_file = "other_words_ngiemboon.csv"

# --- 2. Load data ---
df = pd.read_csv(input_file)

# --- 3. Prepare new expanded rows ---
new_rows = []

for _, row in df.iterrows():
    ng = row["ngiemboon"]
    en_text = str(row["en"]).strip()

    # Split by '/' if multiple meanings
    parts = [p.strip() for p in en_text.split("/")]

    # Add each meaning as a separate row
    for part in parts:
        if part:  # avoid empty strings
            new_rows.append({"ngiemboon": ng, "en": part})

# --- 4. Create new DataFrame ---
expanded_df = pd.DataFrame(new_rows)

# --- 5. Save new CSV ---
expanded_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"✅ Expanded CSV saved to: {output_file}")
print(f"Total lines before: {len(df)}, after: {len(expanded_df)}")
