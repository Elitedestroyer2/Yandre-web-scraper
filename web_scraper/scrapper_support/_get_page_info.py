import requests
from bs4 import BeautifulSoup

def set_character_url(self, page_counter, character_name):
    return f'https://yande.re/post?page={page_counter}&tags={character_name}'

def getPage_thumbnails(self, character_url):
    page = requests.get(character_url)
    pageContent = BeautifulSoup(page.content, 'html.parser')
    results = pageContent.find(id='post-list-posts')
    thumbnails = results.find_all('a', class_='thumb')
    return thumbnails


def getpage_download_and_saferating(self, href_element):
    page = requests.get(self.main_url + href_element)
    soup = BeautifulSoup(page.content, 'html.parser')
    download_link = soup.find(id='highres').attrs['href']
    safeRating = soup.find(id='stats').contents[3].contents[9].contents[0]
    return download_link, safeRating
