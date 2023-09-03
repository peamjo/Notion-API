name, url, property_name = process_input(movie_name)
        get_pages(database_id, topic)
        with open(str(Path.cwd().joinpath(topic +'-db.json')), encoding="utf8") as file:
            movies_pages = json.loads(file.read())["results"]
        movie_exist = check_pages(database_id, movies_pages, movie_name, topic)
        if movie_exist == False:
            description_data, cast_crew_data = get_movie_info(movie_name, database_id)
            movie_data, cover_data, icon_data, summary, template = process_movie_info(movie_name, database_id, description_data, cast_crew_data, topic)
            fast_create_movie(movie_data, cover_data, icon_data, database_id, template)
            print(f"{movie_name} has been added to the database")
        else:
            print(f"{movie_name} already exists in the database")
    """except KeyboardInterrupt: