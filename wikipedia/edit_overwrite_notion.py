from final_transfer import update_page, update_cover_page
from wikipedia_summary import wiki_summary

def overwrite_title(page, data):
    update_data = {"Name": {"title": [{"text": {"content": data}}]}}
    update_page(page["id"], update_data)

def edit_text(page, property, data):
    if page["properties"][property]["rich_text"] == []:
        update_data = {property: {"rich_text": [{"text": {"content": data}}]}}
        update_page(page["id"], update_data)

def overwrite_text(page, property, data):
    update_data = {property: {"rich_text": [{"text": {"content": data}}]}}
    update_page(page["id"], update_data)

def edit_number(page, property, data):
    if page["properties"][property]["number"] == None:
        update_data = {property: {"number": float(data)}}
        update_page(page["id"], update_data)

def overwrite_number(page, property, data):
    update_data = {property: {"number": float(data)}}
    update_page(page["id"], update_data)

def edit_select(page, property, data):
    if page["properties"][property]["select"] == None:
        update_data = {property: {"select": {"name": data}}}
        update_page(page["id"], update_data)

def overwrite_select(page, property, data):
    update_data = {property: {"select": {"name": data}}}
    update_page(page["id"], update_data)

def edit_multiselect(page, property, data):
    if page["properties"][property]["multi_select"] == []:
        property_list = []
        if isinstance(data, list):
            for j in data:
                j = {"name": j}
                property_list.append(j)
            update_data = {property: {"multi_select": property_list}}
        else:
            update_data = {property: {"multi_select": [{"name": data}]}}
        update_page(page["id"], update_data)

def overwrite_multiselect(page, property, data):
    property_list = []
    if isinstance(data, list):
        for j in data:
            j = {"name": j}
            property_list.append(j)
        update_data = {property: {"multi_select": property_list}}
    else:
        update_data = {property: {"multi_select": [{"name": data}]}}
    update_page(page["id"], update_data)

def edit_emoji(page, data):
    if page["icon"] == None:
        update_data = {"emoji": data}
        update_page(page["id"], update_data)

def overwrite_emoji(page, data):
    update_data = {"emoji": data}
    update_page(page["id"], update_data)

def edit_icon_image(page, data):
    if page["icon"] == None:
        update_data = {"external": {"url": data}}
        update_page(page["id"], update_data)

def overwrite_icon_image(page, data):
    update_data = {"external": {"url": data}}
    update_page(page["id"], update_data)

def edit_cover_image(page, data):
    if page["cover"] == None:
        update_data = {"external": {"url": data}}
        update_cover_page(page["id"], update_data)

def overwrite_cover_image(page, data):
    update_data = {"external": {"url": data}}
    update_cover_page(page["id"], update_data)

def edit_url(page, property, data):
    if page["properties"][property]["url"] == None:
        update_data = {property: {"url": data}}
        update_page(page["id"], update_data)

def overwrite_url(page, property, data):
    update_data = {property: {"url": data}}
    update_page(page["id"], update_data)

def edit_date(page, property, data):
    if page["properties"][property]["date"] == None:
        update_data = {property: {"date": {"start": data}}}
        update_page(page["id"], update_data)

def overwrite_date(page, property, data):
    update_data = {property: {"date": {"start": data}}}
    update_page(page["id"], update_data)

def overwrite_dates(page, property, data, date):
    update_data = {property: {"date": {"start": date, "end": data}}}
    update_page(page["id"], update_data)
