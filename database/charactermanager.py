from database import databasecomm

class addedCharacter:
    def __init__(self, name, lewd, wholesome, duplicate, amount, url=''):
        DEFAULT_AMOUNT = 20
        self.name = name
        self.url = url
        if amount == '':
            self.amount = DEFAULT_AMOUNT
        else:
            self.amount = amount
        self.lewd = lewd
        self.wholesome = wholesome
        self.duplicate = duplicate

class Character:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class dbConnection:

    def connect(self):
        self.conn = databasecomm.Connection()
        self.conn.create_connection()
        self.memConn = databasecomm.tempConnection()
        self.memConn.create_connection()

    def return_added_characters(self):
        characters = self.change_to_added_character_format(self.memConn.get_characters_table())
        return characters
    
    def return_characters(self):
        characters = self.change_to_character_format(self.conn.get_character_table())
        return characters


    def add_added_character(self, characterName, amount, lewd, wholesome, duplicate):
        character = (addedCharacter(characterName, amount = amount, lewd = lewd,
                            wholesome = wholesome, duplicate = duplicate))
        if not self.memConn.check_character_exsits([character.name]):
            self.memConn.enter_new_character([character.name, character.amount, character.lewd,
                                                character.wholesome, character.duplicate])
        else:
            self.memConn.update_character_amount([character.amount, character.lewd,
                                                character.wholesome, character.duplicate, character.name])
    
    def grab_added_characters(self):
        characterInfo = self.memConn.get_characters_table()
        characters = self.change_to_added_character_format(characterInfo)
        return characters

    def change_to_added_character_format(self, characterInfo):
        characters = []
        for character in characterInfo:
            #Chracter(name, lewd, wholesome, duplicate, amount, url)
            characters.append(addedCharacter(character[0], kivy_state_to_bool(character[2]), 
                                    kivy_state_to_bool(character[3]), 
                                    kivy_state_to_bool(character[4]), int(character[1]), ''))
        return characters
    
    def change_to_character_format(self, characterInfo):
        characters = []
        for character in characterInfo:
            #Chracter(name, amount)
            characters.append(Character(character[0], int(character[1])))
        return characters

    def remove_added_character(self, characterName):
        self.memConn.delete_character([characterName])
    
    def close_connection(self):
        self.conn.close_connection()
        self.memConn.close_connection()
    
    def delete_added_table(self):
        self.memConn.delete_table()
    
    def delete_table(self):
        self.conn.delete_table()
    
    def create_table(self):
        self.conn.create_table()
    
    def add_character(self, characterName, amount):
        character = (Character(characterName, amount))
        if not self.conn.check_character_exsits([character.name]):
            self.conn.enter_new_character([character.name, character.amount])
        else:
            self.conn.update_character_amount([character.amount, character.name])
    

def kivy_state_to_bool(state):
    if state == 'normal':
        return False
    elif state == 'down':
        return True
    else:
        pass