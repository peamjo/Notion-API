import requests
import json
from add_to_notion import add_title, add_text, add_number, add_multiselect, add_date

input_movie = "Ikiru"
movie_information = [[input_movie]]
movie = input_movie.replace(" ","+")

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
print(data)
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

movie_information.append(["description", movie_description])
movie_information.append(["genre", genres])
movie_information.append(["language", spoken_languages])
movie_information.append(["release date", release_date])
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
movie_information.append(["director", directors]) 
movie_information.append(["writers", writers])
movie_information.append(["producers", producers])
movie_information.append(["cinematographers", cinematographers])
movie_information.append(["composers", composers])
movie_information.append(["editors", editors])
movie_information.append(["audience score", audience_score])

print(movie_information)
