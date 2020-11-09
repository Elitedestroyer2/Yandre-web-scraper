import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from scraper import grab_pictures, searchSuggest, set_path, start_up
import gui_components


class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        start_up()

    def send(self, lewd, wholesome, duplicate, search):
        grab_pictures(lewd, wholesome, duplicate, search)


class ScraperApp(App):

    def build(self):
        return Launch()


if __name__ == '__main__':
    ScraperApp().run()
