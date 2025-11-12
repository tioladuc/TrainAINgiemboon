from transformers import MarianTokenizer, MarianMTModel

model_path = "./models/ngiemboon_en_bilingual_lundi"
tokenizer = MarianTokenizer.from_pretrained(model_path)
model = MarianMTModel.from_pretrained(model_path)

def translate(text, target_lang="en"):
    prefix = ">>en<<" if target_lang == "en" else ">>ng<<"
    inputs = tokenizer([prefix + " " + text], return_tensors="pt", padding=True)
    translated = model.generate(**inputs, max_length=128)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

print("Ngiembɔɔn → English:", translate("Aayi! Mbàŋa tʉ̌ kǔ kwò mèŋ.", "en"))
print("English → Ngiembɔɔn:", translate("What you say is correct.", "ng"))

