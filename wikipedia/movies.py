import ast
import json
import os
import random
import re
import time
from pathlib import Path

import emoji
import requests
from create_notion import *
from dotenv import load_dotenv
from edit_overwrite_notion import *
from final_transfer import (create_page, populate_content, populate_page_data,
                            update_page)
from import_contents import get_content
from import_requests import get_pages
from movie_summary_template import *
from notion_functions import *
from property_exceptions import language_exceptions, movie_country_exceptions
from wikipedia_summary import wiki_summary


def get_movie_info(movie_name, database_id):

    client_id_and_secret = os.getenv("TMDB_CLIENT_ID_AND_SECRET")
    api_key = os.getenv("TMDB_API_KEY")
    
    movie_for_url = movie_name.replace(" ","+")

    get_id_url = rf'https://api.themoviedb.org/3/search/movie?query={movie_for_url}&api_key={api_key}'

    headers = {
        "accept": "application/json",
        "Authorization": rf"Bearer {client_id_and_secret}"
    }

    response = requests.get(get_id_url, headers=headers)
    id_data = response.json()
    results = id_data["results"]

    for result_position in range(len(results)):
        title = results[result_position]["title"]
        if movie_name == title:
            movie_id = results[result_position]["id"]
            break

    get_description = rf'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(get_description, headers=headers)
    description_data = response.json()

    get_credits = rf"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(get_credits, headers=headers)
    cast_crew_data = response.json()

    return description_data, cast_crew_data

def create_movie(movie_name, database_id, description_data, cast_crew_data):

    genres, spoken_languages, regions, production_companies, countries, actors, directors, producers, cinematographers, composers, editors, writers = ([] for i in range(12))
    actors_and_characters = ""
    
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
        spoken_language["english_name"] = language_exceptions(spoken_language["english_name"])
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
        actors_and_characters += (f"{cast['name']} as {cast['character']}\n")
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

    creation_data = create_title("Name", title) + create_multiselect("Director(s)", directors) + create_multiselect("Genre(s)", genres) + create_multiselect("Writer(s)", writers) + create_multiselect("Producer(s)", producers) + create_multiselect("Cinematographer(s)", cinematographers) + create_multiselect("Starring", actors) + create_date("Date Released", release_date) + create_select("Decade", decade) + create_multiselect("Editor(s)", editors) + create_multiselect("Region(s)", regions) + create_multiselect("Composer(s)", composers) + create_multiselect("Language(s)", spoken_languages) + create_multiselect("Production Company", production_companies) + create_number("Worldwide Gross", total_gross) + create_number("Runtime (mins)", runtime) + create_number("TMDB Score", audience_score)
    
    icon_data = create_icon_image(poster_url)
    cover_data = create_cover_image(backdrop_url)

    creation_data = "{"+ creation_data[:len(creation_data)-1] +"}"
    creation_data = ast.literal_eval(creation_data)
    
    #print(creation_data)

    icon_data = "{" + icon_data.replace("'",'"') + "}"
    icon_data = json.loads(icon_data)

    cover_data = "{" + cover_data.replace("'",'"') + "}"
    cover_data = json.loads(cover_data)

    summary = create_media_block(movie_name, movie_description)
    actors_and_characters = create_media_block(movie_name, actors_and_characters[:len(actors_and_characters)-1])
    if cinematographers != []:
        cinematographers = create_media_block(movie_name, "by " + ", ".join(cinematographers))
    else:
        cinematographers = create_media_block(movie_name, "")
    if composers != []:
        composers = create_media_block(movie_name, "by "+", ".join(composers))
    else:
        composers = create_media_block(movie_name, "")
    
    template = details_plot_blocks[1:len(details_plot_blocks)-1] + ", " + summary + ", " + cast_and_characters_block + ", " + actors_and_characters + ", " + cinematography_block + ", " + cinematographers + ", " + music_block + ", " + composers + ", " + quotes_overall_blocks[1:len(quotes_overall_blocks)-1]
    print(template)

    template = ast.literal_eval(template)

    create_page(creation_data, cover_data, icon_data, database_id, template)    

def edit_movie(movie, description_data, cast_crew_data):

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
        spoken_language["english_name"] = language_exceptions(spoken_language["english_name"])
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

    overwrite_multiselect(movie, "Director(s)", directors)
    overwrite_multiselect(movie, "Genre(s)", genres)
    overwrite_multiselect(movie, "Writer(s)", writers)
    overwrite_multiselect(movie, "Producer(s)", producers)
    overwrite_multiselect(movie, "Cinematographer(s)", cinematographers)
    overwrite_multiselect(movie, "Starring", actors)
    overwrite_date(movie, "Date Released", release_date)
    overwrite_select(movie, "Decade", decade)
    overwrite_multiselect(movie, "Editor(s)", editors)
    overwrite_multiselect(movie, "Region(s)", regions)
    overwrite_multiselect(movie, "Composer(s)", composers)
    overwrite_multiselect(movie, "Language(s)", spoken_languages)
    overwrite_multiselect(movie, "Production Company", production_companies)
    overwrite_number(movie, "Worldwide Gross", total_gross)
    overwrite_number(movie, "Runtime (mins)", runtime)
    overwrite_number(movie, "TMDB Score", audience_score)
    
    icon_data = overwrite_icon_image(movie, poster_url)
    cover_data = overwrite_cover_image(movie, backdrop_url)

    #summary = create_media_block(movie_name, movie_description)
    #summary = ast.literal_eval(summary)

