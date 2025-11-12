import pandas as pd

files = ["languages_dicto_ngiemboon_to_english.csv", "languages_newtestament_ngiemboon_to_english.csv"]
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.to_csv("ngiemboon_to_english.csv", index=False)

files = ["languages_dicto_english_to_ngiemboon.csv", "languages_newtestament_english_to_ngiemboon.csv"]
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.to_csv("english_to_ngiemboon.csv", index=False)




files = ["languages_dicto_ngiemboon_to_english.csv", "languages_newtestament_ngiemboon_to_english.csv"]

# Combine all CSVs
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Duplicate and swap columns for reverse direction
reverse_df = df.rename(columns={"ngiemboon": "en", "en": "ngiemboon"})

# Add language direction tags
df["src_lang"] = "ngiemboon"
reverse_df["src_lang"] = "en"

# Combine both
combined_df = pd.concat([df, reverse_df], ignore_index=True)

# Save
combined_df.to_csv("ngiemboon_en_bidirectional.csv", index=False)

print(combined_df.head())

