import requests
import json
from datetime import datetime, timezone

NOTION_TOKEN = "secret_SMfvYsCKecVMjPMQ2KsssmffUnyt7xF5XtMX8xfB2GP"

#DATABASE_ID = "9d6f4d0a5e664f409b12d999414b6986" #example people
#DATABASE_ID = "da11a187af89415493a0fd51bcd78d38" #example movies
#DATABASE_ID = "5b64a7e0e6ab4cb8b2844923bedcfc44" #list of movies
#DATABASE_ID = "42d0dfaed2c7453ab71e078efc252147" #example tv shows
DATABASE_ID = "2759f521c1594fc5864b55dd85abe85b" #example albums

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    number = 0
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
        number +=1
        print("page added", number)

    return results
