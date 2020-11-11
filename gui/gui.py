import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from scraper import grab_pictures, searchSuggest, set_path, start_up, add_character
import gui_components


class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        start_up()

    def send(self, lewd, wholesome, duplicate, search):
        grab_pictures(lewd, wholesome, duplicate, search)
    
    def add(self, characterName, amount):
        if characterName:
            add_character(characterName, amount)
            App.get_running_app().root.ids.search_box.text = ''
            App.get_running_app().root.ids.amount.text = ''
        else:
            pass


class ScraperApp(App):

    def build(self):
        return Launch()

if __name__ == '__main__':
    ScraperApp().run()
