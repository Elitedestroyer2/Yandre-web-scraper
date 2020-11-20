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

    def send(self):
        if not hasattr(self, 'scrap'):
            self.scrap = scraper.scraper()
        self.scrap.grab_pictures()
    
    def add(self, characterName, amount, lewd, wholesome, duplicate):
        if characterName:
            self.conn.add_added_character(characterName, amount, lewd, wholesome, duplicate)
            #reset the view
            self.reset_view()
        else:
            pass
    
    def check_first_time_duplication(self):
        if settings.settings.get_first_duplication() == True:
            warning_text = 'This will dramatically increase the time to download pictures!!!'
            self.warning = gui_components.WarningModalView()
            self.warning.ids.warning_label.text = warning_text
            self.warning.open()


    def reset_view(self):
        App.get_running_app().root.ids.search_box.text = ''
        App.get_running_app().root.ids.amount.text = ''
        App.get_running_app().root.ids.lewd.state = 'normal'
        App.get_running_app().root.ids.wholesome.state = 'normal'
        App.get_running_app().root.ids.duplication.state = 'normal'
        
    def connectToDatabases(self):
        self.conn = charactermanager.dbConnection()
        self.conn.connect()

    def update_collection(self):
        collection = scraper.updateCollection()
        collection.update()

class ScraperApp(App):

    def build(self):
        return Launch()

def start_app():
    ScraperApp().run()

if __name__ == '__main__':
    ScraperApp().run()
