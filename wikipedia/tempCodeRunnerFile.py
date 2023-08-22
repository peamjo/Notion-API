for cast in cast_list:
    actors.append(cast["name"])
for crew in crew_list:
    print(crew["job"])
    if crew["job"] == 'Director':
        directors.append(crew["name"])
        print("yay")
    if crew["job"] == 'Producer':
        producers.append(crew["name"])
    if crew["job"] == 'Director of Photography':
        cinematographers.append(crew["name"])