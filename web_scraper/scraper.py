

import concurrent

from common import CommonClasses
from settings import settings

from .scrapper_support import (CharacterDbManager, DownloadManager,
                               FileManager, FilterManager, PageManager)

page_counter_global = 1
updating_list = False


class scraper(object):

    # not in use
    def start_threads(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executer:
            download_characters = {executer.submit(self.grab_pictures): 8}

    def grab_pictures(self):
        global updating_list
        self.MAINURL = "https://yande.re/"
        self.sav_dir = settings.read_settings()
        self.pageCounter = 1

        # create character from character class
        self.initialize_managers()
        self.dbManager.update_collection()
        while not self.table_empty():
            self.dbManager.grab_added_character()
            if self.character == None:
                break
            self.dbManager.delete_added_charater_from_db()
            self.character = commonClasses.pageCharacter(self.character.name, self.pageManager.set_character_url(
                self.character.name), self.character.amount)
            # ? is this even need?
            self.filterManager.assign_filter_values()
            # check if directory exists, if not create one.
            self.fileManager.checkCharacterDir()
            self.fileManager.get_current_file_count()
            self.stopAmount = self.character.amount + self.fileCount
            self.downloadManager.download_pictures()
            self.dbManager.update_database()
            self.dbManager.update_collection()

    def initialize_managers(self):
        self.dbManager = CharacterDbManager()
        self.filterManager = FilterManager()
        self.commonClasses = CommonClasses()
        self.pageManager = PageManager()
        self.fileManager = FileManager()
        self.downloadManager = DownloadManager()

    # ?minor function

    def grab_default_values(self):
        amount, max_number, min_number = settings.get_default_values()
        return amount, max_number, min_number
