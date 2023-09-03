import base64
import json
import os
import re
import string
from pathlib import Path

from add_to_notion import (add_cover_image, add_date, add_icon_image,
                           add_multiselect, add_number, add_select, add_text,
                           add_url)
from dotenv import load_dotenv
from face_recognition import face_recognition, majority_race_gender
from final_transfer import create_content, create_page, update_page
from get_images import convert_to_jpg, get_images
from import_requests import get_pages
from spotify_request import (get_album, get_album_tracks, get_token,
                           search_for_album)
from property_exceptions import (city_exceptions, country_exceptions,
                                 job_exception)
from requests import get, post
from wiki_scraping_final import wiki_scrape_bot
from wikipedia_summary import wiki_summary
from notion_functions import *


#input_name = input_names("Search: ")
def process_input(input_name):
    name = input_name
    lists = name.split()
    word = "_".join(lists)
    url = "https://en.wikipedia.org/wiki/" + word
    return name, url

def get_info(data, name, url):
    info = []
    for property in (data):
        if property[0] in ("Genres", "Genre"):
            info.append(['Genre(s)', property[1]])
        if property[0] == "Recorded":
            info.append(['Recorded', property[1].replace("–", " to ").replace("-", " to ").replace("  ", " ")])
        if property[0] == "Length":
            info.append(['Length', property[1].replace(":", ".")])
        if property[0] == "Producer" and (property[1].count(" ") == 1):
            info.append(['Producer', property[1]])
    token = get_token()
    result = search_for_album(token, name)
    album_id = result["id"]
    album = get_album(token, album_id)

    info.append(['Wiki', url])
    info.append(['Artist(s)', album["artists"][0]["name"]])
    info.append(['Icon Image', album["images"][0]["url"]])
    info.append(['Label(s)', album["label"].split("/")])
    info.append(['Track(s)', album["total_tracks"]])
    info.append(['Release Date', album["release_date"]])
    album_tracks = get_album_tracks(token, album_id)
    track_names = []
    for track in range(album["total_tracks"]):
        track_names.append(album_tracks["items"][track]["name"])
    info.append(['Track Names', track_names])
    info.append(['Album Name', album["name"]])
    return(info)

def edit_data(individual, pages, info, url):
    for page in pages:
        page_id = page["id"]
        query_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        if query_name == individual:
            for property in info:
                if property[0] == 'Icon Image': 
                    add_icon_image(page, property)
                    add_cover_image(page, property)
                if property[0] == 'Recorded': add_text(page, "Recorded", property)
                if property[0] == 'Wiki': add_url(page, "Wiki", property)
                if property[0] == 'Genre(s)': add_multiselect(page, "Genre(s)", property)
                if property[0] == 'Artist(s)': add_multiselect(page, "Artist(s)", property)
                if property[0] == 'Label(s)': add_multiselect(page, "Label(s)", property)
                if property[0] == 'Track(s)': add_number(page, "Track(s)", property)
                if property[0] == 'Length': add_number(page, "Length (mins)", property)
                if property[0] == 'Release Date': add_date(page, "Release Date", property)
                if property[0] == 'Producer': add_multiselect(page, "Producer(s)", property)
                if property[0] == 'Track Names':
                    summary = wiki_summary((url.split("/")[-1]).replace("_"," "))
                    try:
                        if len(summary) > 1300:
                            summary = summary[:1300]
                            last_period = summary.rfind('.')
                            summary = summary[:last_period+1]
                        update_data = summary + f"\n\n" + str(property[1]).replace("[","").replace("]","").replace("'","").replace('"',"").replace(", ",f"\n")
                        create_content(page_id, update_data)
                    except:
                        update_data = str(property[1]).replace("[","").replace("]","").replace("'","").replace('"',"").replace(", ",f"\n")
                        create_content(page_id, update_data)

def check_for_wiki_url(url, people, artist, counter):
    og_url = url
    data = []
    data = wiki_scrape_bot(url)
    if data == []:
        url = r"https://en.wikipedia.org/wiki/"+people+"_("+artist[counter].replace(" ","_")+"_album)"
        data = wiki_scrape_bot(url)
    if data == []:
        url = r"https://en.wikipedia.org/wiki/"+people+"_("+artist[counter].replace(" ","_")+"_EP)"
        data = wiki_scrape_bot(url)
    if data == []:
        url = og_url + "_(album)"
        data = wiki_scrape_bot(url)
    if data == []:
        url = og_url + "_(EP)"
        data = wiki_scrape_bot(url)
    if data == []:
        return og_url, data
    return url, data

def add_or_edit_notion_wiki(people_list, artist=[""]):
    load_dotenv()
    database_id = os.getenv("EXAMPLE_ALBUMS_DATABASE_ID")
    job = []
    error_list = []

    for counter, people in enumerate(people_list):
        try:
            name, url = process_input(people)
            url, data = check_for_wiki_url(url, people, artist, counter)
            if artist[counter] != "":
                name = name + " (" + artist[counter] + ")"
            info = get_info(data, name, url)
            album_name = (info[-1])[1]
            property_name = {
            "Name": {"title": [{"text": {"content": album_name}}]},
            }
            print("Final List: ", info)
            pages = add_or_check_pages(database_id, album_name, property_name)
            edit_data(album_name, pages, info, url)
        except KeyboardInterrupt:
            break
        #except:
        #    error_list.append(people)
        #   continue
    
    if error_list != []:
        print("Error List:", error_list)

add_or_edit_notion_wiki(["24K Magic"],["Bruno Mars"])
