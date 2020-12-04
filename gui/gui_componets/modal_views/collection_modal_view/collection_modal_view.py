from common import CommonClasses
from database import DbManager

from ..._common_functions import hide_widget
from .._base_character_modal_view import BaseCharacterModalView


class CollectionModalView(BaseCharacterModalView):

    def start_up(self):
        self.dbManager = DbManager()
        self.commonClasses = CommonClasses()
        self.get_characters()
        self.update_modal_view()

    def get_characters(self):
        self.create_connection()
        self.characterList = []
        characters = self.dbManager.get_character_table()
        if characters:
            for character in characters:
                character = self.convert_to_character_class(character)
                self.characterList.append(
                    {'text': character.name + ', ' + str(character.amount)})
        hide_widget(self.ids.collection_list, False)
        self.close_connection()

    @staticmethod
    def convert_to_character_class(character):
        #Name, Amount, Lewd, Wholesome, Duplicate
        character = CommonClasses.Character(
            character[0], character[1])
        return character

    def update_modal_view(self):
        self.ids.collection_list.data = self.characterList
        self.ids.collection_list.refresh_from_data()
