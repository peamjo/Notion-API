import json
import os
import re
import string
from pathlib import Path

from edit_overwrite_notion import *
from face_recognition import face_recognition, majority_race_gender
from final_transfer import create_page, update_page
from get_images import convert_to_jpg, get_images
from import_requests import get_pages
from property_exceptions import (city_exceptions, country_exceptions,
                                 job_exception)
from wiki_scraping_final import wiki_scrape_bot
from wikipedia_summary import wiki_summary


def process_input(input):
    if input[:2] in ("DJ", "dj"):
        processsed_input = "DJ " + string.capwords(input).split(" ",1)[1]
    else:
        processsed_input = string.capwords(input)
    lists = processsed_input.split()
    word = "_".join(lists)
    url = "https://en.wikipedia.org/wiki/" + word
    property_input = {
        "Name": {"title": [{"text": {"content": processsed_input}}]},
    }
    return processsed_input, url, property_input

def split_brackets(input):
    segment_1 = input.split('(', 1)
    segment_2 = segment_1[1].split(')', 1)
    output = segment_2[0]
    return output

def split_hyphens(input):
    segment_1 = input.replace('-', 'to').replace('–', 'to')
    segment_1 = segment_1.split("to")
    output = segment_1[0] + " to " + segment_1[-1]
    return output

def load_states_and_flags_dict():
    with open(str(Path.cwd().joinpath('wikipedia','us_states.txt')), encoding="utf8") as f:
        us_states_dict = f.read().replace("'",'"')
    us_states = json.loads(us_states_dict)
    with open(str(Path.cwd().joinpath('wikipedia','flags.txt')), encoding="utf8") as f:
        flags_dict = f.read().replace("'",'"')
    flags_final = json.loads(flags_dict)
    return us_states, flags_final

def add_or_check_jobs_list(list, jobs):
    counter = 0
    for property in list:
        if property[0] == "Occupations":
            for job in jobs:
                if job not in property[1]: 
                    property[1].append(job)
            break
        else: counter+=1
    if counter == len(list):
        list.append(['Occupations', jobs])

def check_pages(database_id, notion_pages, processsed_input, topic):
    exist = False
    for page in notion_pages:
        existing_page_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        if existing_page_name == processsed_input:
            exist = True
    return exist

def get_location(list, final_location):
    if len(final_location) > 3:
        final_location.pop(0)
    if len(final_location) == 3:
        city = final_location[0]
        city = city_exceptions(city)
        state = final_location[1].replace(' ','',1)
        country = final_location[2].replace(' ','',1)
        country = country_exceptions(country)
        list.append(['City/Region', city])
        list.append(['State', state])
        list.append(['Country', country])
        return city, state, country
    elif len(final_location) == 2:
        city = final_location[0]
        city = city_exceptions(city)
        country = final_location[1].replace(' ','',1)
        country = country_exceptions(country)
        list.append(['City/Region', city])
        list.append(['Country', country])
        return city, country
