from final_transfer import update_page, update_cover_page
from final_transfer import create_content
from wikipedia_summary import wiki_summary

def create_title(page, property, data, creation_data):
    update_data = {property: {"title": [{"text": {"content": data}}]}},
    creation_data += update_data

def create_text(page, property, data, creation_data):
    if page["properties"][property]["rich_text"] == []:
        update_data = {property: {"rich_text": [{"text": {"content": data}}]}},
        creation_data += update_data

def create_number(page, property, data, creation_data):
    if page["properties"][property]["number"] == None:
        update_data = {property: {"number": float(data)}},
        creation_data += update_data

def create_select(page, property, data, creation_data):
    if page["properties"][property]["select"] == None:
        update_data = {property: {"select": {"name": data}}},
        creation_data += update_data

def create_multiselect(page, property, data, creation_data):
    try:
        if page["properties"][property]["multi_select"] == []:
            property_list = []
            if isinstance(data, list):
                for j in data:
                    j = {"name": j}
                    property_list.append(j)
                update_data = {property: {"multi_select": property_list}},
            else:
                update_data = {property: {"multi_select": [{"name": data}]}},
            creation_data += update_data
    except:
        pass

def create_emoji(page, data, creation_data):
    if page["icon"] == None:
        update_data = {"emoji": data},
        creation_data += update_data

def create_icon_image(page, data, creation_data):
    if page["icon"] == None:
        update_data = {"external": {"url": data}},
        creation_data += update_data

def create_cover_image(page, data, creation_data):
    if page["cover"] == None:
        update_data = {"external": {"url": data}},
        creation_data += update_data

def create_url(page, property, data, creation_data):
    if page["properties"][property]["url"] == None:
        update_data = {property: {"url": data}},
        creation_data += update_data

def create_date(page, property, data, creation_data):
    if page["properties"][property]["date"] == None:
        update_data = {property: {"date": {"start": data}}},
        creation_data += update_data

def create_dates(page, property, data, date, creation_data):
    update_data = {property: {"date": {"start": date, "end": data}}},
    creation_data += update_data

def create_summary(page, name):
    summary = wiki_summary(name)
    try:
        if len(summary) > 1300:
            summary = summary[:1300]
            last_period = summary.rfind('.')
            summary = summary[:last_period+1]
        update_data = summary
        create_content(page["id"], update_data)
    except:
        pass
