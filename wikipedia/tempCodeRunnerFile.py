page_id = page["id"]
        query_name = page["properties"]["Name"]["title"][0]["text"]["content"]
        if query_name == individual:
            for property in info:
                if property[0] == 'showrunner': add_multiselect(page, "Creator(s)", property)                   
                if property[0] == 'channels': add_multiselect(page, "Channel(s)", property)
                if property[0] == 'decades': add_multiselect(page, "Decade(s)", property)
                if property[0] == 'genres': add_multiselect(page, "Genre(s)", property)
                if property[0] == 'languages': add_multiselect(page, "Language(s)", property)
                if property[0] == 'countries': add_multiselect(page, "Country", property)
                if property[0] == 'production companies': add_multiselect(page, "Production Company", property)
                if property[0] == 'actors': add_multiselect(page, "Starring", property)
                if property[0] == 'runtime': add_number(page, "Runtime (mins)", property)
                if property[0] == 'season(s)': add_number(page, "Season(s)", property)
                if property[0] == 'episode(s)': add_number(page, "Episode(s)", property)
                if property[0] == 'first episode': 
                    add_date(page, "Date Released", property) 
                    date = property[1]
                if property[0] == 'last episode': add_dates(page, "Date Released", property, date)
            summary = wiki_summary(name)    
            try:
                if len(summary) > 1300:
                    summary = summary[:1300]
                    last_period = summary.rfind('.')
                    summary = summary[:last_period+1]
                update_data = summary
                create_content(page_id, update_data)
            except:
                pass
            with open(str(Path.cwd().joinpath('wikipedia','quoted_emojis.txt')), encoding="utf8") as f:
                data = f.read()
                random_emoji=random.randrange(0, len(data))
                add_emoji(page, [0, data[random_emoji]])