import os
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
    with open(log_Folder + 'init_check_creating_folder.txt', 'w') as f:
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
    with open(log_Folder + 'check_ready_to_start.txt', 'w') as f:
        for line in results:
            f.write(line + '\n')
            print("    " + line)

def preparing_data_set():
    return 

init_check_creating_folder()
check_ready_to_start()
print(mainFolder)