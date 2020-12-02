import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


import settings
#from database import charactermanager

import multiprocessing
import threading
import concurrent.futures

from database import DbManager
from common import CommonClasses
from web_scraper._scraper import scraper

class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        self.dbManager = DbManager()
        self.commonClasses = CommonClasses()

    def send(self):
        #Kivy must stay on the main thread, other wise Kivy pauses
        self.start_gif()
        self.t2 = threading.Thread(target=self.download)
        self.t3 = threading.Thread(target=self.download)
        self.t4 = threading.Thread(target=self.download)
        self.t5 = threading.Thread(target=self.download)
        self.t2.start()
        self.t3.start()
        self.t4.start()
        self.t5.start()

        
    def download(self):
        #if not hasattr(self, 'scrap'):
        #    self.scrap = scraper.scraper()
        #self.scrap.grab_pictures()
        #self.scrap.start_threads()
        scrap = scraper.scraper()
        scrap.grab_pictures()

    def start_gif(self):
        self.workingmv = gui_components.WorkingModalView()
        self.workingmv.open()

    def check_if_done(self):
        while True:
            if not self.t2.is_alive():
                self.workingmv.dismiss()
                break

    def add(self, characterName, amount, lewd, wholesome, duplicate):
        if characterName:
            self.connectToDatabase()
            self.add_added_character(characterName, amount, lewd, wholesome, duplicate)
            self.close_database()
            #reset the view
            self.reset_view()
        else:
            pass
    
    def add_added_character(self, characterName, amount, lewd, wholesome, duplicate):
        character = (self.commonClasses.addedCharacter(characterName, amount = amount, lewd = lewd,
                            wholesome = wholesome, duplicate = duplicate))
        if not self.dbManager.check_added_character_exsits([character.name]):
            self.dbManager.enter_added_new_character([character.name, character.amount, character.lewd,
                                                character.wholesome, character.duplicate])
        else:
            self.dbManager.update_added_character_amount([character.amount, character.lewd,
                                                character.wholesome, character.duplicate, character.name])

    def check_first_time_duplication(self):
        if settings.settings.get_first_duplication():
            warning_text = 'This will dramatically increase the time to download pictures!!!'
            self.warning = gui_components.WarningModalView()
            self.warning.ids.warning_label.text = warning_text
            self.warning.open()
            settings.settings.first_duplication_warning_done()


    def reset_view(self):
        App.get_running_app().root.ids.search_box.text = ''
        App.get_running_app().root.ids.amount.text = ''
        App.get_running_app().root.ids.lewd.state = 'normal'
        App.get_running_app().root.ids.wholesome.state = 'normal'
        App.get_running_app().root.ids.duplication.state = 'normal'
        
    def connectToDatabase(self):
        self.dbManager.create_connection()

    def close_database(self):
        self.dbManager.close_connection()

    def update_collection(self):
        if self.sav_dir_check():
            collection = scraper.updateCollection()
            collection.update()
        else:
            self.sav_dir_warning()

    def sav_dir_check(self):
        if settings.settings.read_settings() != '':
            return True
        else:
            return False

    def sav_dir_warning(self):
        warning_text = 'Please choose a save directory!'
        self.warning = gui_components.WarningModalView()
        self.warning.ids.warning_label.text = warning_text
        self.warning.open()

    def update_suggestions(self):
        self.start_gif()
        self.t2 = threading.Thread(target=self.update_suggestions_workers)
        self.t3 = threading.Thread(target=self.update_suggestions_workers)
        self.t4 = threading.Thread(target=self.update_suggestions_workers)
        self.t5 = threading.Thread(target=self.update_suggestions_workers)
        self.t6 = threading.Thread(target=self.update_suggestions_workers)
        self.t7 = threading.Thread(target=self.update_suggestions_workers)
        self.t8 = threading.Thread(target=self.update_suggestions_workers)
        self.t9 = threading.Thread(target=self.update_suggestions_workers)
        self.t2.start()
        self.t3.start()
        self.t4.start()
        self.t5.start()
        self.t6.start()
        self.t7.start()
        self.t8.start()
        self.t9.start()

    def update_suggestions_workers(self):
        suggestions_updater = scraper.suggestionsUpdater()
        suggestions_updater.startUp()


class ScraperApp(App):

    def build(self):
        return Launch()

def start_app():
    ScraperApp().run()

if __name__ == '__main__':
    ScraperApp().run()
