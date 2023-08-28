import re
import json
import string
from pathlib import Path
from import_requests import get_pages
from dotenv import load_dotenv
import os
from wikipedia_summary import wiki_summary
from property_exceptions import city_exceptions, country_exceptions, job_exception
from wiki_scraping_final import wiki_scrape_bot
from get_images import get_images, convert_to_jpg
from final_transfer import update_page, create_page, create_content
from face_recognition import face_recognition, majority_race_gender
from add_to_notion import add_text, add_number, add_select, add_multiselect, add_url, add_emoji, add_date

load_dotenv()
database_id = os.getenv("EXAMPLE_PEOPLE_DATABASE_ID")

#input_name = input_names("Search: ")
def input_names(input_name):
    if input_name[:2] != "DJ":
        name = string.capwords(input_name)
    else:
        name = "DJ " + string.capwords(input_name).split(" ",1)[1]
    lists = name.split()
    word = "_".join(lists)
    url = "https://en.wikipedia.org/wiki/" + word
    property_name = {
        "Name": {"title": [{"text": {"content": name}}]},
    }
    return name, url, property_name

def get_info(individual, data, name, url):
    info = [[name]]    
    us_states, flags_final = load_dict()

    for counter, property in enumerate(data):
        if property[0] == "Died":
            death_date = split_brackets(property)
            info.append(['Died', death_date])
            update_data = {"Date": {"date": {"start": birth, "end": property[1]}}}
            update_page(page, update_data)
            info.append(['YoD', death_date.split("-",1)[0]])
            add_number(page, "YoD", property)
        if property[0] == "Born":
            birth_date = split_brackets(property)
            if (data[counter+1])[0] == "Died":
                find_digit = re.findall(r'\d', property[1])
                last_num = find_digit[-1]
                segment_1 = property[1].split(last_num)
            else:
                segment_1 = property[1].split(')')
            info.append(['Birthday', birth_date])
            add_date(page, "Date", property)
            info.append(['YoB', birth_date.split("-",1)[0]])
            add_number(page, "YoB", property)
            location = segment_1[-1]     
            final_location = location.split(',')
            if len(final_location) >= 3:       
                city, state, country = get_location(info, final_location)
            else:
                city, country = get_location(info, final_location)
        if property[0] == "Origin":
            location = property[1] 
            final_location = location.split(',')
            if len(final_location) >= 3:       
                city, state, country = get_location(info, final_location)
            else:
                city, country = get_location(info, final_location)
        if len(info)>1:
            if (info[-1])[1] == 'USA':
                if len(final_location)>2:
                    for key in us_states:                    
                        if key == state:
                            (info[-2])[1] = us_states[key]
            for key in flags_final:
                if flags_final[key] == (info[-1])[1]:
                    info.append(['Flag', key])
                    add_emoji(page, property)
        if property[0] in ("Occupations", 'Occupation', "Occupation(s)"):
            info.append(['Occupations', property[1]])
            add_multiselect(page, "Job(s)", property)
        if property[0] == "Genres":
            info.append(['Genres (Music)', property[1]])
            add_multiselect(page, "Genres (Music)", property)
        if property[0] in ("Instruments", "Instrument(s)"):
            info.append(['Instrument(s)', property[1]])
            add_multiselect(page, "Instrument(s)", property)
        if property[0] == "Movement":
            info.append(['Art Style/Movement', property[1]])
            add_multiselect(page, "Art Style/Movement", property)
        if property[0] in ("Years active", "Turned pro"):
            property[1]= split_hyphens(property)
            add_text(page, 'Years active', property)
            info.append(['Years active', property[1]])
        if property[0] == "Retired":
            info.append(['Retired', property[1]])
        info.append(['Wiki', url])
        add_url(page, "Wiki", property)
        summary = wiki_summary(name)
        try:
            if len(summary) > 1300:
                summary = summary[:1300]
                last_period = summary.rfind('.')
                summary = summary[:last_period+1]
            update_data = wiki_summary(name)
            create_content(page_id, update_data)
        except:
            pass
    return(info)

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

def load_dict():
    with open(str(Path.cwd().joinpath('wikipedia','us_states.txt')), encoding="utf8") as f:
        data = f.read().replace("'",'"')
    us_states = json.loads(data)
    with open(str(Path.cwd().joinpath('wikipedia','flags.txt')), encoding="utf8") as f:
        data = f.read().replace("'",'"')
    flags_final = json.loads(data)
    return us_states, flags_final

def add_or_check_jobs(info, job):
    counter = 0
    for property in info:
        if property[0] == "Occupations":
            for counter in job:
                if counter not in property[1]: 
                    property[1].append(counter)
            break
        else: counter+=1
    if counter == len(info):
        info.append(['Occupations', job])

def get_location(info, final_location):
    if len(final_location) > 3:
        final_location.pop(0)
    if len(final_location) == 3:
        city = final_location[0]
        city = city_exceptions(city)
        state = final_location[1].replace(' ','',1)
        country = final_location[2].replace(' ','',1)
        country = country_exceptions(country)
        info.append(['City/Region', city])
        info.append(['State', state])
        info.append(['Country', country])
        pdate_data = {"City/Region": {"multi_select": [{"name": city}, {"name": property[1]}]}}
        update_page(page_id, update_data)
        add_multiselect(page,"Country", property)
        return city, state, country
    elif len(final_location) == 2:
        city = final_location[0]
        city = city_exceptions(city)
        country = final_location[1].replace(' ','',1)
        country = country_exceptions(country)
        info.append(['City/Region', city])
        add_multiselect(page,"City/Region", property)
        info.append(['Country', country])
        add_multiselect(page,"Country", property)
        return city, country

def edit_data(individual, pages, info, name):
    for page in pages:
        page_id = page["id"]
        query_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        if query_name == individual:
            for property in info:
            

def add_or_edit_notion_wiki(people_list):
    job = []
    error_list = []

    for people in people_list:
        try:
            name, url, property_name = input_names(people)
            data = wiki_scrape_bot(url)
            info = get_info(data, name, url)
            if job != []:
                add_or_check_jobs(info, job)
            get_images(people)
            convert_to_jpg(people)
            gender_list = []
            ethnicity_list = []
            for counter in range(1,6):
                link = str(Path.cwd().joinpath('download',rf'{people} face',rf'Image_{counter}.jpg'))
                gender_count, ethnicity_count = face_recognition(link)
                gender_list.append(gender_count)
                ethnicity_list.append(ethnicity_count)
            print(gender_list, ethnicity_list)
            gender, ethnicity = majority_race_gender(gender_list, ethnicity_list)
            info.append(["Gender", gender])
            add_multiselect(page, "Gender", property)
            info.append(["Ethnicity", ethnicity])
            add_multiselect(page,"Ethnicity", property)
            print("Final List: ", info)
            pages = get_pages(database_id)
            exist = False
            for page in pages:
                og_name = page["properties"]["Name"]["title"][0]["text"]["content"]
                if og_name == name:
                    exist = True
            if exist == False:
                create_page(property_name, database_id)
                pages = get_pages(database_id)
            edit_data((info[0])[0], pages, info, name)
        except KeyboardInterrupt:
            break
        except:
            error_list.append(people)
            continue
    
    if error_list != []:
        print("Error List:", error_list)

add_or_edit_notion_wiki(["American Football (band)"])
