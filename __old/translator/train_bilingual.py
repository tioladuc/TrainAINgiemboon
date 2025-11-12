import os
import pandas as pd
from datasets import load_dataset, Dataset, concatenate_datasets
from transformers import MarianTokenizer, MarianMTModel, DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

# --- 1. CONFIGURATION ---
model_name = "Helsinki-NLP/opus-mt-en-fr"  # small + efficient
data_path = "./data/initial"  # folder containing file1.csv, file2.csv, file3.csv
output_dir = "./models/ngiemboon_en_translator"

# --- 2. LOAD ALL CSV FILES ---
csv_files = [os.path.join(data_path, f) for f in os.listdir(data_path) if f.endswith(".csv")]
datasets = []

for f in csv_files:
    df = pd.read_csv(f)
    df = df.dropna(subset=["ngiemboon", "en"])  # ensure valid rows
    datasets.append(Dataset.from_pandas(df))

dataset = concatenate_datasets(datasets).train_test_split(test_size=0.1)

# --- 3. LOAD MODEL & TOKENIZER ---
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# --- 4. PREPROCESS FUNCTION ---
def preprocess_function(batch):
    inputs = batch["ngiemboon"]
    targets = batch["en"]
    model_inputs = tokenizer(inputs, text_target=targets, truncation=True, padding="max_length", max_length=128)
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=["ngiemboon", "en"])

# --- 5. DATA COLLATOR ---
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# --- 6. TRAINING ARGUMENTS ---
training_args = Seq2SeqTrainingArguments(
    output_dir=output_dir,
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=1,#  4,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    fp16=False,  # CPU only
    predict_with_generate=True,
    logging_dir="./logs",
    logging_strategy="steps",
    logging_steps=50,
)

# --- 7. TRAINER ---
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# --- 8. TRAIN ---
trainer.train()

# --- 9. SAVE MODEL ---
trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"✅ Training complete. Model saved to: {output_dir}")

