from bs4 import BeautifulSoup
import requests
import csv
import re
import json
import time
#import deep_translator

# In virtual environment
# pip install deep_translator
from deep_translator import GoogleTranslator
Translator = GoogleTranslator(source='fr', target='en') # Translator.translate(text)

# pip install googletrans==4.0.0-rc1
# from deep_translator import Translator


def extract_span_text_from_class(span_info, class_name):
    if span_info.find("span", class_=class_name) :
        return span_info.find("span", class_=class_name).get_text().replace('\xa0', ' ').strip()
    return ""

def extract_span_text_from_attribut_value(span_info, attrib_name, attrib_value):
    if span_info.find("span", {attrib_name:attrib_value}) :
        return span_info.find("span", {attrib_name:attrib_value}).get_text().replace('\xa0', ' ').strip()
    return ""

def extract_noun(line_dictionnary):
    #print(line_dictionnary)
    base_pattern = line_dictionnary.find("span", class_="reversalform")
    base_pattern = extract_span_text_from_attribut_value(base_pattern, 'lang', 'en')
    return base_pattern

def extract_pronounciation(line_dictionnary):
    return extract_span_text_from_class(line_dictionnary, "pronunciation")

def extract_synonym(line_dictionnary):
    list_synonym = extract_span_text_from_class(line_dictionnary, "synonym")
    if list_synonym == "":
        return []
    return extract_span_text_from_class(line_dictionnary, "synonym").split(';')

def extract_sharedgrammaticalinfo_partofspeech(line_dictionnary):
    base_pattern_partofspeech = line_dictionnary.find("span", class_="sharedgrammaticalinfo")
    
    if base_pattern_partofspeech :
        return extract_span_text_from_class(base_pattern_partofspeech, "partofspeech")
    return ""

def extract_sharedgrammaticalinfo_morphtypes(line_dictionnary):
    base_pattern_morphtypes = line_dictionnary.find("span", class_="sharedgrammaticalinfo")
    if base_pattern_morphtypes :
        return extract_span_text_from_class(base_pattern_morphtypes, "morphtypes")
    return ""

def extract_sensecontent(line_dictionnary):
    resultat = []
    for sense in line_dictionnary.find_all("span", class_="sensecontent"):
        definition_fr = extract_span_text_from_class(sense, "definitionorgloss")
        definition_en = sense.find("span", class_="headword").find("a").get_text()#extract_span_text_from_class(sense, "headword")
        array_example = []
        
        if definition_en == "":
            definition_en = Translator.translate(definition_fr)
                
        for example in sense.find_all("span", class_="examplescontent"):
            example_ngiemboon = extract_span_text_from_attribut_value(example, "lang", "nnh")
            example_fr = extract_span_text_from_attribut_value(example, "lang", "fr")
            example_en = extract_span_text_from_attribut_value(example, "lang", "en")

            if example_en == "":
                example_en = Translator.translate(example_fr)

            array_example.append({"dialect":example_ngiemboon, "fr":example_fr, "en":example_en})
            
        resultat.append({"definition_fr":definition_fr, "definition_en":definition_en, "examples":array_example})
    return resultat


def extract_dictionnary_text(source, from_url=True):
    results = []

    # --- Load HTML ---
    if from_url:
        html = requests.get(source).text
    else:
        with open(source, encoding="utf-8") as f:
            html = f.read()

    # --- Check for the 'no entries' message ---
    if "No entries exist starting with this letter." in html:
        #print("⚠️ No entries found in this page.")
        return []

    # --- Parse HTML ---
    soup = BeautifulSoup(html, "html.parser")

    for line_dictionnary in soup.find_all("div", class_="post"):        
        noun = extract_noun(line_dictionnary)
        pronounciation = extract_pronounciation(line_dictionnary)
        synonym = extract_synonym(line_dictionnary)
        
        sharedgrammaticalinfo_partofspeech = extract_sharedgrammaticalinfo_partofspeech(line_dictionnary)
        sharedgrammaticalinfo_morphtypes = extract_sharedgrammaticalinfo_morphtypes(line_dictionnary)
        sensecontents = extract_sensecontent(line_dictionnary)
                
        results.append({"noun":noun, "pronounciation":pronounciation, "synonym": synonym, "sharedgrammaticalinfo_partofspeech": sharedgrammaticalinfo_partofspeech, "sharedgrammaticalinfo_morphtypes": sharedgrammaticalinfo_morphtypes, "sensecontents": sensecontents})

    return results

def sanitize_token(token):
    if not isinstance(token, str):
        return token
    token = re.sub(r"\s*\([^)]*\)", "", token)
    return token.replace(",", ";").strip();

def prepare_data_for_csv(data, fieldnames, sense):    
    result = []
    for key, value in data.items():
        for index in range(0, len(value)):
            
            for indexS in range(0, len(value[index]['sensecontents'])):
                if sense == 0:
                    array_lang_items = sanitize_token(value[index]['sensecontents'][indexS]['definition_en']).split(';')
                    for item_lang in array_lang_items:
                        result.append({'ngiemboon':sanitize_token(value[index]['noun']), 'en':sanitize_token(item_lang)})
                else:
                    array_lang_items = sanitize_token(value[index]['sensecontents'][indexS]['definition_en']).split(';')
                    for item_lang in array_lang_items:
                        result.append({'en':sanitize_token(item_lang), 'ngiemboon':sanitize_token(value[index]['noun'])})
                for indexY in range(0, len(value[index]['sensecontents'][indexS]['examples'])):
                    if sense == 0:
                        result.append({'ngiemboon':sanitize_token(value[index]['sensecontents'][indexS]['examples'][indexY]['dialect']), 'en':sanitize_token(value[index]['sensecontents'][indexS]['examples'][indexY]['en'])})
                    else:
                        result.append({ 'en':sanitize_token(value[index]['sensecontents'][indexS]['examples'][indexY]['en']), 'ngiemboon':sanitize_token(value[index]['sensecontents'][indexS]['examples'][indexY]['dialect'])})
            #append({fieldnames[0]:value['noun'], fieldnames[1]: value['sensecontents']['definition_en']})

    return result

# ---- Dump (save) to UTF-8 text file ----
def save_file(data, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---- Later, load (recover) it back ----
def recover_file(file):
    recovered_data = []
    with open(file, "r", encoding="utf-8") as f:
        recovered_data = json.load(f)

    return recovered_data


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
endOfPagingText = "No entries exist starting with this letter."
directory = "english_to_ngiemboon/"
urlBase = "https://www.webonary.org/ngiemboon/browse/?letter=[letter]&key=en&totalEntries=89&lang=nnh&pagenr=[page]"
urlBase = "https://www.webonary.org/ngiemboon/browse/browse-english/?letter=[letter]&key=en&totalEntries=382&pagenr=[page]&lang=en"
data = {}
fileCompile = []
compteur = 0

for letter in letters:
    urlLetter = urlBase.replace("[letter]", letter)

    for page in range(1, 500):

        url = urlLetter.replace("[page]", str(page))
        print(url)
        temp = extract_dictionnary_text(url, True)
        #print(len(temp))
        if len(temp)==0:
            break;
        compteur = compteur + 1
        save_file(temp, directory + str(compteur) + "_" + letter + "_" + str(page) + ".txt" )
        data[url] = temp
        fileCompile.append(str(compteur) + ") "+ url +" $ ")
        time.sleep(5)
save_file(fileCompile, "english_to_ngiemboon.txt" )