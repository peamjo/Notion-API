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
from notion_functions import *
from property_exceptions import (city_exceptions, country_exceptions,
                                 job_exception)
from wiki_scraping_final import wiki_scrape_bot
from wikipedia_summary import wiki_summary


def get_info(data_from_wiki, person_name, url):
    person_info_list = [[person_name]]    
    us_states, flags_final = load_states_and_flags_dict()

    for counter, property in enumerate(data_from_wiki):
        if property[0] == "Died":
            death_date = split_brackets(property[1])
            person_info_list.append(['Died', death_date])
            person_info_list.append(['YoD', death_date.split("-",1)[0]])
        if property[0] == "Born":
            birth_date = split_brackets(property[1])
            if (data_from_wiki[counter+1])[0] == "Died":
                find_digit = re.findall(r'\d', property[1])
                last_num = find_digit[-1]
                segment_1 = property[1].split(last_num)
            else:
                segment_1 = property[1].split(')')
            person_info_list.append(['Birthday', birth_date])
            person_info_list.append(['YoB', birth_date.split("-",1)[0]])
            location = segment_1[-1]     
            final_location = location.split(',')
            if len(final_location) >= 3:       
                city, state, country = get_location(person_info_list, final_location)
            else:
                city, country = get_location(person_info_list, final_location)
        if property[0] == "Origin":
            location = property[1] 
            final_location = location.split(',')
            if len(final_location) >= 3:       
                city, state, country = get_location(person_info_list, final_location)
            else:
                city, country = get_location(person_info_list, final_location)
        if len(person_info_list)>1:
            if (person_info_list[-1])[1] == 'USA':
                if len(final_location)>2:
                    for key in us_states:                    
                        if key == state:
                            (person_info_list[-2])[1] = us_states[key]
            for key in flags_final:
                if flags_final[key] == (person_info_list[-1])[1]:
                    person_info_list.append(['Flag', key])
        if property[0] in ("Occupations", 'Occupation', "Occupation(s)"):
            person_info_list.append(['Occupations', property[1]])
        if property[0] == "Genres":
            person_info_list.append(['Genres (Music)', property[1]])
        if property[0] in ("Instruments", "Instrument(s)"):
            person_info_list.append(['Instrument(s)', property[1]])
        if property[0] == "Movement":
            person_info_list.append(['Art Style/Movement', property[1]])
        if property[0] in ("Years active", "Turned pro"):
            property[1]= split_hyphens(property[1])
            person_info_list.append(['Years active', property[1]])
        if property[0] == "Retired":
            person_info_list.append(['Retired', property[1]])
    person_info_list.append(['Wiki', url])
    return(person_info_list)

def get_gender_and_ethnicity(person):
    gender_for_each_pic_list = []
    ethnicity_for_each_pic_list = []
    for counter in range(1,6):
        link = str(Path.cwd().joinpath('download',rf'{person} face',rf'Image_{counter}.jpg'))
        gender_count, ethnicity_count = face_recognition(link)
        gender_for_each_pic_list.append(gender_count)
        ethnicity_for_each_pic_list.append(ethnicity_count)
    return (gender_for_each_pic_list, ethnicity_for_each_pic_list)

def edit_person_data(notion_pages, person_name, person_info_list):
    for page in notion_pages:
        page_id = page["id"]
        query_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        if query_name == person_name:
            city_added = False
            state_added = False
            for property in person_info_list:
                if property[0] == 'Birthday':
                    add_date(page, "Date", property)
                    birth = property[1]
                if property[0] == 'Died':
                    update_data = {"Date": {"date": {"start": birth, "end": property[1]}}}
                    update_page(page, update_data)
                if property[0] == 'YoB': add_number(page, "YoB", property)
                if property[0] == 'YoD': add_number(page, "YoD", property)
                if property[0] == 'Years active': add_text(page, 'Years active', property)
                if property[0] == 'Country': add_multiselect(page,"Country", property)
                if property[0] == 'City/Region' and city_added == False:
                    add_multiselect(page,"City/Region", property)
                    city = property[1]
                    city_added = True
                if property[0] == 'State' and state_added == False:
                    property[1] = [city] + [property[1]]
                    add_multiselect(page,"City/Region", property)
                    state_added = True
                if property[0] == 'Gender': add_multiselect(page, "Gender", property)
                if property[0] == 'Ethnicity': add_multiselect(page,"Ethnicity", property)
                if property[0] == 'Flag': add_emoji(page, property)
                if property[0] == 'Occupations': add_multiselect(page, "Job(s)", property)
                if property[0] == 'Wiki': add_url(page, "Wiki", property)
                if property[0] == 'Genres (Music)': add_multiselect(page, "Genre (Music)", property)
                if property[0] == 'Instrument(s)': add_multiselect(page, "Instrument(s)", property)
                if property[0] == 'Art Style/Movement': add_multiselect(page, "Art Style/Movement", property)
            summary = wiki_summary(person_name)    
            try:
                if len(summary) > 1300:
                    summary = summary[:1300]
                    last_period = summary.rfind('.')
                    summary = summary[:last_period+1]
                update_data = summary
                create_content(page_id, update_data)
            except:
                pass

def add_or_edit_notion_person(people_list):
    load_dotenv()
    database_id = os.getenv("EXAMPLE_PEOPLE_DATABASE_ID")
    jobs = []
    error_list = []

    for person in people_list:
        try:
            person_name, url, person_property_name = process_input(person)
            data_from_wiki = wiki_scrape_bot(url)
            person_info_list = get_info(data_from_wiki, person_name, url)
            if jobs != []:
                add_or_check_jobs_list(person_info_list, jobs)
            get_images(person_name)
            convert_to_jpg(person_name)
            gender_for_each_pic_list, ethnicity_for_each_pic_list = get_gender_and_ethnicity(person_name)
            gender, ethnicity = majority_race_gender(gender_for_each_pic_list, ethnicity_for_each_pic_list)
            person_info_list.append(["Gender", gender])
            person_info_list.append(["Ethnicity", ethnicity])
            print("Final List: ", person_info_list)
            notion_pages = add_or_check_pages(database_id, person_name, person_property_name)
            edit_person_data(notion_pages, person_name, person_info_list)
        except KeyboardInterrupt:
            break
        except:
            error_list.append(person)
            continue
    
    if error_list != []:
        print("Error List:", error_list)

add_or_edit_notion_person(["Louis Tomlinson"])
