def city_exceptions(city):
    if city == "New York City":
        city = "NYC"
    return city

def country_exceptions(country):
    if country.find("Japan") != -1:
        country = "Japan"
    if country.find("French") != -1:
        i[1] = "France"
    if country.find("German") != -1:
        i[1] = "Germany"
    if country in ('U.S.', 'US', 'United States'):
        country = 'USA'
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
