import ast
import json
import os
import random
import re
import time
from pathlib import Path

import emoji
import requests
from dotenv import load_dotenv
from movies.movie_summary_template import *
from notion_manipulation.create_notion import *
from notion_manipulation.edit_overwrite_notion import *
from notion_manipulation.final_transfer import (create_page, delete_content,
                                                populate_content,
                                                populate_content_after_block,
                                                populate_page_data,
                                                update_content, update_page)
from notion_manipulation.import_contents import get_content
from notion_manipulation.import_requests import get_pages
from notion_manipulation.notion_functions import *
from notion_manipulation.property_exceptions import (language_exceptions,
                                                     movie_country_exceptions)
from wikipedia.wikipedia_summary import wiki_summary


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

def process_movie_info(movie_name, database_id, description_data, cast_crew_data, topic):

    genres, spoken_languages, regions, production_companies, countries, actors, directors, producers, cinematographers, composers, editors, writers, actors_and_characters = ([] for i in range(13))
    
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

    casts_and_characters_block = ""

    for cast in cast_list:
        actors.append(cast["name"])
        actors_and_characters.append(f"{cast['name']} as {cast['character']}")
        casts_and_characters_block += f"{cast['name']} as {cast['character']}\n"
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

    movie_data_string = create_title("Name", title) + create_multiselect("Director(s)", directors) + create_multiselect("Genre(s)", genres) + create_multiselect("Writer(s)", writers) + create_multiselect("Producer(s)", producers) + create_multiselect("Cinematographer(s)", cinematographers) + create_multiselect("Starring", actors) + create_date("Date Released", release_date) + create_select("Decade", decade) + create_multiselect("Editor(s)", editors) + create_multiselect("Region(s)", regions) + create_multiselect("Composer(s)", composers) + create_multiselect("Language(s)", spoken_languages) + create_multiselect("Production Company", production_companies) + create_number("Worldwide Gross", total_gross) + create_number("Runtime (mins)", runtime) + create_number("TMDB Score", audience_score)

    #print(movie_data_string)

    movie_data_dict = {"Director(s)": directors, "Starring": actors, "Genre(s)": genres, "Writer(s)": writers, "Producer(s)": producers, "Cinematographer(s)": cinematographers, "Date Released": release_date, "Decade": decade, "Editor(s)": editors, "Region(s)": regions, "Composer(s)": composers, "Language(s)": spoken_languages, "Production Company": production_companies, "Worldwide Gross": total_gross, "Runtime (mins)": runtime, "TMDB Score": audience_score, "Icon Data": poster_url, "Cover Data": backdrop_url}

    icon_data = create_icon_image(poster_url)
    cover_data = create_cover_image(backdrop_url)

    movie_data_string = "{"+ movie_data_string[:len(movie_data_string)-1] +"}"
    movie_data_string = ast.literal_eval(movie_data_string)

    icon_data = "{" + icon_data.replace("'",'"') + "}"
    icon_data = json.loads(icon_data)

    cover_data = "{" + cover_data.replace("'",'"') + "}"
    cover_data = json.loads(cover_data)

    summary = create_paragraph_block(movie_description)

    casts_and_characters_blocks_to_add = []

    for actor_and_character in actors_and_characters: 
        casts_and_characters_blocks_to_add.append(create_paragraph_block(actor_and_character))

    casts_and_characters_blocks_to_add_string = ', '.join(casts_and_characters_blocks_to_add)

    if cinematographers != []:
        cinematographers = create_paragraph_block("by " + ", ".join(cinematographers))
    else:
        cinematographers = create_paragraph_block("")
    if composers != []:
        composers = create_paragraph_block("by "+", ".join(composers))
    else:
        composers = create_paragraph_block("")
    

    template = details_plot_blocks[1:len(details_plot_blocks)-1] + ", " + summary + ", " + cast_and_characters_block + ", " + casts_and_characters_blocks_to_add_string + ", " + cinematography_block + ", " + cinematographers + ", " + music_block + ", " + composers + ", " + quotes_overall_blocks[1:len(quotes_overall_blocks)-1]
    #print(template)
    
    summary = ast.literal_eval(summary)
    template = ast.literal_eval(template)
    
    return movie_data_string, movie_data_dict, cover_data, icon_data, summary, movie_description, template, casts_and_characters_blocks_to_add, cinematographers, composers

