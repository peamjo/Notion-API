import ast
import json
import os
import random
import re
from pathlib import Path

import emoji
import requests
from dotenv import load_dotenv
from final_transfer import create_page, update_page, populate_page_data
from import_requests import get_pages
from edit_overwrite_notion import *
from create_notion import *
from notion_functions import *
from property_exceptions import movie_country_exceptions, language_exceptions
from wikipedia_summary import wiki_summary
from import_contents import get_content

load_dotenv()
database_id = os.getenv("EXAMPLE_MOVIES_DATABASE_ID")
not_found_list=[]
error_list = []
topic = "movies"

get_content("552ec313-21da-4c98-b1ad-d7dc2f3bd7ec", topic)
