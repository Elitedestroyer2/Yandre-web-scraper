
def add(self, characterName, amount, lewd, wholesome, duplicate):
    if characterName:
        self.add_added_character(
            characterName, amount, lewd, wholesome, duplicate)
        # reset the view
        self.reset_view()
    else:
        pass

def add_added_character(self, characterName, amount, lewd, wholesome, duplicate):
    character = (self.commonClasses.AddedCharacter(characterName, amount=amount, lewd=lewd,
                                                    wholesome=wholesome, duplicate=duplicate))
    self.dbManager.create_connection()
    if not self.dbManager.check_added_character_exists([character.name]):
        self.dbManager.enter_added_new_character([character.name, character.amount, character.lewd,
                                                    character.wholesome, character.duplicate])
    else:
        self.dbManager.update_added_character([character.amount, character.lewd,
                                                character.wholesome, character.duplicate, character.name])
    self.dbManager.close_connection()