import requests
import json
from add_to_notion import add_title, add_text, add_number, add_multiselect, add_date, add_select, add_dates, add_emoji
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

load_dotenv()
database_id = os.getenv("EXAMPLE_CARS_DATABASE_ID")
cars_client_id = os.getenv("CARS_CLIENT_ID")
cars_secret_id = os.getenv("CARS_SECRET_ID")

get_token_url = rf'https://carapi.app/api/auth/login'

headers = {
    "Accept": "application/json",
    "Authorization": rf"Bearer {cars_secret_id}"
}

response = requests.post(get_token_url)
data = response.json()
print(data)
token = data["access_token"]

cars_url = "https://carapi.app/api"

headers = {
    "Accept": "application/json",
    "Client-ID": cars_secret_id,
    "Authorization": rf"Bearer {token}"
}

#response = requests.get(cars_url, headers=headers)
#data = response.json()
