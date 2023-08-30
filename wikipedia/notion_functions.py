import json
import os
import re
import string
from pathlib import Path

from add_to_notion import (add_date, add_emoji, add_multiselect, add_number,
                           add_select, add_text, add_url)
from dotenv import load_dotenv
from face_recognition import face_recognition, majority_race_gender
from final_transfer import create_content, create_page, update_page
from get_images import convert_to_jpg, get_images
from import_requests import get_pages
from property_exceptions import (city_exceptions, country_exceptions,
                                 job_exception)
from wiki_scraping_final import wiki_scrape_bot
from wikipedia_summary import wiki_summary


def process_names(name):
    if name[:2] in ("DJ", "dj"):
        person_name = "DJ " + string.capwords(name).split(" ",1)[1]
    else:
        person_name = string.capwords(name)
    lists = person_name.split()
    word = "_".join(lists)
    url = "https://en.wikipedia.org/wiki/" + word
    person_property_name = {
        "Name": {"title": [{"text": {"content": person_name}}]},
    }
    return person_name, url, person_property_name

def split_brackets(property):
    segment_1 = property[1].split('(', 1)
    segment_2 = segment_1[1].split(')', 1)
    date = segment_2[0]
    return(date)

def split_hyphens(property):
    segment_1 = property[1].replace('-', 'to').replace('–', 'to')
    segment_1 = segment_1.split("to")
    date = segment_1[0] + " to " + segment_1[-1]
    return(date)

def load_states_and_flags_dict():
    with open(str(Path.cwd().joinpath('wikipedia','us_states.txt')), encoding="utf8") as f:
        data_from_wiki = f.read().replace("'",'"')
    us_states = json.loads(data_from_wiki)
    with open(str(Path.cwd().joinpath('wikipedia','flags.txt')), encoding="utf8") as f:
        data_from_wiki = f.read().replace("'",'"')
    flags_final = json.loads(data_from_wiki)
    return us_states, flags_final

def add_or_check_jobs(person_info_list, job):
    counter = 0
    for property in person_info_list:
        if property[0] == "Occupations":
            for counter in job:
                if counter not in property[1]: 
                    property[1].append(counter)
            break
        else: counter+=1
    if counter == len(person_info_list):
        person_info_list.append(['Occupations', job])

def add_or_check_pages(database_id, person_property_name, person_name):
    pages = get_pages(database_id)
    exist = False
    for page in pages:
        existed_page_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        if existed_page_name == person_name:
            exist = True
    if exist == False:
        create_page(person_property_name, database_id)
        pages = get_pages(database_id)
    return(pages)

def get_location(person_info_list, final_location):
    if len(final_location) > 3:
        final_location.pop(0)
    if len(final_location) == 3:
        city = final_location[0]
        city = city_exceptions(city)
        state = final_location[1].replace(' ','',1)
        country = final_location[2].replace(' ','',1)
        country = country_exceptions(country)
        person_info_list.append(['City/Region', city])
        person_info_list.append(['State', state])
        person_info_list.append(['Country', country])
        return city, state, country
    elif len(final_location) == 2:
        city = final_location[0]
        city = city_exceptions(city)
        country = final_location[1].replace(' ','',1)
        country = country_exceptions(country)
        person_info_list.append(['City/Region', city])
        person_info_list.append(['Country', country])
        return city, country
