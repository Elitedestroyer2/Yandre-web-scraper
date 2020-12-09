from common import CommonClasses

def grab_suggestion_list(self):
    self.dbManager.create_connection()
    character_sql = list(self.dbManager.grab_suggestion_list())
    self.dbManager.delete_added_table()
    self.dbManager.create_added_table()
    for character in character_sql:
        if int(character[1]) < self.default_values.min_amount:
            pass
        else:
            character = CommonClasses.AddedCharacter(
                character[0], self.default_values.amount, self.default_values.lewd,
                self.default_values.wholesome, self.default_values.duplication, '')
            self.dbManager.enter_added_new_character([character.name, character.amount, character.lewd,
                                                        character.wholesome, character.duplicate])
    self.dbManager.close_connection()