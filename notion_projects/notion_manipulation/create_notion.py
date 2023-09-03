from notion_manipulation.final_transfer import update_page, update_cover_page
from wikipedia.wikipedia_summary import wiki_summary

def create_title(property, data):
    update_data = str({property: {"title": [{"text": {"content": data}}]}})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

def create_text(property, data):
    update_data = str({property: {"rich_text": [{"text": {"content": data}}]}})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

def create_number(property, data):
    update_data = str({property: {"number": float(data)}})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

def create_select(property, data):
    update_data = str({property: {"select": {"name": data}}})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

def create_multiselect(property, data):
    try:
        property_list = []
        if isinstance(data, list):
            for j in data:
                j = {"name": j}
                property_list.append(j)
            update_data = str({property: {"multi_select": property_list}})   
        else:
            update_data = str({property: {"multi_select": [{"name": data}]}})
        creation_data = update_data[1:len(update_data)-1] + ","
        return creation_data    
    except:
        pass

def create_emoji(data):
    update_data = str({"emoji": data})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

def create_url(property, data):
    update_data = str({property: {"url": data}})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

def create_date(property, data):
    update_data = str({property: {"date": {"start": data}}})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

def create_dates(property, data, date):
    update_data = str({property: {"date": {"start": date, "end": data}}})
    creation_data = update_data[1:len(update_data)-1] + ","
    return creation_data

#functions below this line does NOT add to properties

def create_icon_image(data):
    update_data = str({"external": {"url": data}})
    creation_data = update_data[1:len(update_data)-1]
    return creation_data

def create_cover_image(data):
    update_data = str({"external": {"url": data}})
    creation_data = update_data[1:len(update_data)-1]
    return creation_data

def create_media_block(name, description):
    update_data = str({
        "children": [
        {
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": description}}]}}]})
    creation_data = update_data[14:len(update_data)-2]
    return creation_data

def create_wiki_summary(name):
    summary = wiki_summary(name)
    try:
        if len(summary) > 1300:
            summary = summary[:1300]
            last_period = summary.rfind('.')
            summary = summary[:last_period+1]
    except:
        pass
    update_data = str({
        "children": [
        {
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": summary}}]}}]})
    creation_data = update_data[14:len(update_data)-2]
    return creation_data