def edit_existing_movie_data(movie_page, movie_description, existing_content, template, summary, casts_and_characters_blocks_to_add, cinematographers, composers):
    #if existing_content[0]["type"] == "heading_2":
    if existing_content[0]["heading_2"]["rich_text"][0]["text"]["content"] == "History":
        for i in range(len(existing_content)):
            if existing_content[i]["type"] == "heading_2":
                if existing_content[i]["heading_2"]["rich_text"][0]["text"]["content"] == "History":
                        update_content(existing_content[i]["id"], ast.literal_eval(create_h2_block("Movie History/Details", "yellow")))
                if existing_content[i]["heading_2"]["rich_text"][0]["text"]["content"] == "Plot":
                        update_content(existing_content[i]["id"], ast.literal_eval(create_h2_block("Plot", "green")))
                        plot_block = i
                if existing_content[i]["heading_2"]["rich_text"][0]["text"]["content"] == "Cast and Characters":
                        update_content(existing_content[i]["id"], ast.literal_eval(create_h2_block("Cast and Characters", "pink")))
                        cast_and_characters_block = i
                if existing_content[i]["heading_2"]["rich_text"][0]["text"]["content"] == "Cinematography":
                        update_content(existing_content[i]["id"], ast.literal_eval(create_h2_block("Cinematography", "gray")))
                        cinematography_block = i
                if existing_content[i]["heading_2"]["rich_text"][0]["text"]["content"] == "Music Score":
                        update_content(existing_content[i]["id"], ast.literal_eval(create_h2_block("Music/Film Score", "blue")))
                        music_block = i
                if existing_content[i]["heading_2"]["rich_text"][0]["text"]["content"] == "Quote":
                        update_content(existing_content[i]["id"], ast.literal_eval(create_h2_block("Quotes", "purple")))
                if existing_content[i]["heading_2"]["rich_text"][0]["text"]["content"] == "Overall":
                        update_content(existing_content[i]["id"], ast.literal_eval(create_h2_block("Overall", "brown")))
                        overall_block = i
        

        if existing_content[plot_block+1]["type"] == "paragraph":
            if existing_content[plot_block+1]["paragraph"]["rich_text"] == []:
                update_content(existing_content[plot_block+1]["id"], summary) 
        
        for cast in reversed(casts_and_characters_blocks_to_add):
            populate_content_after_block(movie_page["id"], [ast.literal_eval(cast)], existing_content[cast_and_characters_block]["id"])

        if existing_content[cinematography_block+1]["type"] == "paragraph" and existing_content[cinematography_block+1]["paragraph"]["rich_text"] == [] and cinematographers != create_paragraph_block(""):
            populate_content_after_block(movie_page["id"], [ast.literal_eval(cinematographers)], existing_content[cinematography_block]["id"])

        if existing_content[music_block+1]["type"] == "paragraph" and existing_content[music_block+1]["paragraph"]["rich_text"] == [] and composers != create_paragraph_block(""):
            populate_content_after_block(movie_page["id"], [ast.literal_eval(composers)], existing_content[music_block]["id"])

        try:
            extra_plot_limit = len(existing_content)-overall_block   
            for i in range(1,extra_plot_limit):
                if existing_content[overall_block+i]["type"] == "paragraph":
                    if existing_content[overall_block+i]["paragraph"]["rich_text"][0]["text"]["content"] == movie_description:
                        delete_content(existing_content[overall_block+i]["id"])
        except:
            pass

    else:
        populate_content(movie_page["id"], template)

def fast_create_movie(movie_data_string, cover_data, icon_data, database_id, template):
    create_page(movie_data_string, cover_data, icon_data, database_id, template)    

def fast_populate_movie(movie_page, movie_data_string, cover_data, icon_data, template, summary, movie_description, topic, casts_and_characters_blocks_to_add, cinematographers, composers):    
    existing_content = get_content(movie_page["id"], topic)
    if existing_content == []:
        populate_page_data(movie_page["id"], movie_data_string, cover_data, icon_data)
        populate_content(movie_page["id"], template)
    else:
        populate_page_data(movie_page["id"], movie_data_string, cover_data, icon_data)
        edit_existing_movie_data(movie_page, movie_description, existing_content, template, summary, casts_and_characters_blocks_to_add, cinematographers, composers)

