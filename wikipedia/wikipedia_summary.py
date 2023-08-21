import wikipedia as wiki

def wiki_summary(search):
    try:
        result = wiki.search(search)
        page = wiki.page(result[0])
        summary = (page.summary)
    except (wiki.exceptions.PageError, wiki.exceptions.DisambiguationError) as e:
        summary = None
    return(summary)
