import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


from settings import settings
#from database import charactermanager

import multiprocessing
import threading
import concurrent.futures

from database import DbManager
from common import CommonClasses
from web_scraper import scraper

from web_scraper.scrapper_support import CharacterDbManager
import os
from gui.gui_componets.modal_views.working_modal_view.working_modal_view import WorkingModalView
from gui.gui_componets.modal_views.warning_modal_view.warning_modal_view import WarningModalView


class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        self.dbManager = DbManager()
        self.characterDbManager = CharacterDbManager()
        self.commonClasses = CommonClasses()
        self.grab_default_values()

    def grab_default_values(self):
        self.default_values = settings.get_default_values()

    def wholesome_toggle_init(self):
        wholesome = settings.get_default_values().wholesome
        return wholesome

    def lewd_toggle_init(self):
        lewd = settings.get_default_values().lewd
        return lewd

    def duplication_toggle_init(self):
        duplication = settings.get_default_values().duplication
        return duplication

    def send(self):
        # Kivy must stay on the main thread, other wise Kivy pauses
        self.check_if_all()
        self.start_gif()
        self.t2 = threading.Thread(target=self.download)
        #self.t3 = threading.Thread(target=self.download)
        #self.t4 = threading.Thread(target=self.download)
        #self.t5 = threading.Thread(target=self.download)
        self.t2.start()
        #self.t3.start()
        #self.t4.start()
        #self.t5.start()

    def grab_suggestion_list(self):
        self.dbManager.create_connection()
        character_sql = list(self.dbManager.grab_suggestion_list())
        self.dbManager.delete_added_table()
        self.dbManager.create_added_table()
        amount, max_number, min_number = settings.get_default_values()
        for character in character_sql:
            if int(character[1]) < min_number:
                pass
            else:
                character = CommonClasses.AddedCharacter(
                    character[0], False, True, False, amount, '')
                self.dbManager.enter_added_new_character([character.name, character.amount, character.lewd,
                                                          character.wholesome, character.duplicate])
        self.dbManager.close_connection()

    def check_if_all(self):
        self.characterDbManager.create_connection()
        character = list(self.characterDbManager.get_added_character())
        self.characterDbManager.close_connection()
        for c in character:
            character = c
        if character[0] == 'ALL':
            self.grab_suggestion_list()

    def download(self):
        # if not hasattr(self, 'scrap'):
        #    self.scrap = scraper.scraper()
        # self.scrap.grab_pictures()
        # self.scrap.start_threads()
        scrap = scraper.scraper()
        scrap.grab_pictures()

    def start_gif(self):
        self.workingmv = WorkingModalView()
        self.workingmv.open()

    def check_if_done(self):
        while True:
            if not self.t2.is_alive():
                self.workingmv.dismiss()
                break

    def add(self, characterName, amount, lewd, wholesome, duplicate):
        if characterName:
            self.add_added_character(
                characterName, amount, lewd, wholesome, duplicate)
            # reset the view
            self.reset_view()
        else:
            pass

    def add_added_character(self, characterName, amount, lewd, wholesome, duplicate):
        character = (self.commonClasses.AddedCharacter(characterName, amount=amount, lewd=lewd,
                                                       wholesome=wholesome, duplicate=duplicate))
        self.connectToDatabase()
        if not self.dbManager.check_added_character_exists([character.name]):
            self.dbManager.enter_added_new_character([character.name, character.amount, character.lewd,
                                                      character.wholesome, character.duplicate])
        else:
            self.dbManager.update_added_character([character.amount, character.lewd,
                                                          character.wholesome, character.duplicate, character.name])
        self.close_database()

    def check_first_time_duplication(self):
        if settings.get_first_duplication():
            warning_text = 'This will dramatically increase the time to download pictures!!!'
            self.warning = WarningModalView()
            self.warning.ids.warning_label.text = warning_text
            self.warning.open()
            settings.first_duplication_warning_done()

    def reset_view(self):
        App.get_running_app().root.ids.search_box.text = ''
        App.get_running_app().root.ids.amount.text = ''
        App.get_running_app().root.ids.lewd.state = self.default_values.lewd
        App.get_running_app().root.ids.wholesome.state = self.default_values.wholesome
        App.get_running_app().root.ids.duplication.state = self.default_values.duplication

    def connectToDatabase(self):
        self.dbManager.create_connection()

    def close_database(self):
        self.dbManager.close_connection()

    def update_collection(self):
        if self.sav_dir_check():
            collection = self.update_collection()
        else:
            self.sav_dir_warning()

    def sav_dir_check(self):
        if settings.settings.read_settings() != '':
            return True
        else:
            return False

    def update_collection(self):
        self.connectToDatabase()
        self.sav_dir = settings.read_settings()
        list_folders = os.listdir(self.sav_dir)
        self.dbManager.delete_table()
        self.dbManager.create_table()
        for folder in list_folders:
            folder_path = self.get_folder_path(self.sav_dir, folder)
            amount_of_pics_in_folder = len(next(os.walk(folder_path))[2])
            self.dbManager.add_character(folder, amount_of_pics_in_folder)
        self.close_database()

    def sav_dir_warning(self):
        warning_text = 'Please choose a save directory!'
        self.warning = WarningModalView()
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
