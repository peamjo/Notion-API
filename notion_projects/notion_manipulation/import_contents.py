import requests
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from pathlib import Path


def get_content(block_id, topic, num_pages=None):
    load_dotenv()
    notion_token = os.getenv("NOTION_TOKEN")

    HEADERS = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"

    response = requests.get(url, headers=HEADERS)

    data = response.json()

    with open(str(Path.cwd().joinpath('Notion-API','notion_projects', 'movies', 'movies_databases', topic + '-content-db.json')), 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    return results
