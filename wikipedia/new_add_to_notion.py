from final_transfer import update_page, update_cover_page

def add_title(page, property, data):
    update_data = {property: {"title": [{"text": {"content": data}}]}}
    update_page(page["id"], update_data)

def add_text(page, property, data):
    if page["properties"][property]["rich_text"] == []:
        update_data = {property: {"rich_text": [{"text": {"content": data}}]}}
        update_page(page["id"], update_data)

def add_number(page, property, data):
    if page["properties"][property]["number"] == None:
        update_data = {property: {"number": float(data)}}
        update_page(page["id"], update_data)

def add_select(page, property, data):
    if page["properties"][property]["select"] == None:
        update_data = {property: {"select": {"name": data}}}
        update_page(page["id"], update_data)

def add_multiselect(page, property, data):
    if page["properties"][property]["multi_select"] == []:
        property_list = []
        if isinstance(data[1], list):
            for j in data[1]:
                j = {"name": j}
                property_list.append(j)
            update_data = {property: {"multi_select": property_list}}
        else:
            update_data = {property: {"multi_select": [{"name": data[1]}]}}
        update_page(page["id"], update_data)

def add_emoji(page, data):
    if page["icon"] == None:
        update_data = {"emoji": data}
        update_page(page["id"], update_data)

def add_icon_image(page, data):
    if page["icon"] == None:
        update_data = {"external": {"url": data}}
        update_page(page["id"], update_data)

def add_cover_image(page, data):
    if page["cover"] == None:
        update_data = {"external": {"url": data}}
        update_cover_page(page["id"], update_data)

def add_url(page, property, data):
    if page["properties"][property]["url"] == None:
        update_data = {property: {"url": data}}
        update_page(page["id"], update_data)

def add_date(page, property, data):
    if page["properties"][property]["date"] == None:
        update_data = {property: {"date": {"start": data}}}
        update_page(page["id"], update_data)

def add_dates(page, property, data, date):
    update_data = {property: {"date": {"start": date, "end": data}}}
    update_page(page["id"], update_data)
