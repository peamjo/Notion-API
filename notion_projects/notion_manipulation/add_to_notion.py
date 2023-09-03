from final_transfer import update_page, update_cover_page

def add_title(page, value, property):
    update_data = {value: {"title": [{"text": {"content": property[1]}}]}}
    update_page(page["id"], update_data)

def add_text(page, value, property):
    if page["properties"][value]["rich_text"] == []:
        update_data = {value: {"rich_text": [{"text": {"content": property[1]}}]}}
        update_page(page["id"], update_data)

def add_number(page, value, property):
    if page["properties"][value]["number"] == None:
        update_data = {value: {"number": float(property[1])}}
        update_page(page["id"], update_data)

def add_select(page, value, property):
    if page["properties"][value]["select"] == None:
        update_data = {value: {"select": {"name": property[1]}}}
        update_page(page["id"], update_data)

def add_multiselect(page, value, property):
    if page["properties"][value]["multi_select"] == []:
        property_list = []
        if isinstance(property[1], list):
            for j in property[1]:
                j = {"name": j}
                property_list.append(j)
            update_data = {value: {"multi_select": property_list}}
        else:
            update_data = {value: {"multi_select": [{"name": property[1]}]}}
        update_page(page["id"], update_data)

def add_emoji(page, property):
    if page["icon"] == None:
        update_data = {"emoji": property[1]}
        update_page(page["id"], update_data)

def add_icon_image(page, property):
    if page["icon"] == None:
        update_data = {"external": {"url": property[1]}}
        update_page(page["id"], update_data)

def add_cover_image(page, property):
    if page["cover"] == None:
        update_data = {"external": {"url": property[1]}}
        update_cover_page(page["id"], update_data)

def add_url(page, value, property):
    if page["properties"][value]["url"] == None:
        update_data = {value: {"url": property[1]}}
        update_page(page["id"], update_data)

def add_date(page, value, property):
    if page["properties"][value]["date"] == None:
        update_data = {value: {"date": {"start": property[1]}}}
        update_page(page["id"], update_data)

def add_dates(page, value, property, date):
    update_data = {value: {"date": {"start": date, "end": property[1]}}}
    update_page(page["id"], update_data)
