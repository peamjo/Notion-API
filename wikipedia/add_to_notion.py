from final_transfer import update_page

def add_text(page_id, value, property):
    update_data = {value: {"rich_text": [{"text": {"content": property[1]}}]}}
    update_page(page_id, update_data)

def add_number(page_id, value, property):
    update_data = {value: {"number": int(property[1])}}
    update_page(page_id, update_data)

def add_select(page_id, value, property):
    update_data = {value: {"select": {"name": property[1]}}}
    update_page(page_id, update_data)

def add_multiselect(page_id, value, property):
    property_list = []
    if isinstance(property[1], list):
        for j in property[1]:
            j = {"name": j}
            property_list.append(j)
        update_data = {value: {"multi_select": property_list}}
    else:
        update_data = {value: {"multi_select": [{"name": property[1]}]}}
    update_page(page_id, update_data)

def add_emoji(page_id, property):
    update_data = {"emoji": property[1]}
    update_page(page_id, update_data)

def add_url(page_id, value, property):
    update_data = {value: {"url": property[1]}}
    update_page(page_id, update_data)

def add_birthday(page_id, value, property):
    update_data = {value: {"date": {"start": property[1]}}}
    update_page(page_id, update_data)
