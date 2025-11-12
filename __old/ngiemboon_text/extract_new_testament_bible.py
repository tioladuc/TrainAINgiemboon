from bs4 import BeautifulSoup
import requests
import csv
import os
import pickle


def append_associativeOld(arr, keyA, valueA, keyB, valueB):
    if len(valueA) < 100 and len(valueB) < 100 :
        arr.append({keyA:valueA, keyB: valueB})
    
    return arr

    if '?' in valueA and '?' in valueB :
        valueATMP = valueA.split('?')
        valueBTMP = valueB.split('?')
        for i in range(len(valueATMP)):
            append_associative(arr, keyA, valueATMP[i], keyB, valueBTMP[i])

    if '!' in valueA and '!' in valueB :
        valueATMP = valueA.split('!')
        valueBTMP = valueB.split('!')
        for i in range(len(valueATMP)):
            append_associative(arr, keyA, valueATMP[i], keyB, valueBTMP[i])

    
    arr.append({keyA:valueA, keyB: valueB})

    return arr

def prepare_data_for_csv(data, fieldnames):    
    result = []
    for key, value in data.items():
        for index in range(0, len(value)):
            
            for indexS in range(0, len(value[index]['sensecontents'])):
                result.append({'ngiemboon':value[index]['noun'], 'en':value[index]['sensecontents'][indexS]['definition_en']})
                for indexY in range(0, len(value[index]['sensecontents'][indexS]['examples'])):
                    result.append({'ngiemboon':value[index]['sensecontents'][indexS]['examples'][indexY]['dialect'], 'en':value[index]['sensecontents'][indexS]['examples'][indexY]['en']})
            #append({fieldnames[0]:value['noun'], fieldnames[1]: value['sensecontents']['definition_en']})

    return result

def save_data_as_csv_ngiemboon_to_english(data, fieldnames):
    # Specify the output file name
    filename = 'data/mardi_newtestament_ngiemboon_to_english.csv'

    # Open the file in write mode ('w')
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)

def save_data_as_csv_english_to_ngiemboon(data, fieldnames):
    # Specify the output file name
    filename = 'data/mardi_newtestament_english_to_ngiemboon.csv'

    # Open the file in write mode ('w')
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)






def extract_bible_text(source, from_url=True):
    # Load HTML
    if from_url:
        html = requests.get(source).text
    else:
        with open(source, encoding="utf-8") as f:
            html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    chapter_div = soup.find("div", {"data-testid": "chapter-content"})
    if not chapter_div:
        return {} #raise ValueError("No div with data-testid='chapter-content' found.")

    results = {}
    # Find all span elements with a data-usfm attribute
    for verse_span in chapter_div.find_all("span", attrs={"data-usfm": True}):
        usfm_key = verse_span["data-usfm"]

        # Collect all descendant span text with class ChapterContent_content__RrUqA
        contents = verse_span.find_all("span", class_="ChapterContent_content__RrUqA")
        verse_text = "".join(c.get_text(strip=True) for c in contents)

        # Only store non-empty verses
        if verse_text.strip():
            results[usfm_key] = verse_text

    return results

def append_associative(arr, keyA, valueA, keyB, valueB):
    #if len(valueA) < 100 and len(valueB) < 100 :
    arr.append({keyA:valueA, keyB: valueB})
    return arr
    #print('*****************************************************')
    #print(valueA + ' 9999999999')
    #print(valueB + ' 7777777777')
    if '?' in valueA and '?' in valueB :
        valueATMP = valueA.split('?')
        valueBTMP = valueB.split('?')
        if len(valueATMP) != len(valueBTMP):
            valueA = valueA.strip()
            valueB = valueB.strip()
            if valueA.endswith("?"):
                valueA = valueA[:-1]
            if valueB.endswith("?"):
                valueB = valueB[:-1]
            valueATMP = valueA.split('?')
            valueBTMP = valueB.split('?')
        #print(str( len(valueATMP) ) + ' ======')
        #print(str( len(valueBTMP) ) + ' ======')
        for i in range(len(valueATMP)):
            arr = append_associative(arr, keyA, valueATMP[i], keyB, valueBTMP[i])
        return arr

    if '!' in valueA and '!' in valueB :
        valueATMP = valueA.split('!')
        valueBTMP = valueB.split('!')
        if len(valueATMP) != len(valueBTMP):
            valueA = valueA.strip()
            valueB = valueB.strip()
            if valueA.endswith("!"):
                valueA = valueA[:-1]
            if valueB.endswith("!"):
                valueB = valueB[:-1]
            valueATMP = valueA.split('!')
            valueBTMP = valueB.split('!')
        #print(str( len(valueATMP) ) + ' ----')
        #print(str( len(valueBTMP) ) + ' ----')
        for i in range(len(valueATMP)):
            arr = append_associative(arr, keyA, valueATMP[i], keyB, valueBTMP[i])
        return arr

    
    arr.append({keyA:valueA, keyB: valueB})

    return arr


