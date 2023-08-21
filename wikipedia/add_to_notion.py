from final_transfer import update_page

def add_text(value, property):
    update_data = {{value}: {"rich_text": [{"text": {"content": {property}[1]}}]}}
    update_page(page_id, update_data)

def add_number(value, property):
    update_data = {{value}: {"number": int({property}[1])}}
    update_page(page_id, update_data)

def add_select(value, property):
    update_data = {{value}: {"select": {"name": {property}[1]}}}
    update_page(page_id, update_data)

def add_multiselect(value, property):
    property_list = []
    for j in {property}[1]:
        j = {"name": j}
        property_list.append(j)
    update_data = {{value}: {"multi_select": property_list}}
    update_page(page_id, update_data)

def add_emoji(property):
    update_data = {"emoji": {property}[1]}
    update_page(page_id, update_data)

def add_url(value, property):
    update_data = {{value}: {"url": {property}[1]}}
    update_page(page_id, update_data)
