import os
import shutil
import pandas as pd
from datasets import Dataset
#import pandas as pd
#from datasets import Dataset, concatenate_datasets
#from transformers import MarianTokenizer, MarianMTModel, DataCollatorForSeq2Seq
#from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments


mainFolder = (__file__).split('\\')[-1].split('_')[0]
data_Folder = "../training_datasets/" + mainFolder
testing_Folder = "../testing_models/" + mainFolder
model_Folder = "../models/" + mainFolder
log_Folder = "../logs/" + mainFolder
bleu_folder = "../bleu_score/" + mainFolder
translator_Interface = "../translator_interfaces/" + mainFolder
# --- 1. CONFIGURATION ---
#model_name = "Helsinki-NLP/opus-mt-en-fr"  # small + efficient
#data_path = "./data/data_mardi"
#output_dir = "./models/ngiemboon_en_bilingual_mardi"

destination_En_Ngiemboon = data_Folder + "/en_ngiemboon"
destination_Ngiemboon_En = data_Folder + "/ngiemboon_en"
destination_bible_En_Ngiemboon = data_Folder + "/bible_en_ngiemboon"
model_name = "Helsinki-NLP/opus-mt-en-fr"
dataset = None
tokenizer = None
model = None


def init_check_creating_folder():
    results = []
    if os.path.isdir(data_Folder):
        results.append(f"The folder '{data_Folder}' exists.")
    else:
        os.mkdir(data_Folder)
        results.append(f"The folder '{data_Folder}' is being created.")

    if os.path.isdir(testing_Folder):
        results.append(f"The folder '{testing_Folder}' exists.")
    else:
        os.mkdir(testing_Folder)
        results.append(f"The folder '{testing_Folder}' is being created.")

    ########
    if os.path.isdir(model_Folder):
        results.append(f"The folder '{data_Folder}' exists.")
    else:
        os.mkdir(model_Folder)
        results.append(f"The folder '{model_Folder}' is being created.")

    if os.path.isdir(log_Folder):
        results.append(f"The folder '{log_Folder}' exists.")
    else:
        os.mkdir(log_Folder)
        results.append(f"The folder '{log_Folder}' is being created.")

    ########
    if os.path.isdir(bleu_folder):
        results.append(f"The folder '{bleu_folder}' exists.")
    else:
        os.mkdir(bleu_folder)
        results.append(f"The folder '{bleu_folder}' is being created.")

    if os.path.isdir(translator_Interface):
        results.append(f"The folder '{translator_Interface}' exists.")
    else:
        os.mkdir(translator_Interface)
        results.append(f"The folder '{translator_Interface}' is being created.")

    print("\n\n\n>>> init_check_creating_folder")
    with open(log_Folder + '1-init_check_creating_folder.txt', 'w') as f:
        for line in results:
            f.write(line + '\n')
            print("    " + line)
    print

def check_ready_to_start():
    results = []
    if os.listdir(data_Folder):
        results.append("training data existing .....................OK")
    else:
        results.append("training data does not exist ...............KO")

    if os.listdir(testing_Folder):
        results.append("testing scripts existing .....................OK")
    else:
        results.append("testing scripts do not exist .................KO")
    ########
    if os.listdir(model_Folder):
        results.append("training model existing .....................OK")
    else:
        results.append("training model does not exist ...............KO")

    if os.listdir(bleu_folder):
        results.append("BLEU scripts existing .....................OK")
    else:
        results.append("BLEU scripts do not exist .................KO")

    if os.listdir(translator_Interface):
        results.append("translator interface scripts existing .....................OK")
    else:
        results.append("translator interface scripts do not exist .................KO")


    print("\n\n\n>>> check_ready_to_start")
    with open(log_Folder + '2-check_ready_to_start.txt', 'w') as f:
        for line in results:
            f.write(line + '\n')
            print("    " + line)

