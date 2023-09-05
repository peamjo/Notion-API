import requests
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from pathlib import Path

def get_pages(database_id, topic, num_pages=None):
    load_dotenv()
    notion_token = os.getenv("NOTION_TOKEN")

    HEADERS = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=HEADERS)

    data = response.json()

    with open(str(Path.cwd().joinpath('notion_projects', 'movies', 'movies_databases', topic + '-db.json')), 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    number = 0
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(url, json=payload, headers=HEADERS)
        data = response.json()
        results.extend(data["results"])
        number +=1
        print(str(number*100) + "+" + " pages added")

    return results
