
from common import CommonClasses
from database import DbManager
from .._common_functions import hide_widget

from ._baseCharacterModalView import BaseCharacterModalView


class CharacterModalView(BaseCharacterModalView):
    charactesToRemove = []

    def get_characters(self):
        self.create_connection()
        self.characterList = []
        characters = self.dbManager.get_added_characters_table()
        if characters:
            for character in characters:
                character = self.convert_to_character_class(character)
                self.characterList.append(
                    {'text': self.create_string_for_added_character_list(character)})
        hide_widget(self.ids.character_list, False)
        self.close_connection()

    def update_modal_view(self):
        self.ids.character_list.data = self.characterList
        self.ids.character_list.refresh_from_data()

    @staticmethod
    def convert_to_character_class(character):
        #Name, Amount, Lewd, Wholesome, Duplicate
        character = CommonClasses.addedCharacter(
            character[0], character[1], character[2], character[3], character[4])
        return character

    def create_string_for_added_character_list(self, character):
        string = character.name + ', ' + str(character.amount)
        if character.lewd and not character.duplicate:
            string = string + ', ' + 'Lewd'
        elif character.lewd and character.duplicate:
            string = string + ', ' + 'Lewd' + ', ' + 'Duplication check'
        elif character.wholesome and not character.duplicate:
            string = string + ', ' + 'Wholesome'
        elif character.wholesome and character.duplicate:
            string = string + ', ' + 'Wholesome' + ', ' + 'Duplication check'
        elif not character.lewd and character.duplicate:
            string = string + ', ' + 'Duplication check'
        elif not character.wholesome and character.duplicate:
            string = string + ', ' + 'Duplication check'
        return string

    def remove_character(self, characterName):
        self.dbManager.remove_added_character(characterName)

    def remove_character_button(self):
        self.create_connection()
        characterNames = self.get_selected_remove_characters()
        for characterName in characterNames:
            self.remove_character(characterName)
        self.close_connection()
        self.get_characters()
        # reset selected nodes
        self.ids.character_list.children[0].selected_nodes = []
        self.update_modal_view()

    def get_selected_remove_characters(self):
        characters_to_remove = []
        # the node provides the index for the character that is selected
        for node in self.ids.character_list.children[0].selected_nodes:
            # appends the name to list of characters to remove
            character_to_remove = (
                self.ids.character_list.data[node]['text']).split(',', 1)
            characters_to_remove.append(character_to_remove[0])
        return characters_to_remove
