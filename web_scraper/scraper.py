import concurrent

from common import CommonClasses
from settings import settings

from .scrapper_support import (CharacterDbManager, DownloadManager,
                               FileManager, FilterManager, PageManager)

page_counter_global = 1


class scraper(object):

    # not in use
    def start_threads(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executer:
            download_characters = {executer.submit(self.start_download, character): character for character in self.characters}

    def grab_pictures(self):
        self.MAINURL = "https://yande.re/"
        self.sav_dir = settings.read_settings()
        self.pageCounter = 1

        self.dbManager = CharacterDbManager()
        self.dbManager.update_collection()
        self.characters = self.dbManager.grab_added_character_table()
        self.characters = self.change_kivy_to_bool(self.characters)
        self.dbManager.create_connection()
        self.dbManager.delete_added_table()
        self.dbManager.create_added_table()
        self.dbManager.close_connection()
        self.start_threads()


    def change_kivy_to_bool(self, characters_sql):
        characters = []
        for character in characters_sql:
            if character.lewd == 'down':
                character.lewd = True
            else:
                character.lewd = False
            if character.wholesome == 'down':
                character.wholesome = True
            else:
                character.wholesome = False
            if character.duplicate == 'down':
                character.duplicate = True
            else:
                character.duplicate = False
            characters.append(character)
        return characters

    def start_download(self, character):
        downloader = Downloader(character)
        downloader.download()


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

        # check if directory exists, if not create one.
        self.fileManager.checkCharacterDir()
        self.folder_path = self.fileManager.get_folder_path()
        self.file_count = self.fileManager.get_current_file_count()
        self.stop_amount = self.character.amount + self.file_count
        while self.file_count < self.stop_amount:
            self.character.url = self.pageManager.set_character_url(self.pageCounter, self.character.name)
            thumb_nails = self.pageManager.getPage_thumbnails(self.character.url)
            self.downloadManager.download_pictures(self.file_count, self.stop_amount, self.folder_path)
            self.file_count = self.fileManager.get_current_file_count()
            self.pageCounter += 1
        self.dbManager.update_database(self.character.name, self.file_count)
        self.dbManager.update_collection()

    def initialize_managers(self):
        self.dbManager = CharacterDbManager()
        self.filterManager = FilterManager(self.character)
        self.commonClasses = CommonClasses()
        self.pageManager = PageManager(self.MAINURL)
        self.fileManager = FileManager(self.character, self.sav_dir)
        self.downloadManager = DownloadManager(self.character, self.MAINURL)