from final_transfer import update_page, update_cover_page
from wikipedia_summary import wiki_summary

def create_title(property, data, creation_data):
    update_data = str({property: {"title": [{"text": {"content": data}}]}})
    creation_data += update_data[1:len(update_data)-1] + ","
    return creation_data

def create_text(property, data, creation_data):
    update_data = str({property: {"rich_text": [{"text": {"content": data}}]}})
    creation_data += update_data[1:len(update_data)-1] + ","
    return creation_data

def create_number(property, data, creation_data):
    update_data = str({property: {"number": float(data)}})
    creation_data += update_data[1:len(update_data)-1] + ","
    return creation_data

def create_select(property, data, creation_data):
    update_data = str({property: {"select": {"name": data}}})
    creation_data += update_data[1:len(update_data)-1] + ","
    return creation_data

def create_multiselect(property, data, creation_data):
    try:
        property_list = []
        if isinstance(data, list):
            for j in data:
                j = {"name": j}
                property_list.append(j)
            update_data = str({property: {"multi_select": property_list}})   
        else:
            update_data = str({property: {"multi_select": [{"name": data}]}})
        creation_data += update_data[1:len(update_data)-1] + ","
        return creation_data    
    except:
        pass

def create_emoji(data, creation_data):
    update_data = str({"emoji": data})
    creation_data += update_data[1:len(update_data)-1] + ","
    return creation_data

def create_url(property, data, creation_data):
    update_data = str({property: {"url": data}})
    creation_data += update_data[1:len(update_data)-1] + ","
    return creation_data

def create_date(property, data, creation_data):
    update_data = str({property: {"date": {"start": data}}})
    creation_data += update_data[1:len(update_data)-1] + ","
    return creation_data

def create_dates(property, data, date, creation_data):
    update_data = str({property: {"date": {"start": date, "end": data}}})
    creation_data += update_data[1:len(update_data)-1] + ","
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

def create_summary(name, description="There is no summary available"):
    summary = wiki_summary(name)
    try:
        if len(summary) > 1300:
            summary = summary[:1300]
            last_period = summary.rfind('.')
            summary = summary[:last_period+1]
        summary = summary + "\n" + description
    except:
        summary = description
    update_data = str({
        "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": summary}}]}}]})
    creation_data = update_data[14:len(update_data)-2]
    return creation_data
