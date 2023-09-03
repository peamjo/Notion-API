import requests
import json
from new_add_to_notion import add_title, add_text, add_number, add_multiselect, add_date, add_select, add_dates, add_emoji
from get_info import input_names
from import_requests import get_pages
from final_transfer import update_page, create_page, create_content
from dotenv import load_dotenv
import os
from wikipedia_summary import wiki_summary
from property_exceptions import country_exceptions
from pathlib import Path
import random
import emoji
from datetime import datetime
from iso3166 import countries
from property_exceptions import country_exceptions

load_dotenv()
database_id = os.getenv("EXAMPLE_GAMES_DATABASE_ID")
client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")

#games_information = [[games_name]]
games_list = []
game_name = "Overwatch"

get_token_url = rf'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'

response = requests.post(get_token_url)
data = response.json()
token = data["access_token"]

headers = {
    "Accept": "application/json",
    "Client-ID": client_id,
    "Authorization": rf"Bearer {token}"
}

get_game_id = rf"https://api.igdb.com/v4/games/?search={game_name}&fields=id,name"
response = requests.get(get_game_id, headers=headers)
data = response.json()
for page in data:
        game_id = page["id"]
        break
#print(game_id)

get_games_url = rf"https://api.igdb.com/v4/games/{game_id}?fields=name,genres.name,game_engines.name,cover.url,franchises.name,game_modes.name,platforms.name,player_perspectives.name,total_rating,first_release_date,storyline,url,dlcs.name,themes.name,involved_companies.company.name,involved_companies.company.country,involved_companies.developer,involved_companies.publisher,screenshots.url"

response = requests.get(get_games_url, headers=headers)
data = response.json()
print(data)

cover_url = "https:"+(data[0]["cover"]["url"]).replace("thumb","720p")
screenshot_url = "https:"+(data[0]["screenshots"][0]["url"]).replace("thumb","original")
release_date = (str(datetime.utcfromtimestamp(data[0]["first_release_date"])).split(' '))[0]
companies = []
developers = []
publishers = []
for company in data[0]["involved_companies"]:
    if company["developer"] == True:
        companies.append(country_exceptions((countries.get(company["company"]["country"])).name))
        developers.append(company["company"]["name"])
    if company["publisher"] == True:
        publishers.append(company["company"]["name"])

#for game in games_list:
        #try:
