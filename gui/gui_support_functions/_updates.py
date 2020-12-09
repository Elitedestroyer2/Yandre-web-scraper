from settings import settings
import os
import threading


def update_collection_check(self):
    if self.sav_dir_check():
        collection = self.update_collection()
    else:
        self.sav_dir_warning()

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

def update_suggestions(self):
    self.suggestionUpdater.reset_suggestion_table()
    self.updater_thread = threading.Thread(target=self.mainPageSuggestionsUpdater.start_threads)
    self.check_thread = threading.Thread(target=self.check_if_done)
    self.check_thread
    self.updater_thread.start()
    self.start_gif()