def populate_movie(movie, movie_name, database_id, description_data, cast_crew_data, topic):

    genres, spoken_languages, regions, production_companies, countries, actors, directors, producers, cinematographers, composers, editors, writers = ([] for i in range(12))
    actors_and_characters = ""
    
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
        spoken_language["english_name"] = language_exceptions(spoken_language["english_name"])
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
        actors_and_characters += (f"{cast['name']} as {cast['character']}\n")
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

    populate_data =  create_multiselect("Director(s)", directors) + create_multiselect("Genre(s)", genres) + create_multiselect("Writer(s)", writers) + create_multiselect("Producer(s)", producers) + create_multiselect("Cinematographer(s)", cinematographers) + create_multiselect("Starring", actors) + create_date("Date Released", release_date) + create_select("Decade", decade) + create_multiselect("Editor(s)", editors) + create_multiselect("Region(s)", regions) + create_multiselect("Composer(s)", composers) + create_multiselect("Language(s)", spoken_languages) + create_multiselect("Production Company", production_companies) + create_number("Worldwide Gross", total_gross) + create_number("Runtime (mins)", runtime) + create_number("TMDB Score", audience_score)
    
    icon_data = create_icon_image(poster_url)
    cover_data = create_cover_image(backdrop_url)

    populate_data = "{"+ populate_data[:len(populate_data)-1] +"}"
    populate_data = ast.literal_eval(populate_data)
    
    #print(populate_data)

    icon_data = "{" + icon_data.replace("'",'"') + "}"
    icon_data = json.loads(icon_data)

    cover_data = "{" + cover_data.replace("'",'"') + "}"
    cover_data = json.loads(cover_data)

    summary = create_media_block(movie_name, movie_description)
    actors_and_characters = create_media_block(movie_name, actors_and_characters[:len(actors_and_characters)-1])
    if cinematographers != []:
        cinematographers = create_media_block(movie_name, "by " + ", ".join(cinematographers))
    else:
        cinematographers = create_media_block(movie_name, "")
    if composers != []:
        composers = create_media_block(movie_name, "by "+", ".join(composers))
    else:
        composers = create_media_block(movie_name, "")
    
    template = details_plot_blocks[1:len(details_plot_blocks)-1] + ", " + summary + ", " + cast_and_characters_block + ", " + actors_and_characters + ", " + cinematography_block + ", " + cinematographers + ", " + music_block + ", " + composers + ", " + quotes_overall_blocks[1:len(quotes_overall_blocks)-1]
    #print(template)
    
    summary = ast.literal_eval(summary)
    template = ast.literal_eval(template)

    content = get_content(movie["id"], topic)

    if content == []:
        populate_page_data(movie["id"], populate_data, cover_data, icon_data)
        populate_content(movie["id"], database_id, template)
    else:
        populate_page_data(movie["id"], populate_data, cover_data, icon_data)
        populate_content(movie["id"], database_id, [summary])

def add_movies_to_notion(movies_list):
    load_dotenv()
    database_id = os.getenv("EXAMPLE_MOVIES_DATABASE_ID")
    error_list = []
    topic = "movies"

    for movie in movies_list:
       # try:
            name, url, property_name = process_input(movie)
            get_pages(database_id, topic)
            with open(str(Path.cwd().joinpath(topic+'-db.json')), encoding="utf8") as file:
                movies_pages = json.loads(file.read())["results"]
            movie_exist = check_pages(database_id, movies_pages, movie, topic)
            if movie_exist == False:
                description_data, cast_crew_data = get_movie_info(movie, database_id)
                create_movie(movie, database_id, description_data, cast_crew_data)
                print(f"{movie} has been added to the database")
            else:
                print(f"{movie} already exists in the database")
      #  except KeyboardInterrupt:
            break
      #  except:
            error_list.append(movie)
            continue
    
    if error_list != []:
        print("Error List:", error_list)

def edit_existing_movies_in_notion():
    load_dotenv()
    database_id = os.getenv("MOVIES_DATABASE_ID")
    not_found_list=[]
    error_list = []
    topic = "movies"

    get_pages(database_id, topic)
    with open(str(Path.cwd().joinpath('real-' + topic + '-db.json')), encoding="utf8") as file:
        movies_pages = json.loads(file.read())["results"]
    for movie in movies_pages:
        try:
            movie_name = movie["properties"]["Name"]["title"][0]["text"]["content"]
            description_data, cast_crew_data = get_movie_info(movie_name, database_id)
            try:
                #edit_movie(movie, description_data, cast_crew_data)
                populate_movie(movie, movie_name, database_id, description_data, cast_crew_data, topic)
                print(f"{movie_name} has been edited")
            except Exception as error:
                error_list.append(movie_name)
                print(f"{movie_name} editing failed")
                print("An exception occurred:", error)
        except Exception as error:
            not_found_list.append(movie_name)
            print(f"{movie_name} could not be found")
            print("An exception occurred:", error)
    
    if error_list != []:
        print("Error List:", error_list)

    if not_found_list != []:
        print("Not Found List:", not_found_list)

start = time.time()
#add_movies_to_notion(["Toy Story 2"])
edit_existing_movies_in_notion()
end = time.time()

print(f"Time taken to run the code was {end-start} seconds")
