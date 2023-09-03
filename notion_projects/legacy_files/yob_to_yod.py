import requests
from datetime import datetime, timezone
from import_requests import pages
from final_transfer import update_page

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": data}
    res = requests.patch(url, json=payload, headers=headers)
    return res

def yob_to_yod(page):
    page_id = page["id"]
    props = page["properties"]
    while True:        
        try:
            current_yob = props["YoB"]["rich_text"][0]["text"]["content"]
            if len(current_yob) > 4:
                new_yob = current_yob.split(' to ')[0]
                new_yod = current_yob.split(' to ')[1]
                update_data = {"YoD": {"rich_text": [{"text": {"content": new_yod}}]}}
                update_page(page_id, update_data)
                update_data = {"YoB": {"rich_text": [{"text": {"content": new_yob}}]}}
                update_page(page_id, update_data)
            break
        except IndexError:
            break
