1) get the git repository
2) Prepare the environnement for python
    python -m venv env
    env/Scripts/activate.bat
3) install the other stuffs
    pip install -r requirements.txt

4) prepare data for text ngiemboon translation
5) ngiemboon_text repository
6) use extract_dictionnary.py that produce "languages.csv" for dictionnary of ngiemboon
7) use extract_new_testament_bible.py that produce "languages_bible.csv" for new testament verset translation with ngiemboon
8) pip install sacrebleu

9) transform numpy, transformers
pip uninstall -y transformers numpy
pip cache purge
pip install "numpy<2.0" "transformers==4.42.4"
pip show transformers numpy | grep Version























# Dialect Voice Assistant Prototype
Whisper (listening) → BLOOMZ (understanding/responding) → Coqui TTS (speaking)

## What You Get
- `app.py` – A single script that runs the full pipeline (CLI or Gradio UI).
- `requirements.txt` – Install dependencies.
- This README.

## Install
> Python 3.10+ is recommended. You also need `ffmpeg` installed on your system.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

If you have a GPU + CUDA, install a GPU build of PyTorch first (see pytorch.org).

## Run (CLI)
```bash
python app.py \
  --input_wav path/to/input.wav \
  --whisper_model medium \
  --bloomz_model bigscience/bloomz-560m \
  --tts_model_path path/to/your_dialect_tts_model.pth \
  --out_wav response.wav \
  --language_code auto
```

- Use `--language_code auto` to let Whisper detect the language automatically, or set a code (e.g., `fr`, `en`, or your dialect code if supported).
- If you **don’t** have a local TTS model, try a community model name instead:
  ```bash
  python app.py --ui --tts_model_name tts_models/multilingual/multi-dataset/your_choice
  ```

## Run (Gradio UI)
```bash
python app.py --ui
```
Then open the local URL shown in the terminal. In the **Model Settings** accordion:
- Set your Whisper model (e.g., `small`, `medium`, `large` or a path to your fine-tuned model).
- Set `BLOOMZ model` to your fine-tuned path if you trained on your dialect (e.g., `./dialect_bloomz`).
- Provide **either** a `TTS model name` (from Coqui community) **or** a `TTS model path` to a local `.pth` model trained for your dialect.
- Optionally set a `system prompt` like: `Réponds en dialecte, poliment et avec des phrases courtes.`

## Fine-tuning Notes
- **Whisper**: Fine-tune with your dialect audio + transcripts (10–100+ hours ideal). Export a `.pt` or checkpoint; pass its path via `--whisper_model` if using a custom load mechanism, or replace the load call.
- **BLOOMZ**: Fine-tune on your parallel corpus (Dialect ↔ FR/EN). Save to `./dialect_bloomz` and set `--bloomz_model ./dialect_bloomz`.
- **Coqui TTS**: Train on clean, single-speaker recordings in your dialect. Save a `.pth` and use `--tts_model_path`.

## Tips
- Keep utterances ~5–15 seconds for best ASR accuracy.
- If BLOOMZ echoes the prompt, it will be trimmed in post-processing.
- Some TTS models support `speaker` names; pass `--speaker myvoice` if applicable.
- For production, consider faster ASR (`faster-whisper`) and quantized NLP models.

## Troubleshooting
- **whisper not available**: Ensure `openai-whisper` and `ffmpeg` are installed and on PATH.
- **CUDA OOM**: Use a smaller Whisper model, or BLOOMZ size (`bloomz-560m`), or run on CPU.
- **TTS voice quality**: Train Coqui TTS on a clean dataset with consistent mic and environment.

---

Made for rapid prototyping: plug in your **fine-tuned** models when they’re ready.
