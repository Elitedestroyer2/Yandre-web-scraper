from database import DbManager


class CharacterDbManager(DbManager):
    from ._character_db_functions import (
        update_database, grab_added_character,
        delete_added_characters_from_table, table_empty,
        delete_added_charater_from_db, grab_suggestion_list,
        update_collection)


class FilterManager(object):
    from ._filters import (assign_filter_values, ratingCheck)


class PageManager(object):
    from ._get_page_info import (set_character_url, getPage_thumbnails,
                                 getpage_download_and_saferating)

class FileManager(object):
    from ._file_manager import (get_current_file_count, checkCharacterDir)

class DownloadManager(object):
    from ._downloader import (download_pictures, download)