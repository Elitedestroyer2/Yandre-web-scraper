import requests
from bs4 import BeautifulSoup
from common import CommonClasses
from database import DbManager

page_counter_global = 1


class suggestionsUpdater(object):

    def __init__(self):
        self.url = f'https://yande.re/tag?commit=Search&name=&order=count&page={page_counter_global}&type=4'

    def startUp(self):
        self.dbManager = DbManager()
        self.commonClasses = CommonClasses()
        self.reset_suggestion_table()
        self.grab_character_names_and_counts()
        self.add_characters_to_suggestions()

    def reset_suggestion_table(self):
        self.connect_to_database()
        self.conn.delete_suggestions_table()
        self.conn.create_suggestions_table()
        self.close_database()

    def connect_to_database(self):
        self.dbManager.create_connection()

    def close_database(self):
        self.dbManager.close_connection()

    def grab_character_names_and_counts(self):
        self.character = []
        done = False
        while not done:
            self.grab_html_data()
            for character_name_outer_html, character_count_outer_html in zip(self.character_names_outer_html, self.character_counts_outer_html):
                if int(character_count_outer_html.contents[0]) > 9:
                    self.character.append(commonClasses.CharacterSuggestion(
                        character_name_outer_html.contents[3].contents[0], character_count_outer_html.contents[0]))
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
        self.connect_to_database()
        for character in self.character:
            self.conn.added_character_to_suggest_list(character)
        self.close_database()
