import requests
import string
from bs4 import BeautifulSoup

Enter_input = input("Search: ")
u_i = string.capwords(Enter_input)
lists = u_i.split()
word = "_".join(lists)

url = "https://en.wikipedia.org/wiki/" + word

def wikibot(url):
    url_open = requests.get(url)
    soup = BeautifulSoup(url_open.content, 'html.parser')
    details = soup('table', {'class': 'infobox'})
    for i in details:
        rows = i.find_all('tr')
        for row in rows:
            header = row.find_all('th')
            data = row.find_all('td')
            if header is not None and data is not None:
                for x,y in zip(header,data):
                    print("{} : {}".format(x.text,y.text))
                    print("----------------")
    #for i in range (1,3):
    #    print(soup('p')[i].text)

wikibot(url)
