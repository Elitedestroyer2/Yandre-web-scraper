import requests
from bs4 import BeautifulSoup


def set_character_url(self):
    return f'https://yande.re/post?page={self.pageCounter}&tags={self.character.name}'

def getPage_thumbnails(self):
    page = requests.get(self.character.url)
    pageContent = BeautifulSoup(page.content, 'html.parser')
    results = pageContent.find(id='post-list-posts')
    thumbnails = results.find_all('a', class_='thumb')
    return thumbnails


def getpage_download_and_saferating(self, href_element):
    page = requests.get(self.MAINURL + href_element)
    soup = BeautifulSoup(page.content, 'html.parser')
    download_link = soup.find(id='highres').attrs['href']
    safeRating = soup.find(id='stats').contents[3].contents[9].contents[0]
    return download_link, safeRating
