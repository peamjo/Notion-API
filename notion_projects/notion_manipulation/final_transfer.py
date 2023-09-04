import requests
from datetime import datetime, timezone
from notion_manipulation.import_requests import get_pages
from dotenv import load_dotenv
import os
import base64

load_dotenv()
notion_token = os.getenv("NOTION_TOKEN")

HEADERS = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_page(data: dict, cover_data, icon_data, database_id, content):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": database_id}, "cover": cover_data, "icon": icon_data, "properties": data, "children": content}
    res = requests.post(create_url, headers=HEADERS, json=payload)
    #print("Create Page",res.status_code, res.text)
    return res

def populate_page_data(page_id: str, data: dict, cover_data, icon_data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"cover": cover_data, "icon": icon_data, "properties": data}
    res = requests.patch(url, headers=HEADERS, json=payload)
    #print("Populate Page Data", res.status_code, res.text)
    return res

def populate_content(block_id: str, content):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    payload = {"children": content}
    res = requests.patch(url, headers=HEADERS, json=payload)
    #print("Populate Content", res.status_code, res.text)
    return res

def update_content(block_id: str):
    url = f"https://api.notion.com/v1/blocks/{block_id}/"
    payload = {"children": content}
    res = requests.patch(url, headers=HEADERS, json=payload)
    print("Update Content", res.status_code, res.text)
    return res

def delete_content(block_id: str):
    url = f"https://api.notion.com/v1/blocks/{block_id}/"
    res = requests.delete(url, headers=HEADERS)
    #print("Delete Content", res.status_code, res.text)
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
    res = requests.patch(url, json=payload, headers=HEADERS)
    print("Update Page", res.status_code, res.text)
    return res

def update_cover_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    for key in data:
        payload = {"cover": data}
    res = requests.patch(url, json=payload, headers=HEADERS)
    print("Update Cover Page", res.status_code, res.text)
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
