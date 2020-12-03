from common._commonClasses import AddedCharacter
import settings
import os


def update_database(self):
    self.dbManager.create_connection()
    amount = self.get_current_file_count() - 1
    character_name = self.character.name
    character_name = character_name.replace('_', ' ')
    self.dbManager.add_character(character_name, amount)
    self.dbManager.close_connection()


def grab_added_character(self):
    self.dbManager.create_connection()
    self.character = self.dbManager.grab_added_character()
    self.dbManager.close_connection()


def delete_added_characters_from_table(self):
    self.dbManager.create_connection()
    self.dbManager.delete_added_table()
    self.dbManager.close_connection()


def table_empty(self):
    self.dbManager.create_connection()
    if self.dbManager.check_added_characters_table_count() > 0:
        self.dbManager.close_connection()
        return False
    else:
        self.dbManager.close_connection()
        return True


def delete_added_charater_from_db(self):
    self.dbManager.create_connection()
    self.dbManager.remove_added_character(self.character.name)
    self.dbManager.close_connection()


def grab_suggestion_list(self):
    self.dbManager.create_connection()
    character_sql = self.dbManager.grab_suggestion_list()
    self.dbManager.delete_added_table()
    self.dbManager.create_added_table()
    amount, max_number, min_number = self.grab_default_values()
    for character in character_sql:
        if character.amount < min_number:
            pass
        else:
            character = AddedCharacter(
                character.name, False, True, False, amount, '')
            self.dbManager.add_added_character(character.name, character.amount, character.lewd,
                                               character.wholesome, character.duplicate)
    self.dbManager.close_connection()


def update_collection(self):
    self.dbManager.create_connection()
    self.sav_dir = settings.read_settings()
    list_folders = os.listdir(self.sav_dir)
    self.dbManager.delete_table()
    self.dbManager.create_table()
    for folder in list_folders:
        folder_path = self.get_folder_path(self.sav_dir, folder)
        amount_of_pics_in_folder = len(next(os.walk(folder_path))[2])
        self.dbManager.add_character(folder, amount_of_pics_in_folder)
    self.dbManager.close_connection()

# ? minor function?
def get_folder_path(self, sav_dir, folder):
    folder_path = sav_dir + '/' + folder
    return folder_path
