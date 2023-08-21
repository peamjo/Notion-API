from final_transfer import update_page

def add_text():
    update_data = {"Years active": {"rich_text": [{"text": {"content": i[1]}}]}}
    update_page(page_id, update_data)
