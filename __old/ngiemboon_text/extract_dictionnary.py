from bs4 import BeautifulSoup
import requests
import csv
import re
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
    base_pattern = line_dictionnary.find("span", class_="mainheadword").find("a")
    if base_pattern :
        return base_pattern.get_text()
    return ""

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
        definition_en = extract_span_text_from_class(sense, "definitionorgloss_1")
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
        print("==============**********")
        print(token)
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

def save_data_as_csv_ngiemboon_to_english(data, fieldnames):
    # Specify the output file name
    filename = 'vendredi_dicto_ngiemboon_to_english.csv'

    # Open the file in write mode ('w')
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)
    print('duclair')

def save_data_as_csv_english_to_ngiemboon(data, fieldnames):
    # Specify the output file name
    filename = 'vendredi_dicto_english_to_ngiemboon.csv'

    # Open the file in write mode ('w')
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)
    print('duclair')


letters = ['a','b','c','e','ɛ','f','g','h','j','k','l','m','n','ŋ','o','ɔ','p','s','t','u','v','w','y','z']
endOfPagingText = "No entries exist starting with this letter."

urlBase = "https://www.webonary.org/ngiemboon/browse/?letter=[letter]&key=nnh&totalEntries=89&lang=en&pagenr=[page]"
data = {}

for letter in letters:
    urlLetter = urlBase.replace("[letter]", letter)

    for page in range(1, 100):
        url = urlLetter.replace("[page]", str(page))
        print(url)
        temp = extract_dictionnary_text(url, True)
        #print(len(temp))
        if len(temp)==0:
            break;
        data[url] = temp

fieldnames = ['ngiemboon', 'en']
fieldnamesB = [ 'en', 'ngiemboon']
print('-------------------------------------------------------------')
print(data)
print('-------------------------------------------------------------')

prepared_data_ngiemboon_to_english = prepare_data_for_csv(data, fieldnames, 0)
prepared_data_english_to_ngiemboon = prepare_data_for_csv(data, fieldnamesB, 1)
# remove couple having an element that is empty
prepared_data_ngiemboon_to_english = [item for item in prepared_data_ngiemboon_to_english if item.get('ngiemboon') and item.get('en')]
prepared_data_english_to_ngiemboon = [item for item in prepared_data_english_to_ngiemboon if item.get('ngiemboon') and item.get('en')]
# Remove duplicates
prepared_data_ngiemboon_to_english = [dict(t) for t in {tuple(sorted(d.items())) for d in prepared_data_ngiemboon_to_english}]
prepared_data_english_to_ngiemboon = [dict(t) for t in {tuple(sorted(d.items())) for d in prepared_data_english_to_ngiemboon}]
# descending order
prepared_data_ngiemboon_to_english = sorted(prepared_data_ngiemboon_to_english, key=lambda item: len(item.get('ngiemboon', '')))
prepared_data_english_to_ngiemboon = sorted(prepared_data_english_to_ngiemboon, key=lambda item: len(item.get('ngiemboon', '')))

save_data_as_csv_ngiemboon_to_english(prepared_data_ngiemboon_to_english, fieldnames)
save_data_as_csv_english_to_ngiemboon(prepared_data_english_to_ngiemboon, fieldnamesB)
print(prepared_data_english_to_ngiemboon)
print("FIN")
    
