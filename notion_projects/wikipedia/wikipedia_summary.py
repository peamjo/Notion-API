import wikipedia as wiki

def wiki_summary(search):
    try:
        result = wiki.search(search)
        page = wiki.page(result[0])
        summary = page.summary
    except:
        summary = None
    return summary

#print(wiki_summary("Cars"))
