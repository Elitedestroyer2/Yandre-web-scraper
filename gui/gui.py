import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from web_scraper import scraper
import settings
from gui import gui_components
from database import charactermanager


class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        self.connectToDatabases()

    def send(self, lewd, wholesome, duplicate):
        scraper.grab_pictures(lewd, wholesome, duplicate)
    
    def add(self, characterName, amount):
        if characterName:
            self.conn.add_character(characterName, amount)
            App.get_running_app().root.ids.search_box.text = ''
            App.get_running_app().root.ids.amount.text = ''
        else:
            pass

    def connectToDatabases(self):
        self.conn = charactermanager.dbConnection()
        self.conn.connect()


class ScraperApp(App):

    def build(self):
        return Launch()

def start_app():
    ScraperApp().run()

if __name__ == '__main__':
    ScraperApp().run()
