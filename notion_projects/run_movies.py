import os
import time

from dotenv import load_dotenv
from movies.movies import create_movies_in_notion, populate_existing_movies_in_notion
from notion_manipulation.import_contents import get_content


def create_movies():
    create_movies_in_notion(["Coco"])

def populate_movies():
    populate_existing_movies_in_notion()

def get_content_children():
    load_dotenv()
    database_id = os.getenv("EXAMPLE_MOVIES_DATABASE_ID")
    topic = "movies"
    get_content("7f6c995f-27ec-4d90-8c07-97c23af8c19c", topic)

if __name__ == '__main__':
    start = time.time()

    #create_movies()
    populate_movies()
    #get_content_children()
    
    end = time.time()
    print(f"Time taken to run the code was {end-start} seconds")
