from database import DbManager


class CharacterDbManager(DbManager):
    from ._character_db_functions import (
        update_database, grab_added_character,
        delete_added_characters_from_table, table_empty,
        delete_added_charater_from_db, grab_suggestion_list,
        update_collection, grab_added_character_table)


class FilterManager(object):
    def __init__(self, character):
        self.character = character

    from ._filters import (ratingCheck)


class PageManager(object):
    def __init__(self, main_url):
        self.main_url = main_url

    from ._get_page_info import (set_character_url, getPage_thumbnails,
                                 getpage_download_and_saferating)

class FileManager(object):
    def __init__(self, character, sav_dir):
        self.character = character
        self.sav_dir = sav_dir

    from ._file_manager import (get_current_file_count, checkCharacterDir, get_folder_path)

class DownloadManager(object):
    def __init__(self, character, main_url):
        self.character = character
        self.pageManager = PageManager(main_url)
        self.filterManager = FilterManager(character)

    from ._downloader import (download_pictures, download)