import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import csv


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

def save_data_as_csv(data, fieldnames):
    # Specify the output file name
    filename = 'languages_bible.csv'

    # Open the file in write mode ('w')
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)



my_dict = {}
my_dictBeta = {}

# --- Fetch HTML from the URL ---
urlBase = "https://www.bible.com/fr/bible/299/MAT.[-].NGBM"
urlBase = "https://www.bible.com/fr/bible/104/MAT.[-].NBS"

for i in range(1, 5):  
	url = urlBase.replace("[-]", str(i))
	print(i, " => ", url)
	response = requests.get(url)
	response.raise_for_status()
	html = response.text

	# --- Parse HTML ---
	soup = BeautifulSoup(html, "html.parser")

	# Find the chapter content container
	chapter_div = soup.find("div", {"data-testid": "chapter-content"})
	if not chapter_div:
		break 
		#raise ValueError("No div with data-testid='chapter-content' found")

	# Dictionary to group text by data-usfm value
	grouped_texts = defaultdict(str)

	# Iterate over spans in the chapter
	for span in chapter_div.find_all("span", attrs={"data-usfm": True}):
		# Skip verse number or label spans
		if "ChapterContent_label__R2PLt" in span.get("class", []):
			continue
		if "ChapterContent_note__YlDW0" in span.get("class", []):
			continue

		data_usfm = span["data-usfm"]
		text = span.get_text(strip=True)
		grouped_texts[data_usfm] += (" " + text)
	
	for usfm, text in grouped_texts.items():
		parts = usfm.split('.')
		startPart = len(parts[ len(parts) -1 ])+1
		my_dictBeta[usfm] = text[ startPart: ]
	#my_dict[url] = grouped_texts


# --- Print results ---
for usfm, text in my_dictBeta.items():
	print(usfm, "=>", text.strip())


#for url, myDictionnairy in my_dict.items():
#	print(url)
    #for usfm, text in myDictionnairy.items():
	#	print(usfm, "=>", text.strip())
