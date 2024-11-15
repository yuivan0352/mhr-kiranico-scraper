import requests
import sys
from bs4 import BeautifulSoup

def scrapePage():
    URL = "https://mhrise.kiranico.com/"
    page = requests.get(URL)
    page = page.text.encode('ascii', 'ignore').decode('ascii')

    soup = BeautifulSoup(page, "html.parser")
    return soup

currentPage = scrapePage()

links = {}
linkKeywords = {"armors?", "weapons?", "material", "view=lg", "view=event", "view=hub_high", "view=hub_low", "view=hub_master", "view=mystery"}

for link in currentPage.find_all('a'):
    linkString = str(link.get('href'))
    if (linkString.find("data") != -1):
        for word in linkKeywords:
            if (linkString.find(word) != -1):
                links.setdefault(link.get_text(), link.get('href'))

links = sorted(links.items(), key=lambda item: item[1])

for link in links:
    print(link)

