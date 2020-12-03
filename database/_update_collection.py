import os

from settings import settings


def update_collection(self):
    self.sav_dir = settings.read_settings()
    list_folders = os.listdir(self.sav_dir)
    self.dbManager.delete_table()
    self.dbManager.create_table()
    for folder in list_folders:
        folder_path = self.get_folder_path(self.sav_dir, folder)
        amount_of_pics_in_folder = len(next(os.walk(folder_path))[2])
        self.dbManager.add_character(folder, amount_of_pics_in_folder)
