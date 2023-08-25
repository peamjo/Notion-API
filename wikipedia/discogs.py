import discogs_client
d = discogs_client.Client('my_user_agent/1.0', user_token='QdlrpDSmosznUjbQKLGFoVYsvrOefcMmHjlnCwRe')

results = d.search('Abbey Road', type='release,album')
#print(results.page(1))
artist_id=results[0].id
print(d.release(artist_id).fetch("extraartists"))

#artist = results[0].artists[0]
#print(artist.name)

#there's no album search
