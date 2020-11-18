from database import databasecomm

class Character:
    def __init__(self, name, url='', amount = 20):
        self.name = name
        self.url = url
        self.amount = amount

class dbConnection:

    def connect(self):
        self.conn = databasecomm.Connection()
        self.conn.create_connection()
        self.memConn = databasecomm.tempConnection()
        self.memConn.create_connection()

    def return_added_characters(self):
        return self.memConn.get_characters_names()

    def add_character(self, characterName, amount):
        character = (Character(characterName, amount = amount))
        if not self.memConn.check_character_exsits([character.name]):
            self.memConn.enter_new_character([character.name, character.amount])
        else:
            self.memConn.update_character_amount([character.amount, character.name])
    
    def grab_added_characters(self):
        characterInfo = self.memConn.get_characters_table()
        characters = []
        for character in characterInfo:
            #taking grabed info from database, and returning it as a class Character
            characters.append(Character(character[0],character[1]))
        return characters

    def remove_added_character(self, characterName):
        self.memConn.delete_character([characterName])
    
    def close_connection(self):
        self.conn.close_connection()
        self.memConn.close_connection()
    
    def delete_table(self):
        self.memConn.delete_table()
    

    