def slow_populate_movie(movie_page, movie_data_dict, template, summary, movie_description, topic, casts_and_characters_blocks_to_add, cinematographers, composers):
    overwrite_multiselect(movie_page, "Director(s)", movie_data_dict.get("Director(s)"))
    overwrite_multiselect(movie_page, "Starring", movie_data_dict.get("Starring"))
    overwrite_multiselect(movie_page, "Genre(s)", movie_data_dict.get("Genre(s)"))
    overwrite_multiselect(movie_page, "Writer(s)", movie_data_dict.get("Writer(s)"))
    overwrite_multiselect(movie_page, "Producer(s)", movie_data_dict.get("Producer(s)"))
    overwrite_multiselect(movie_page, "Cinematographer(s)", movie_data_dict.get("Cinematographer(s)"))
    overwrite_date(movie_page, "Date Released", movie_data_dict.get("Date Released"))
    overwrite_select(movie_page, "Decade", movie_data_dict.get("Decade"))
    overwrite_multiselect(movie_page, "Editor(s)", movie_data_dict.get("Editor(s)"))
    overwrite_multiselect(movie_page, "Region(s)", movie_data_dict.get("Region(s)"))
    overwrite_multiselect(movie_page, "Composer(s)", movie_data_dict.get("Composer(s)"))
    overwrite_multiselect(movie_page, "Language(s)", movie_data_dict.get("Language(s)"))
    overwrite_multiselect(movie_page, "Production Company", movie_data_dict.get("Production Company"))
    overwrite_number(movie_page, "Worldwide Gross", movie_data_dict.get("Worldwide Gross"))
    overwrite_number(movie_page, "Runtime (mins)", movie_data_dict.get("Runtime (mins)"))
    overwrite_number(movie_page, "TMDB Score", movie_data_dict.get("TMDB Score"))
    overwrite_icon_image(movie_page, movie_data_dict.get("Icon Data"))
    overwrite_cover_image(movie_page, movie_data_dict.get("Cover Data"))

    existing_content = get_content(movie_page["id"], topic)
    if existing_content == []:
        populate_content(movie_page["id"], template)
    else:
        edit_existing_movie_data(movie_page, movie_description, existing_content, template, summary, casts_and_characters_blocks_to_add, cinematographers, composers)

def create_movies_in_notion(movies_list):
    load_dotenv()
    database_id = os.getenv("MOVIES_DATABASE_ID")
    error_list = []
    topic = "movies"

    #get_pages(database_id, topic)
    with open(str(Path.cwd().joinpath('notion_projects', 'movies', 'movies_databases','real-' + topic +'-db.json')), encoding="utf8") as file:
        movies_pages = json.loads(file.read())["results"]
    
    for movie_name in movies_list:
        try:
            movie_exist = check_pages(database_id, movies_pages, movie_name, topic)
            if movie_exist == False:
                description_data, cast_crew_data = get_movie_info(movie_name, database_id)
                movie_data_string, movie_data_dict, cover_data, icon_data, summary, movie_description, template, casts_and_characters_blocks_to_add, cinematographers, composers = process_movie_info(movie_name, database_id, description_data, cast_crew_data, topic)
                fast_create_movie(movie_data_string, cover_data, icon_data, database_id, template)
                print(f"{movie_name} has been added to the database")
            else:
                print(f"{movie_name} already exists in the database")
        except KeyboardInterrupt:
            break
        except Exception as error:
            error_list.append(movie_name)
            print("An exception occurred:", error)
            continue
    
    if error_list != []:
        print("Error List:", error_list)

def populate_existing_movies_in_notion():
    load_dotenv()
    database_id = os.getenv("EXAMPLE_MOVIES_DATABASE_ID")
    not_found_list=[]
    error_list = []
    topic = "movies"

    get_pages(database_id, topic)
    with open(str(Path.cwd().joinpath('notion_projects', 'movies', 'movies_databases', topic + '-db.json')), encoding="utf8") as file:
        movies_pages = json.loads(file.read())["results"]
    
    for movie_page in movies_pages:
        try:
            movie_name = movie_page["properties"]["Name"]["title"][0]["text"]["content"]
            description_data, cast_crew_data = get_movie_info(movie_name, database_id)
            try:
                movie_data_string, movie_data_dict, cover_data, icon_data, summary, movie_description, template, casts_and_characters_blocks_to_add, cinematographers, composers = process_movie_info(movie_name, database_id, description_data, cast_crew_data, topic)
                fast_populate_movie(movie_page, movie_data_string, cover_data, icon_data, template, summary, movie_description, topic, casts_and_characters_blocks_to_add, cinematographers, composers)
                #slow_populate_movie(movie_page, movie_data_dict, template, summary, movie_description, topic, casts_and_characters_blocks_to_add, cinematographers, composers)
                print(f"{movie_name} has been edited")
            except Exception as error:
                error_list.append(movie_name)
                print(f"{movie_name} editing failed")
                print("An exception occurred:", error)
        except Exception as error:
            try:
                not_found_list.append(movie_name)
                print(f"{movie_name} could not be found")
                print("An exception occurred:", error)
            except:
                print("Empty Page")


    if error_list != []:
        print("Error List:", error_list)

    if not_found_list != []:
        print("Not Found List:", not_found_list)