def extract_bible_website_array_data():
    dictionnaryEnglish = ["https://www.bible.com/fr/bible/1/MAT.[-].KJV",
                        "https://www.bible.com/fr/bible/1/MRK.[-].KJV",
                        
                        "https://www.bible.com/fr/bible/1/LUK.[-].KJV",
                        "https://www.bible.com/fr/bible/1/JHN.[-].KJV",
                        "https://www.bible.com/fr/bible/1/ACT.[-].KJV",
                        "https://www.bible.com/fr/bible/1/ROM.[-].KJV",
                        "https://www.bible.com/fr/bible/1/1CO.[-].KJV",
                        "https://www.bible.com/fr/bible/1/2CO.[-].KJV",
                        "https://www.bible.com/fr/bible/1/GAL.[-].KJV",
                        "https://www.bible.com/fr/bible/1/EPH.[-].KJV",
                        "https://www.bible.com/fr/bible/1/PHP.[-].KJV",
                        "https://www.bible.com/fr/bible/1/COL.[-].KJV",
                        "https://www.bible.com/fr/bible/1/1TH.[-].KJV",
                        "https://www.bible.com/fr/bible/1/2TH.[-].KJV",
                        "https://www.bible.com/fr/bible/1/1TI.[-].KJV",
                        "https://www.bible.com/fr/bible/1/2TI.[-].KJV",
                        "https://www.bible.com/fr/bible/1/TIT.[-].KJV",
                        "https://www.bible.com/fr/bible/1/PHM.[-].KJV",
                        "https://www.bible.com/fr/bible/1/HEB.[-].KJV",
                        
                        "https://www.bible.com/fr/bible/1/JAS.[-].KJV",
                        "https://www.bible.com/fr/bible/1/1PE.[-].KJV",
                        "https://www.bible.com/fr/bible/1/2PE.[-].KJV",
                        "https://www.bible.com/fr/bible/1/1JN.[-].KJV",
                        "https://www.bible.com/fr/bible/1/2JN.[-].KJV",
                        "https://www.bible.com/fr/bible/1/3JN.[-].KJV",
                        "https://www.bible.com/fr/bible/1/JUD.[-].KJV",
                        "https://www.bible.com/fr/bible/1/REV.[-].KJV",
                        ]
    dictionnaryDialect = ["https://www.bible.com/fr/bible/299/MAT.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/MRK.[-].NGBM",
                        
                        "https://www.bible.com/fr/bible/299/LUK.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/JHN.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/ACT.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/ROM.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/1CO.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/2CO.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/GAL.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/EPH.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/PHP.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/COL.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/1TH.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/2TH.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/1TI.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/2TI.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/TIT.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/PHM.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/HEB.[-].NGBM",
                        
                        "https://www.bible.com/fr/bible/299/JAS.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/1PE.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/2PE.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/1JN.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/2JN.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/3JN.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/JUD.[-].NGBM",
                        "https://www.bible.com/fr/bible/299/REV.[-].NGBM",
                        ]

    fileA = 'bible_global.pkl'
    fileB = 'bible_english_to_ngiemboon.pkl'
    fileC = 'bible_ngiemboon_to_english.pkl'
    
    globalDataCSV = {}
    globalDataCsv_english_to_ngiemboon = []
    globalDataCsv_ngiemboon_to_english = []

    if os.path.exists(fileA):
        with open(fileA, "rb") as file:
            globalDataCSV = pickle.load(file)
        with open(fileB, "rb") as file:
            globalDataCsv_english_to_ngiemboon = pickle.load(file)
        with open(fileC, "rb") as file:
            globalDataCsv_ngiemboon_to_english = pickle.load(file)

    else :        
        i = 0
        while i < len(dictionnaryEnglish):
            urlEnglishBase = dictionnaryEnglish[i] 
            urlDialectBase = dictionnaryDialect[i] 
            i += 1
            
            for chapter in range(1, 2000):  
                urlEnglish = urlEnglishBase.replace("[-]", str(chapter))
                urlDialect = urlDialectBase.replace("[-]", str(chapter))
                
                versesEnglish = extract_bible_text(urlEnglish, from_url=True)
                versesDialect = extract_bible_text(urlDialect, from_url=True)
                if( len(versesEnglish) == 0 ):
                    break
                print( len(versesEnglish), "=>", len(versesDialect), " ::: ", urlEnglish, "=>", urlDialect)
                top = 1
                for k, v in versesDialect.items():
                    if(k in versesEnglish):
                        #print(top)
                        top = top +1
                        globalDataCSV[k] = v + "****" + versesEnglish[k]
                        globalDataCsv_ngiemboon_to_english = append_associative(globalDataCsv_ngiemboon_to_english, 'ngiemboon', v, 'en', versesEnglish[k])# + ' # ' + urlEnglish + ' #' + str(top-1))
                        #globalDataCsv_ngiemboon_to_english.append({'ngiemboon': v, 'en': versesEnglish[k]})
                        globalDataCsv_english_to_ngiemboon = append_associative(globalDataCsv_english_to_ngiemboon, 'en', versesEnglish[k], 'ngiemboon', v)
                        #globalDataCsv_english_to_ngiemboon.append({'en': versesEnglish[k], 'ngiemboon': v})

        with open(fileA, "wb") as file:
            pickle.dump(globalDataCSV, file)
        with open(fileB, "wb") as file:
            pickle.dump(globalDataCsv_english_to_ngiemboon, file)
        with open(fileC, "wb") as file:
            pickle.dump(globalDataCsv_ngiemboon_to_english, file)
        
    return [globalDataCSV, globalDataCsv_english_to_ngiemboon, globalDataCsv_ngiemboon_to_english]

