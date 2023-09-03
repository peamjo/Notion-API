from movies.movies import create_movies_in_notion
import time

def create_movies():
    start = time.time()
    create_movies_in_notion(["Encanto"])
    end = time.time()

    print(f"Time taken to run the code was {end-start} seconds")

if __name__ == '__main__':
    create_movies()
