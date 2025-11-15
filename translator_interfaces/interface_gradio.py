import torch
from transformers import MarianTokenizer, MarianMTModel
import gradio as gr

# ---------- 1️⃣ LOAD YOUR LOCAL BILINGUAL MODEL ----------
MODEL_DIR = "./models/tuesday"

tokenizer = MarianTokenizer.from_pretrained(MODEL_DIR)
model = MarianMTModel.from_pretrained(MODEL_DIR)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# ---------- 2️⃣ TRANSLATION FUNCTION ----------
def translate(text, direction):
    text = text.strip()
    if not text:
        return ""

    # Use the same prefix tags used during training
    if direction == "Ngiemboon → English":
        prefixed_text = f">>en<< {text}"
    else:
        prefixed_text = f">>ng<< {text}"

    inputs = tokenizer(prefixed_text, return_tensors="pt", padding=True, truncation=True).to(device)

    outputs = model.generate(
        **inputs,
        max_length=256,
        num_beams=4,
        forced_eos_token_id=0
    )

    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# ---------- 3️⃣ GRADIO INTERFACE ----------
with gr.Blocks(theme=gr.themes.Soft(), title="🗣️ Ngiemboon ↔ English Translator") as demo:
    gr.Markdown("# 🌍 Ngiemboon ↔ English Translator")
    gr.Markdown("Translate both ways using your locally trained bilingual MarianMT model.")

    with gr.Row():
        input_text = gr.Textbox(
            label="Enter text (Ngiemboon or English)",
            placeholder="Type your sentence here...",
            lines=5
        )
        output_text = gr.Textbox(label="Translation", lines=5)

    direction = gr.Radio(
        choices=["Ngiemboon → English", "English → Ngiemboon"],
        value="Ngiemboon → English",
        label="Select translation direction"
    )

    translate_button = gr.Button("🔁 Translate")
    translate_button.click(translate, inputs=[input_text, direction], outputs=output_text)

    gr.Examples(
        examples=[
            ["Ndɔŋ mɛ̀ nù", "Ngiemboon → English"],
            ["Good morning my friend", "English → Ngiemboon"],
            ["Wɔ̀ nɛ̀ bɛ́?", "Ngiemboon → English"]
        ],
        inputs=[input_text, direction]
    )

# ---------- 4️⃣ LAUNCH ----------
if __name__ == "__main__":
    demo.launch()

