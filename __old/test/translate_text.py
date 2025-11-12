from transformers import MarianTokenizer, MarianMTModel

# Load your fine-tuned model
model_name = "./models/ngiemboon_en_translator"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate(text, direction="ngiemboon_to_en"):
    if direction == "en_to_ngiemboon":
        text = f">>ngiemboon<< {text}"  # if you trained bilingual direction tags
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    translated_tokens = model.generate(**inputs, max_length=128)
    translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translation

# Example usage
print("🔤 Translating from Ngiembɔɔn to English:")
print(translate("Shʉ́ŋngẅi néŋe nzɔ̌? Á ssé"))

print("\n🔤 Translating from English to Ngiembɔɔn:")
print(translate("see you soon", direction="en_to_ngiemboon"))

