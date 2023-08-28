import requests
import json
from add_to_notion import add_title, add_text, add_number, add_multiselect, add_date, add_select, add_dates
from get_info import input_names
from import_requests import get_pages
from final_transfer import update_page, create_page, create_content
from dotenv import load_dotenv
import os
from property_exceptions import country_exceptions

load_dotenv()
database_id = os.getenv("EXAMPLE_TV_SHOWS_DATABASE_ID")

def get_tv_show_info(tv_show_name):
    tv_show_information = [[tv_show_name]]
    tv = tv_show_name.replace(" ","+")

    get_id_url = rf'https://api.themoviedb.org/3/search/tv?query={tv}&api_key=557d338147d764947241b45e888da7f3'

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NTdkMzM4MTQ3ZDc2NDk0NzI0MWI0NWU4ODhkYTdmMyIsInN1YiI6IjY0ZTQ3OTIxZTBjYTdmMDBlMzQ5NWVkYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.TpJ9RDJ5qQmjDzDFp_Y9x1JDFrSFgvt4PJIY5mYQabU"
    }
    response = requests.get(get_id_url, headers=headers)
    data = response.json()
    results = data["results"]

    for page in results:
        tv_id = page["id"]
        break

    get_description = rf'https://api.themoviedb.org/3/tv/{tv_id}?api_key=557d338147d764947241b45e888da7f3'
    response = requests.get(get_description, headers=headers)
    data = response.json()

    genres = []
    spoken_languages = []
    production_companies = []
    countries = []
    creators = []
    channels = []
    decades=[]

    try:
        runtime = data["episode_run_time"][0]
        tv_show_information.append(["runtime", runtime])
    except:
        pass
    seasons = data["number_of_seasons"]
    episodes = data["number_of_episodes"]
    first_episode = data["first_air_date"]
    decades.append((data["first_air_date"])[:3]+"0s")
    if data["last_episode_to_air"]["episode_type"] == "finale":
        last_episode = data["last_air_date"]
        decades.append((data["last_air_date"])[:3]+"0s")
    for creator in data["created_by"]:
        creators.append(creator["name"])
    for spoken_language in data["languages"]:
        spoken_languages.append(spoken_language)
    for genre in data["genres"]:
        genres.append(genre["name"])
    for company in data["production_companies"]:
        production_companies.append(company["name"])
    for country in data["production_countries"]:
        country["name"] = country_exceptions(country["name"])
        countries.append(country["name"])
    for channel in data["networks"]:
        channels.append(channel["name"])


    tv_show_information.append(["showrunner", creators])
    tv_show_information.append(["genres", genres])
    tv_show_information.append(["languages", spoken_languages])
    tv_show_information.append(["countries", countries])
    tv_show_information.append(["channels", channels])
    tv_show_information.append(["decades", decades])
    tv_show_information.append(["production companies", production_companies])
    tv_show_information.append(["season(s)", seasons])
    tv_show_information.append(["episode(s)", episodes])
    tv_show_information.append(["first episode", first_episode])
    if data["last_episode_to_air"]["episode_type"] == "finale":
        tv_show_information.append(["last episode", last_episode])

    get_credits = rf"https://api.themoviedb.org/3/tv/{tv_id}/credits"
    response = requests.get(get_credits, headers=headers)
    data = response.json()

    cast_list = data["cast"]
    counter = 0
    actors = []

    for cast in cast_list:
        actors.append(cast["name"])
        counter += 1
        if counter == 11:
            break
    tv_show_information.append(["actors", actors])

    print(tv_show_information)
    return(tv_show_information)

def edit_tv_show_data(individual, pages, info, name):
    for page in pages:
            page_id = page["id"]
            query_name = page["properties"]["Name"]["title"][0]["text"]["content"]
            if query_name == individual:
                for property in info:
                    if property[0] == 'showrunner': add_multiselect(page, "Creator(s)", property)                   
                    if property[0] == 'channels': add_multiselect(page, "Channel(s)", property)
                    if property[0] == 'decades': add_multiselect(page, "Decade(s)", property)
                    if property[0] == 'genres': add_multiselect(page, "Genre(s)", property)
                    if property[0] == 'languages': add_multiselect(page, "Language(s)", property)
                    if property[0] == 'countries': add_multiselect(page, "Country", property)
                    if property[0] == 'production companies': add_multiselect(page, "Production Company", property)
                    if property[0] == 'actors': add_multiselect(page, "Starring", property)
                    if property[0] == 'runtime': add_number(page, "Runtime (mins)", property)
                    if property[0] == 'season(s)': add_number(page, "Season(s)", property)
                    if property[0] == 'episode(s)': add_number(page, "Episode(s)", property)
                    if property[0] == 'first episode': 
                        add_date(page, "Date Released", property) 
                        date = property[1]
                    if property[0] == 'last episode': add_dates(page, "Date Released", property, date)

def add_or_edit_notion_tv(tv_show_list):
    error_list = []

    for tv in tv_show_list:
        try:
            name, url, property_name = input_names(tv)
            info = get_tv_show_info(tv)
            pages = get_pages(database_id)
            exist = False
            for page in pages:
                og_name = page["properties"]["Name"]["title"][0]["text"]["content"]
                if og_name == name:
                    exist = True
            if exist == False:
                create_page(property_name, database_id)
                pages = get_pages(database_id)
            edit_tv_show_data((info[0])[0], pages, info, name)
        except KeyboardInterrupt:
            break
        except:
            error_list.append(tv)
            continue
    
    if error_list != []:
        print("Error List:", error_list)

add_or_edit_notion_tv(["Luke Cage"])
