import requests
from datetime import datetime, timezone
from import_requests import get_pages

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

pages = get_pages()

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    for key in data:
        if key in ('emoji', 'external'):
            payload = {"icon": data}
            break
        else:
            payload = {"properties": data}
            break
    res = requests.patch(url, json=payload, headers=headers)
    return res

def create_content(page_id: str, data: str):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": data,}}]}}]}
    res = requests.patch(url, json=payload, headers=headers)
    return res


def date_to_yob(page):
    props = page["properties"]
    while True:        
        try:
            current_yob = props["YoB"]["rich_text"][0]["text"]["content"]
            # edit YoB & YoD
            if len(current_yob) > 4:
                new_yob = current_yob.split(' to ')[0]
                new_yod = current_yob.split(' to ')[1]
                update_data = {"YoD": {"rich_text": [{"text": {"content": new_yod}}]}}
                update_page(page_id, update_data)
                update_data = {"YoB": {"rich_text": [{"text": {"content": new_yob}}]}}
                update_page(page_id, update_data)
            break
        except IndexError:
            while True:
                try:
                    # move Date to YoB & YoD
                    current_date_start = props["Date"]["date"]["start"]
                    current_date_end = props["Date"]["date"]["end"]
                    update_data = {"YoB": {"rich_text": [{"text": {"content": current_date_start[:4]}}]}}
                    update_page(page_id, update_data)
                    update_data = {"YoD": {"rich_text": [{"text": {"content": current_date_end[:4]}}]}}
                    update_page(page_id, update_data)
                    break
                except TypeError:
                    break
            break
