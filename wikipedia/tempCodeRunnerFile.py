import re
import json
import string
from pathlib import Path
from import_requests import get_pages
from dotenv import load_dotenv
import os
from wikipedia_summary import wiki_summary
from property_exceptions import city_exceptions, country_exceptions, job_exception
from wiki_scraping_final import wiki_scrape_bot
from get_images import get_images, convert_to_jpg
from final_transfer import update_page, create_page, create_content
from face_recognition import face_recognition, majority_race_gender
from add_to_notion import add_text, add_number, add_select, add_multiselect, add_url, add_emoji, add_date