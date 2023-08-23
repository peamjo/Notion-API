import requests
import json
from add_to_notion import add_title, add_text, add_number, add_multiselect, add_date, add_select
from get_info import input_names
from import_requests import get_pages
from final_transfer import update_page, create_page, create_content


def get_movie_info(movie_name):
    movie_information = [[movie_name]]
    movie = movie_name.replace(" ","+")

    get_id_url = rf'https://api.themoviedb.org/3/search/movie?query={movie}&api_key=557d338147d764947241b45e888da7f3'

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NTdkMzM4MTQ3ZDc2NDk0NzI0MWI0NWU4ODhkYTdmMyIsInN1YiI6IjY0ZTQ3OTIxZTBjYTdmMDBlMzQ5NWVkYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.TpJ9RDJ5qQmjDzDFp_Y9x1JDFrSFgvt4PJIY5mYQabU"
    }

    response = requests.get(get_id_url, headers=headers)
    data = response.json()
    results = data["results"]

    for page in results:
        movie_id = page["id"]
        break

    get_description = rf'https://api.themoviedb.org/3/movie/{movie_id}?api_key=557d338147d764947241b45e888da7f3'
    response = requests.get(get_description, headers=headers)
    data = response.json()
    genres = []
    spoken_languages = []
    production_companies = []
    countries = []

    movie_description = data["overview"]
    release_date = data["release_date"]
    total_gross = data["revenue"]
    runtime = data["runtime"]
    audience_score = data["vote_average"]
    for spoken_language in data["spoken_languages"]:
        spoken_languages.append(spoken_language["english_name"])
    for genre in data["genres"]:
        genres.append(genre["name"])
    for company in data["production_companies"]:
        production_companies.append(company["name"])
    for country in data["production_countries"]:
        countries.append(country["name"])

    decade = release_date[:3]+"0s"

    movie_information.append(["description", movie_description])
    movie_information.append(["genres", genres])
    movie_information.append(["languages", spoken_languages])
    movie_information.append(["release date", release_date])
    movie_information.append(["decade", decade])
    movie_information.append(["production companies", production_companies])
    movie_information.append(["total gross", total_gross])
    movie_information.append(["runtime", runtime])

    get_credits = rf"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(get_credits, headers=headers)
    data = response.json()
    actors = []
    directors = []
    producers = []
    cinematographers = []
    composers = []
    editors = []
    writers = []

    cast_list = data["cast"]
    crew_list = data["crew"]
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

    movie_information.append(["actors", actors])
    movie_information.append(["directors", directors]) 
    movie_information.append(["writers", writers])
    movie_information.append(["producers", producers])
    movie_information.append(["cinematographers", cinematographers])
    movie_information.append(["composers", composers])
    movie_information.append(["editors", editors])
    movie_information.append(["audience score", audience_score])

    print(movie_information)
    return(movie_information)

def edit_movie_data(individual, pages, info, name):
    for page in pages:
        page_id = page["id"]
        query_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        if query_name == individual:
            for property in info:
                if property[0] == 'directors': add_multiselect(page_id, "Director(s)", property)
                if property[0] == 'release date': add_date(page_id, "Date Released", property)
                if property[0] == 'decade': add_select(page_id, "Decade", property)
                if property[0] == 'genres': add_multiselect(page_id, "Genre(s)", property)
                if property[0] == 'languages': add_multiselect(page_id, "Language(s)", property)
                if property[0] == 'production companies': add_multiselect(page_id, "Production Company", property)
                if property[0] == 'actors': add_multiselect(page_id, "Starring", property)
                if property[0] == 'producers': add_multiselect(page_id, "Producer(s)", property)
                if property[0] == 'writers': add_multiselect(page_id, "Writer(s)", property)
                if property[0] == 'cinematographers': add_multiselect(page_id, "Cinematographer(s)", property)
                if property[0] == 'composers': add_multiselect(page_id, "Composer(s)", property)
                if property[0] == 'editors': add_multiselect(page_id, "Editor(s)", property)
                if property[0] == 'total gross': add_number(page_id, "Worldwide Gross", property)
                if property[0] == 'runtime': add_number(page_id, "Runtime (mins)", property)
                if property[0] == 'audience score': add_number(page_id, "TMDB Score", property)

def add_or_edit_notion_movies(movies_list):
    error_list = []

    for movie in movies_list:
        try:
            name, url, property_name = input_names(movie)
            info = get_movie_info(movie)
            pages = get_pages()
            exist = False
            for page in pages:
                og_name = page["properties"]["Name"]["title"][0]["text"]["content"]
                if og_name == name:
                    exist = True
            if exist == False:
                create_page(property_name)
                pages = get_pages()
            edit_movie_data((info[0])[0], pages, info, name)
        except KeyboardInterrupt:
            break
        except:
            error_list.append(movie)
            continue
    
    if error_list != []:
        print("Error List:", error_list)

add_or_edit_notion_movies(["One Direction: This Is Us"])