# Example 1 — from live site
##urlEnglish = "https://www.bible.com/fr/bible/1/MAT.122.KJV" 
##urlDialect = "https://www.bible.com/fr/bible/299/MAT.122.NGBM"
##versesEnglish = extract_bible_text(urlEnglish, from_url=True)
##versesDialect = extract_bible_text(urlDialect, from_url=True)


globalDataCSV = {}
globalDataCsv_english_to_ngiemboon = []
globalDataCsv_ngiemboon_to_english = []

tmpData = extract_bible_website_array_data()

globalDataCSV = tmpData[0]
globalDataCsv_english_to_ngiemboon = tmpData[1]
globalDataCsv_ngiemboon_to_english = tmpData[2]

fieldnames = ['ngiemboon', 'en']
fieldnamesX = [ 'en', 'ngiemboon']
globalDataCsv_english_to_ngiemboonTop =[]
globalDataCsv_ngiemboon_to_englishTop = []
for item in globalDataCsv_english_to_ngiemboon:
    if len(item['en']) < 120 and len(item['ngiemboon']) < 120:
        globalDataCsv_english_to_ngiemboonTop.append(item)
for item in globalDataCsv_ngiemboon_to_english:
    if len(item['en']) < 120 and len(item['ngiemboon']) < 120:
        globalDataCsv_ngiemboon_to_englishTop.append(item)
save_data_as_csv_english_to_ngiemboon(globalDataCsv_english_to_ngiemboonTop, fieldnamesX)
save_data_as_csv_ngiemboon_to_english(globalDataCsv_ngiemboon_to_englishTop, fieldnames)
# save_data_as_csv(globalDataCsvBeta, fieldnames)
print("FIN")
    
