from common._commonClasses import AddedCharacter
from settings import settings
import os


def update_database(self, character_name, file_count):
    self.create_connection()
    amount = file_count - 1
    character_name = character_name
    character_name = character_name.replace('_', ' ')
    self.update_character_amount([character_name, amount])
    self.close_connection()


def grab_added_character(self):
    self.create_connection()
    self.character = self.grab_added_character()
    self.close_connection()

def grab_added_character_table(self):
    characters = []
    self.create_connection()
    characters_sql = list(self.get_added_characters_table())
    for character in characters_sql:
        characters.append(AddedCharacter(character[0], character[1], character[2], character[3], character[4]))
    self.close_connection()
    return characters


def delete_added_characters_from_table(self):
    self.create_connection()
    self.delete_added_table()
    self.close_connection()


def table_empty(self):
    self.create_connection()
    if self.check_added_characters_table_count() > 0:
        self.close_connection()
        return False
    else:
        self.close_connection()
        return True


def delete_added_charater_from_db(self):
    self.create_connection()
    self.remove_added_character(self.character.name)
    self.close_connection()


def grab_suggestion_list(self):
    self.create_connection()
    character_sql = self.grab_suggestion_list()
    self.delete_added_table()
    self.create_added_table()
    amount, max_number, min_number = self.grab_default_values()
    for character in character_sql:
        if character.amount < min_number:
            pass
        else:
            character = AddedCharacter(
                character.name, False, True, False, amount, '')
            self.add_added_character(character.name, character.amount, character.lewd,
                                               character.wholesome, character.duplicate)
    self.close_connection()


def update_collection(self):
    self.create_connection()
    self.sav_dir = settings.read_settings()
    list_folders = os.listdir(self.sav_dir)
    self.delete_table()
    self.create_table()
    for folder in list_folders:
        folder_path = get_folder_path(self.sav_dir, folder)
        amount_of_pics_in_folder = len(next(os.walk(folder_path))[2])
        self.update_character_amount([folder, amount_of_pics_in_folder])
    self.close_connection()

# ? minor function?
def get_folder_path(sav_dir, folder):
    folder_path = sav_dir + '/' + folder
    return folder_path
