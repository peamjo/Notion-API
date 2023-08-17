import requests
import string
import unicodedata
import json
import wordninja
import gzip
import shutil
from bs4 import BeautifulSoup
"""
Enter_input = input("Search: ")
u_i = string.capwords(Enter_input)
lists = u_i.split()
word = "_".join(lists)

url = "https://en.wikipedia.org/wiki/" + word
"""

def wiki_scrape_bot(url):
    url_open = requests.get(url)
    soup = BeautifulSoup(url_open.content, 'html.parser')
    details = soup('table', {'class': 'infobox'})
    data_list = []
    #with open('lang_database.txt', 'rb') as f_in:
    #    with gzip.open('lang_database.txt.gz', 'wb') as f_out:
    #        shutil.copyfileobj(f_in, f_out)
    #wordninja.DEFAULT_LANGUAGE_MODEL = wordninja.LanguageModel('lang_database.txt.gz')
    for i in details:
        rows = i.find_all('tr')
        for row in rows:
            header = row.find_all('th')
            data = row.find_all('td')
            if header is not None and data is not None:
                for x,y in zip(header,data):
                    normalized_x = unicodedata.normalize('NFKC',x.text).replace('\u200b', '').replace('\n', '')
                    normalized_y = unicodedata.normalize('NFKC',y.text).replace('\u200b', '').replace('\n', '')
                    for z in normalized_y:
                        segment_1 = normalized_y.split('[')
                        if len(segment_1) > 1:
                            segment_2 = segment_1[1].split(']')
                            new_y = segment_1[0]+segment_2[1]
                            data_list.append([normalized_x, new_y])
                        else:
                            data_list.append([normalized_x, normalized_y])
                        break
    for i in data_list:
        if i[0] == "Occupations" or i[0] == "Occupation" or i[0] == "Occupation(s)" or i[0] == "Genres":
            i[1] = wordninja.split(i[1])
            for j in range(len(i[1])):
                new = ((i[1])[j]).capitalize()
                if new == "Dj":
                    new = "DJ"
                (i[1])[j] = new
    #print (data_list)
    return (data_list)

#wikibot(url)
