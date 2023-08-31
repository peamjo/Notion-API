import ast
import json
import os
import random
import re
from pathlib import Path

import emoji
import requests
from dotenv import load_dotenv
from final_transfer import create_content, create_page, update_page
from import_requests import get_pages
from new_add_to_notion import *
from new_create_notion import *
from notion_functions import *
from property_exceptions import movie_country_exceptions
from wikipedia_summary import wiki_summary


def get_info_and_create_movie(movie_name, database_id):
    creation_data = ""

    client_id_and_secret = os.getenv("TMDB_CLIENT_ID_AND_SECRET")
    
    movie_for_url = movie_name.replace(" ","+")

    get_id_url = rf'https://api.themoviedb.org/3/search/movie?query={movie_for_url}&api_key=557d338147d764947241b45e888da7f3'

    headers = {
        "accept": "application/json",
        "Authorization": rf"Bearer {client_id_and_secret}"
    }

    response = requests.get(get_id_url, headers=headers)
    id_data = response.json()
    results = id_data["results"]

    #increase the result position if the movie is not the one you intended
    result_position = 0
    movie_id = results[result_position]["id"]

    get_description = rf'https://api.themoviedb.org/3/movie/{movie_id}?api_key=557d338147d764947241b45e888da7f3'
    response = requests.get(get_description, headers=headers)
    description_data = response.json()

    get_credits = rf"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(get_credits, headers=headers)
    cast_crew_data = response.json()

    genres, spoken_languages, regions, production_companies, countries, actors, directors, producers, cinematographers, composers, editors, writers = ([] for i in range(12))
    
    title = description_data["title"]
    movie_description = description_data["overview"].replace("/","")
    release_date = description_data["release_date"]
    decade = release_date[:3]+"0s"
    total_gross = description_data["revenue"]
    runtime = description_data["runtime"]
    backdrop_url = 'https://image.tmdb.org/t/p/original'+description_data["backdrop_path"]
    poster_url = 'https://image.tmdb.org/t/p/w342/'+description_data["poster_path"]
    audience_score = description_data["vote_average"]
    for spoken_language in description_data["spoken_languages"]:
        spoken_languages.append(spoken_language["english_name"])
    for region in description_data["production_countries"]:
        region["name"] = movie_country_exceptions(region["name"])
        regions.append(region["name"])
    for genre in description_data["genres"]:
        genres.append(genre["name"])
    for company in description_data["production_companies"]:
        production_companies.append(company["name"])
    for country in description_data["production_countries"]:
        countries.append(country["name"])

    cast_list = cast_crew_data["cast"]
    crew_list = cast_crew_data["crew"]
    counter = 0

    for cast in cast_list:
        actors.append(cast["name"])
        counter += 1
        if counter == 11:
            break
    for crew in crew_list:
        if crew["job"] == 'Director':
            directors.append(crew["name"])
        if crew["job"] == 'Producer':
            producers.append(crew["name"])
        if crew["job"] == 'Director of Photography':
            cinematographers.append(crew["name"])
        if crew["job"] == 'Original Music Composer':
            composers.append(crew["name"])
        if crew["job"] == 'Editor':
            editors.append(crew["name"])
        if crew["job"] == 'Writer':
            writers.append(crew["name"])
    
    creation_data = create_title("Name", title, creation_data)
    creation_data = create_multiselect("Director(s)", directors, creation_data)
    creation_data = create_multiselect("Genre(s)", genres, creation_data)
    creation_data = create_multiselect("Writer(s)", writers, creation_data)
    creation_data = create_multiselect("Producer(s)", producers, creation_data)
    creation_data = create_multiselect("Cinematographer(s)", cinematographers, creation_data)
    creation_data = create_multiselect("Starring", actors, creation_data)
    creation_data = create_date("Date Released", release_date, creation_data)
    creation_data = create_select("Decade", decade, creation_data)
    creation_data = create_multiselect("Editor(s)", editors, creation_data)
    creation_data = create_multiselect("Region(s)", regions, creation_data)
    creation_data = create_multiselect("Composer(s)", composers, creation_data)
    creation_data = create_multiselect("Language(s)", spoken_languages, creation_data)
    creation_data = create_multiselect("Production Company", production_companies, creation_data)
    creation_data = create_number("Worldwide Gross", total_gross, creation_data)
    creation_data = create_number("Runtime (mins)", runtime, creation_data)
    creation_data = create_number("TMDB Score", audience_score, creation_data)
    icon_data = create_icon_image(poster_url)
    cover_data = create_cover_image(backdrop_url)

    creation_data = "{"+ creation_data[:len(creation_data)-1] +"}"
    creation_data = ast.literal_eval(creation_data)
    print(creation_data)

    icon_data = "{" + icon_data.replace("'",'"') + "}"
    icon_data = json.loads(icon_data)

    cover_data = "{" + cover_data.replace("'",'"') + "}"
    cover_data = json.loads(cover_data)

    page = create_page(creation_data, cover_data, icon_data, database_id)
    print(page)
    #create_content(page["id"], movie_description)
    #add_summary(page, movie_name)


def add_or_edit_notion_movies(movies_list):
    load_dotenv()
    database_id = os.getenv("EXAMPLE_MOVIES_DATABASE_ID")
    error_list = []
    topic = "movies"

    for movie in movies_list:
        try:
            name, url, property_name = process_input(movie)
            load_pages(database_id, topic)
            with open(str(Path.cwd().joinpath(topic+'-db.json')), encoding="utf8") as file:
                movies_pages = json.loads(file.read())["results"]
            movie_exist = check_pages(database_id, movies_pages, name, property_name, topic)
            if movie_exist == False:
                get_info_and_create_movie(movie, database_id)
            else:
                pass
                #update_movie_page
        except KeyboardInterrupt:
            break
        except:
            error_list.append(movie)
            continue
    
    if error_list != []:
        print("Error List:", error_list)

add_or_edit_notion_movies(["The Big Short"])