def copy_files_from_folder_to_folder(source, destination):
    # Copy all files (not subfolders)
    for filename in os.listdir(source):
        src_file = os.path.join(source, filename)
        dst_file = os.path.join(destination, filename)
        
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)  # copy2 keeps metadata

def collecting_csv_for_training_data_set():
    source_dico_En_Ngiemboon = "../../ExtractNgiemboonDictionnary/english_to_ngiemboon_transform"
    source_dico_Ngiemboon_EN = "../../ExtractNgiemboonDictionnary/ngiemboon_to_english_transform"
    source_bible_En_Ngiemboon = "../../ExtractNgiemboonBible/csv_bible/0_ALL"
    
    # Make sure destination folder exists
    results = []
    if os.path.isdir(destination_En_Ngiemboon):
        results.append(f"The folder '{destination_En_Ngiemboon}' exists.")
    else:
        os.makedirs(destination_En_Ngiemboon, exist_ok=True)
        results.append(f"The folder '{destination_En_Ngiemboon}' is being created.")

    if os.path.isdir(destination_Ngiemboon_En):
        results.append(f"The folder '{destination_Ngiemboon_En}' exists.")
    else:
        os.makedirs(destination_Ngiemboon_En, exist_ok=True)
        results.append(f"The folder '{destination_Ngiemboon_En}' is being created.")

    if os.path.isdir(destination_bible_En_Ngiemboon):
        results.append(f"The folder '{destination_bible_En_Ngiemboon}' exists.")
    else:
        os.makedirs(destination_bible_En_Ngiemboon, exist_ok=True)
        results.append(f"The folder '{destination_bible_En_Ngiemboon}' is being created.")    
    
    results.append(f"moving csv files from {source_dico_En_Ngiemboon} to {destination_En_Ngiemboon}")
    copy_files_from_folder_to_folder(source_dico_En_Ngiemboon, destination_En_Ngiemboon)
    results.append(f"moving csv files from {source_dico_Ngiemboon_EN} to {destination_Ngiemboon_En}")
    copy_files_from_folder_to_folder(source_dico_Ngiemboon_EN, destination_Ngiemboon_En)
    results.append(f"moving csv files from {source_bible_En_Ngiemboon} to {destination_bible_En_Ngiemboon}")
    copy_files_from_folder_to_folder(source_bible_En_Ngiemboon, destination_bible_En_Ngiemboon)
        
    print("\n\n\n>>> collecting_csv_for_training_data_set")
    with open(log_Folder + '3-collecting_csv_for_training_data_set.txt', 'w') as f:
        for line in results:
            f.write(line + '\n')
            print("    " + line)
    return 

def ai_pick_base_training_model_name():
    return "Helsinki-NLP/opus-mt-en-fr"  # small + efficient

def ai_preparing_training_data_set():  

    # Define your folders
    folders = {
        "En_Ngiemboon": {"path": destination_En_Ngiemboon, "headers": ("en", "ngiemboon"), "bidirectional": False},
        "Ngiemboon_En": {"path": destination_Ngiemboon_En, "headers": ("ngiemboon", "en"), "bidirectional": False},
        "bible_En_Ngiemboon": {"path": destination_bible_En_Ngiemboon, "headers": ("ngiemboon", "en"), "bidirectional": True},
    }

    pairs = []

    for name, cfg in folders.items():
        data_path = cfg["path"]
        src_col, tgt_col = cfg["headers"]

        # Collect CSV files
        csv_files = [os.path.join(data_path, f)
                    for f in os.listdir(data_path) if f.endswith(".csv")]

        for f in csv_files:
            df = pd.read_csv(f)
            df = df.dropna(subset=[src_col, tgt_col])
            df[src_col] = df[src_col].astype(str).str.strip()
            df[tgt_col] = df[tgt_col].astype(str).str.strip()

            # One direction
            for src, tgt in zip(df[src_col], df[tgt_col]):
                pairs.append({"src": f">>{tgt_col[:2]}<< {src}", "tgt": tgt})

                # Add reverse if bidirectional
                if cfg["bidirectional"]:
                    pairs.append({"src": f">>{src_col[:2]}<< {tgt}", "tgt": src})

    # Convert to HuggingFace Dataset and split
    dataset = Dataset.from_pandas(pd.DataFrame(pairs)).train_test_split(test_size=0.1)

    print(f"Training samples: {len(dataset['train'])}")
    print(f"Test samples: {len(dataset['test'])}")
    return dataset

