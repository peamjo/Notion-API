import wptools
so = wptools.page('Stack Overflow').get_parse()
infobox = so.data['infobox']
print(infobox)
