import concurrent

from common import CommonClasses
from settings import settings

from .scrapper_support import (CharacterDbManager, DownloadManager,
                               FileManager, FilterManager, PageManager)

page_counter_global = 1


class scraper(object):

    # not in use
    def start_threads(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executer:
            download_characters = {executer.submit(self.start_download, character): character for character in self.characters}

    def grab_pictures(self):
        self.MAINURL = "https://yande.re/"
        self.sav_dir = settings.read_settings()
        self.pageCounter = 1

        # create character from character class
        self.initialize_managers()
        self.dbManager.update_collection()
        self.characters = self.dbManager.grab_added_character_table()
        self.dbManager.create_connection()
        self.dbManager.delete_added_table()
        self.dbManager.create_added_table()
        self.dbManager.close_connection()
        #self.start_threads()
        self.start_download(self.characters[0])


    def start_download(self, character):
        downloader = Downloader(character)
        downloader.download()

        # old working solution:
        '''
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
            '''

    def initialize_managers(self):


        self.dbManager = CharacterDbManager()
        #self.filterManager = FilterManager()
        #self.commonClasses = CommonClasses()
        #self.pageManager = PageManager()
        #self.fileManager = FileManager()
        #self.downloadManager = DownloadManager()

    # ?minor function

    def grab_default_values(self):
        amount, max_number, min_number = settings.get_default_values()
        return amount, max_number, min_number


class Downloader(object):

    def __init__(self, character):
        self.character = character

    def download(self):
        self.MAINURL = "https://yande.re/"
        self.sav_dir = settings.read_settings()
        self.pageCounter = 1



        self.initialize_managers()
        self.character.url = self.pageManager.set_character_url(self.pageCounter, self.character.name)
        # check if directory exists, if not create one.
        self.fileManager.checkCharacterDir()
        self.folder_path = self.fileManager.get_folder_path()
        self.file_count = self.fileManager.get_current_file_count()
        self.stop_amount = self.character.amount + self.file_count
        while self.file_count <= self.stop_amount:
            thumb_nails = self.pageManager.getPage_thumbnails(self.character.url)
            self.downloadManager.download_pictures(self.file_count, self.stop_amount, self.folder_path)
            self.file_count = self.fileManager.get_current_file_count()
            self.pageCounter += 1
            self.character.url = self.pageManager.set_character_url(self.pageCounter, self.character.name)
        self.dbManager.update_database()
        self.dbManager.update_collection()

    def initialize_managers(self):
        self.dbManager = CharacterDbManager()
        self.filterManager = FilterManager(self.character)
        self.commonClasses = CommonClasses()
        self.pageManager = PageManager(self.MAINURL)
        self.fileManager = FileManager(self.character, self.sav_dir)
        self.downloadManager = DownloadManager(self.character, self.MAINURL)