def ai_load_model_tokenizer(model_name):
    # --- 3. LOAD MODEL & TOKENIZER ---
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def ai_preprocess_function(batch):
    model_inputs = tokenizer(
        batch["src"],
        text_target=batch["tgt"],
        truncation=True,
        padding="max_length",
        max_length=128,
    )
    return model_inputs

def ai_save_log(text, appendMode=True):
    file_name = '0-main.txt'
    if(appendMode == False):
        with open(log_Folder + file_name, 'w') as f:
             f.write(text + '\n')
    else:
        with open(log_Folder + file_name, 'a') as f:
             f.write(text + '\n')

def main():
    print("\n\n\n>>> Main Training AI")
    ai_save_log(">>> Main Training AI", appendMode=False)

   
    # --- 1. CONFIGURATION ---
    ai_save_log("# --- 1. CONFIGURATION ---")
    print("# --- 1. CONFIGURATION ---")
    #1# init_check_creating_folder()
    #2# check_ready_to_start()
    #3# preparing_training_data_set()
    model_name = ai_pick_base_training_model_name()

    # --- 2. LOAD ALL CSV FILES ---
    ai_save_log("# --- 2. LOAD ALL CSV FILES ---")
    print("# --- 2. LOAD ALL CSV FILES ---")
    dataset = ai_preparing_training_data_set()

    # --- 3. LOAD MODEL & TOKENIZER ---
    ai_save_log("# --- 3. LOAD MODEL & TOKENIZER ---" )
    print("# --- 3. LOAD MODEL & TOKENIZER ---")
    tokenizer, model = ai_load_model_tokenizer(model_name)

    # --- 4. PREPROCESS FUNCTION ---
    ai_save_log("# --- 4. PREPROCESS FUNCTION ---" )
    print("# --- 4. PREPROCESS FUNCTION ---")
    tokenized_datasets = dataset.map(ai_preprocess_function, batched=True, remove_columns=["src", "tgt"])

    # --- 5. DATA COLLATOR ---
    ai_save_log("# --- 5. DATA COLLATOR ---" )
    print("# --- 5. DATA COLLATOR ---")
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # --- 6. TRAINING ARGUMENTS ---
    ai_save_log("# --- 6. TRAINING ARGUMENTS ---" )
    print("# --- 6. TRAINING ARGUMENTS ---")
    training_args = Seq2SeqTrainingArguments(
            output_dir=model_Folder,
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            num_train_epochs=5,
            weight_decay=0.01,
            save_total_limit=2,
            predict_with_generate=True,
            fp16=False,
            logging_dir="./logs_" + mainFolder,
            logging_strategy="steps",
            logging_steps=100,
        )

    # --- 7. TRAINER ---
    ai_save_log("# --- 7. TRAINER ---" )
    print("# --- 7. TRAINER ---")
    trainer = Seq2SeqTrainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets["train"],
            eval_dataset=tokenized_datasets["test"],
            tokenizer=tokenizer,
            data_collator=data_collator,
        )


    # --- 8. TRAIN ---
    ai_save_log("# --- 8. TRAIN ---" )
    print("# --- 8. TRAIN ---")
    trainer.train()

    # --- 9. SAVE MODEL ---
    ai_save_log("# --- 9. SAVE MODEL ---" )
    print("# --- 9. SAVE MODEL ---")
    trainer.save_model(model_Folder)
    tokenizer.save_pretrained(model_Folder)

    ai_save_log(f"✅ Bilingual training complete. Model saved to: {model_Folder}" )
    print(f"✅ Bilingual training complete. Model saved to: {model_Folder}")

main()
    