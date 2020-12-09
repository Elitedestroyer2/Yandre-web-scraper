import requests
from bs4 import BeautifulSoup
from common import CommonClasses
from database import DbManager

page_counter_global = 0


def start_up(self):
    self.increment_page_counter()
    self.commonClasses = CommonClasses()
    self.grab_character_names_and_counts()
    self.add_characters_to_suggestions()

def reset_suggestion_table(self):
    self.dbManager.create_connection()
    self.dbManager.delete_suggestions_table()
    self.dbManager.create_suggestions_table()
    self.dbManager.close_connection()

def grab_character_names_and_counts(self):
    self.character = []
    done = False
    while not done:
        self.grab_html_data()
        for character_name_outer_html, character_count_outer_html in zip(self.character_names_outer_html, self.character_counts_outer_html):
            if int(character_count_outer_html.contents[0]) > 9:
                self.character.append(self.commonClasses.CharacterSuggestion(
                    str(character_name_outer_html.contents[3].contents[0]), str(character_count_outer_html.contents[0])))
            elif int(character_count_outer_html.contents[0]) < 10:
                done = True
                continue

def grab_html_data(self):
    page = requests.get(self.url)
    soup = BeautifulSoup(page.content, 'html.parser')
    self.character_names_outer_html = soup.findAll(
        'td', class_='tag-type-character')
    self.character_counts_outer_html = soup.findAll('td', align='right')
    self.increment_page_counter()

def increment_page_counter(self):
    global page_counter_global
    page_counter_global += 1
    self.url = f'https://yande.re/tag?commit=Search&name=&order=count&page={page_counter_global}&type=4'

def add_characters_to_suggestions(self):
    self.dbManager.create_connection()
    for character in self.character:
        self.dbManager.added_character_to_suggest_list([character.name, character.count])
    self.dbManager.close_connection()
