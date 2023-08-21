from wiki_scraping_final import wiki_scrape_bot
import string
from import_requests import get_pages
from final_transfer import update_page, create_page, create_content
import re
from wikipedia_summary import wiki_summary
from get_images import get_images, convert_to_jpg
from face_recognition import face_recognition, majority_race_gender
from pathlib import Path
import json

#Enter_input = input("Search: ")
def input_names(Enter_input):
    if Enter_input[:2] != "DJ":
        u_i = string.capwords(Enter_input)
    else:
        u_i = "DJ " + string.capwords(Enter_input).split(" ",1)[1]
    lists = u_i.split()
    word = "_".join(lists)
    url = "https://en.wikipedia.org/wiki/" + word
    name = {
        "Name": {"title": [{"text": {"content": u_i}}]},
    }
    return u_i, url, name

def get_info(data):
    info = [[u_i]]    
    us_states, flags_final = load_dict()

    for counter, property in enumerate(data):
        if property[0] == "Died":
            segment_1 = property[1].split('(', 1)
            segment_2 = segment_1[1].split(')', 1)
            death_date = segment_2[0]
            info.append(['Died', death_date])
            info.append(['YoD', death_date.split("-",1)[0]])
        if property[0] == "Born":
            segment_1 = property[1].split('(', 1)
            segment_2 = segment_1[1].split(')', 1)
            birth_date = segment_2[0]
            if (data[counter+1])[0] == "Died":
                match = re.findall(r'\d', property[1])
                last_num = match[-1]
                segment_1 = property[1].split(last_num)
            else:
                segment_1 = property[1].split(')')
            location = segment_1[-1]            
            final_location = location.split(',')
            info.append(['Birthday', birth_date])
            info.append(['YoB', birth_date.split("-",1)[0]])
            if len(final_location) > 3:
                final_location.pop(0)
            if len(final_location) == 3:
                city = final_location[0]
                state = final_location[1].replace(' ','',1)
                country = final_location[2].replace(' ','',1)
                info.append(['City/Region', city])
                info.append(['State', state])
                info.append(['Country', country])
            elif len(final_location) > 1 and len(final_location) < 3:
                city = final_location[0]
                if city == "New York City":
                    city = "NYC"
                country = final_location[1].replace(' ','',1)
                if country == "Empire of Japan":
                    country = "Japan"
            #   if country == "French Algeria":
            #       country = "'France', 'Algeria'"
                info.append(['City', city])
                info.append(['Country', country])
            if len(info)>1:
                if (info[-1])[1] == 'U.S.' or (info[-1])[1] == 'US' or (info[-1])[1] == 'United States':
                    (info[-1])[1] = 'USA'
                    if len(final_location)>2:
                        for key in us_states:                    
                            if key == state:
                                (info[-2])[1] = us_states[key]
                for key in flags_final:
                    if flags_final[key] == (info[-1])[1]:
                        info.append(['Flag', key])
        if property[0] == "Occupations" or property[0] == 'Occupation' or property[0] == "Occupation(s)":
            info.append(['Occupations', property[1]])
        if property[0] == "Genres":
            info.append(['Genres', property[1]])
        if property[0] == "Instruments" or property[0] == "Instrument(s)":
            info.append(['Instruments', property[1]])
        if property[0] == "Movement":
            info.append(['Art Style/Movement', property[1]])
        if property[0] == "Years active" or property[0] == "Turned pro":
            property[1]=property[1].replace("–"," to ")
            property[1]=property[1].replace("-"," to ")
            info.append(['Years active', property[1]])
        if property[0] == "Retired":
            info.append(['Retired', property[1]])
    info.append(['Wiki', url])
    return(info)

def load_dict():
    with open(str(Path.cwd().joinpath('wikipedia','us_states.txt'))) as f:
        data = f.read().replace("'",'"')
    us_states = json.loads(data)
    with open(str(Path.cwd().joinpath('wikipedia','flags.txt'))) as f:
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
        

def edit_data(individual):
    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        name = props["Name"]["title"][0]["text"]["content"]
        if name == individual:
            for counter,property in enumerate(info):
                if property[0] == 'Birthday':
                    update_data = {"Date": {"date": {"start": property[1]}}}
                    update_page(page_id, update_data)
                    birth = property[1]
                if property[0] == 'Died':
                    update_data = {"Date": {"date": {"start": birth, "end": property[1]}}}
                    update_page(page_id, update_data)
                if property[0] == 'YoB':
                    update_data = {"YoB": {"number": int(property[1])}}
                    update_page(page_id, update_data)
                if property[0] == 'YoD':
                    update_data = {"YoD": {"number": int(property[1])}}
                    update_page(page_id, update_data)
                if property[0] == 'Years active':
                    update_data = {"Years active": {"rich_text": [{"text": {"content": property[1]}}]}}
                    update_page(page_id, update_data)
                if property[0] == 'Country':
                    update_data = {"Country": {"multi_select": [{"name": property[1]}]}}
                    update_page(page_id, update_data)
                if property[0] == 'City/Region':
                    update_data = {"City/Region": {"multi_select": [{"name": property[1]}]}}
                    update_page(page_id, update_data)
                    city = property[1]
                if property[0] == 'State':
                    update_data = {"City/Region": {"multi_select": [{"name": city}, {"name": property[1]}]}}
                    update_page(page_id, update_data)
                if property[0] == 'Gender':
                    update_data = {"Gender": {"select": {"name": property[1]}}}
                    update_page(page_id, update_data)
                if property[0] == 'Ethnicity':
                    update_data = {"Ethnicity": {"multi_select": [{"name": property[1]}]}}
                    update_page(page_id, update_data)
                if property[0] == 'Flag':
                    update_data = {"emoji": property[1]}
                    update_page(page_id, update_data)
                if property[0] == 'Occupations':
                    jobs = []
                    for j in property[1]:
                        j = {"name": j}
                        jobs.append(j)
                    update_data = {"Job(s)": {"multi_select": jobs}}
                    update_page(page_id, update_data)
                if property[0] == 'Wiki':
                    update_data = {"Wiki": {"url": property[1]}}
                    update_page(page_id, update_data)
                if property[0] == 'Genres':
                    genres = []
                    for j in property[1]:
                        j = {"name": j}
                        genres.append(j)
                    update_data = {"Genre (Music)": {"multi_select": genres}}
                    update_page(page_id, update_data)
                if property[0] == 'Instruments':
                    instruments = []
                    for j in property[1]:
                        j = {"name": j}
                        instruments.append(j)
                    update_data = {"Instrument(s)": {"multi_select": instruments}}
                    update_page(page_id, update_data)
                if property[0] == 'Art Style/Movement':
                    movement = []
                    for j in property[1]:
                        j = {"name": j}
                        movement.append(j)
                    update_data = {"Art Style/Movement": {"multi_select": movement}}
                    update_page(page_id, update_data)
            update_data = wiki_summary(name)
            create_content(page_id, update_data)

people_list = ["Taylor Swift"]
job = []
error_list = []

for people in people_list:
    try:
        u_i, url, name = input_names(people)
        data = wiki_scrape_bot(url)
        print(data)
        info = get_info(data)
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
        info.append(["Ethnicity", ethnicity])
        print(info)
        pages = get_pages()
        exist = False
        for page in pages:
            og_name = page["properties"]["Name"]["title"][0]["text"]["content"]
            if og_name == u_i:
                exist = True
        if exist == False:
            create_page(name)
            pages = get_pages()
        edit_data((info[0])[0])
    except KeyboardInterrupt:
        break
    #except:
     #   error_list.append(people)
     #   continue
print("Error List:", error_list)
