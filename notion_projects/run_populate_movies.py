from movies.movies import populate_existing_movies_in_notion
import time

def populate_movies():
    start = time.time()
    populate_existing_movies_in_notion()
    end = time.time()

    print(f"Time taken to run the code was {end-start} seconds")

if __name__ == '__main__':
    populate_movies()
