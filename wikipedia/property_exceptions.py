def city_exceptions(city):
    if city == "New York City":
        city = "NYC"
    return city

def country_exceptions(country):
    if country in ("Japan"):
        country = "Japan"
    if country in ("French"):
        country = "France"
    if country in ("German"):
        country = "Germany"
    if country in ('U.S.', 'US', 'United States', 'United States of America'):
        country = 'USA'
    if country in ('U.K.', 'UK', 'United Kingdom'):
        country = 'UK'
    return country

def movie_country_exceptions(country):
    if country in ("Japan"):
        country = "Japan"
    if country in ("French"):
        country = "France"
    if country in ("German"):
        country = "Germany"
    if country in ('U.S.', 'US', 'United States', 'United States of America'):
        country = 'Hollywood'
    if country in ('U.K.', 'UK'):
        country = 'United Kingdom'
    return country

def data_list_exception(data):
    if data in ("R", "B", "Rhythm And Blues"):
        data = "R&B"
    if data == "Edm":
        data = "EDM"
    if data in ("Dj", "Disc Jockey"):
        data = "DJ"
    if data == "Mc":
        data = "MC"
    if data == "Hiphop":
        data = "Hip Hop"  
    if data in ("Businesswoman", "Businessman", "Businessperson"):
        data = "Business Person"
    if data in ("Actress"):
        data = "Actor"
    return(data)

def job_exception(data):
    if data in ("Actress"):
        data = "Actor"
