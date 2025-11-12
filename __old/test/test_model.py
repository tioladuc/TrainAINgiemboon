from transformers import MarianTokenizer
tok = MarianTokenizer.from_pretrained("./models/ngiemboon_en_translator")
print(tok.tokenize("ànɔ̀ŋ", add_special_tokens=False))

