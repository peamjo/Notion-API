import requests
import string
import unicodedata
import json
import wordninja
import gzip
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from property_exceptions import data_list_exception

def wiki_scrape_bot(url):
    url_open = requests.get(url)
    soup = BeautifulSoup(url_open.content, 'html.parser')
    details = soup('table', {'class': 'infobox'})
    data_list = []
    with open(str(Path.cwd().joinpath('wikipedia','lang_database.txt')), 'rb') as f_in:
         with gzip.open('lang_database.txt.gz', 'wb') as f_out:
             shutil.copyfileobj(f_in, f_out)
    wordninja.DEFAULT_LANGUAGE_MODEL = wordninja.LanguageModel('lang_database.txt.gz')
    with open(str(Path.cwd().joinpath('wikipedia','og_lang_database.txt')), 'rb') as f_in:
         with gzip.open('og_lang_database.txt.gz', 'wb') as f_out:
             shutil.copyfileobj(f_in, f_out)
    og_list_split = wordninja.LanguageModel(str(Path.cwd().joinpath('og_lang_database.txt.gz')))
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
        if i[0] in ("Occupations", "Occupation", "Occupation(s)", "Genre", "Genres", "Instruments", "Instrument(s)", "Movement"):
            i[1]=i[1].replace(" ","")
            i[1] = wordninja.split(i[1])
            for j in range(len(i[1])):
                list_property = (i[1])[j]
                list_property = og_list_split.split(list_property)
                out = map(lambda x:x.capitalize(), list_property)
                list_property = list(out)
                list_property = (' '.join(list_property))
                (i[1])[j] = data_list_exception(list_property)

    return (data_list)
