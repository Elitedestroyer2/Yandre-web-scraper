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

    def return_added_characters(self):
        characters = self.change_to_added_character_format_many(self.conn.get_added_characters_table())
        return characters
    
    def return_characters(self):
        characters = self.change_to_character_format(self.conn.get_character_table())
        return characters


    def add_added_character(self, characterName, amount, lewd, wholesome, duplicate):
        character = (addedCharacter(characterName, amount = amount, lewd = lewd,
                            wholesome = wholesome, duplicate = duplicate))
        if not self.conn.check_added_character_exsits([character.name]):
            self.conn.enter_added_new_character([character.name, character.amount, character.lewd,
                                                character.wholesome, character.duplicate])
        else:
            self.conn.update_added_character_amount([character.amount, character.lewd,
                                                character.wholesome, character.duplicate, character.name])
    
    def grab_added_character(self):
        characterInfo = self.conn.get_added_characters_table_first_name()
        character = self.change_to_added_character_format_single(characterInfo)
        return character

    def change_to_added_character_format_single(self, characterInfo):
        character = None
        for character_sql in characterInfo:
            #Chracter(name, lewd, wholesome, duplicate, amount, url)
            character = (addedCharacter(character_sql[0], kivy_state_to_bool(character_sql[2]), 
                                    kivy_state_to_bool(character_sql[3]), 
                                    kivy_state_to_bool(character_sql[4]), int(character_sql[1]), ''))
        return character
    
    def change_to_added_character_format_many(self, characterInfo):
        characters = []
        for character_sql in characterInfo:
            #Chracter(name, lewd, wholesome, duplicate, amount, url)
            characters.append(addedCharacter(character_sql[0], kivy_state_to_bool(character_sql[2]), 
                                    kivy_state_to_bool(character_sql[3]), 
                                    kivy_state_to_bool(character_sql[4]), int(character_sql[1]), ''))
        return characters
    
    def change_to_character_format(self, characterInfo):
        characters = []
        for character in characterInfo:
            #Chracter(name, amount)
            characters.append(Character(character[0], int(character[1])))
        return characters

    def remove_added_character(self, characterName):
        self.conn.delete_added_character([characterName])
    
    def close_connection(self):
        self.conn.close_connection()
    
    def delete_added_table(self):
        self.conn.delete_added_table()
    
    def create_added_table(self):
        self.conn.create_added_table()
    
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

    def delete_suggestions_table(self):
        self.conn.delete_suggestions_table()   

    def create_suggestions_table(self):
        self.conn.create_suggestions_table() 

    def added_character_to_suggest_list(self, character):
        self.conn.added_character_to_suggest_list([character.name, character.count])
    
    def search_for_suggestions(self, search_text):
        #modify for 'like' command in sqlite
        search_text = '%' + search_text + '%'
        return self.conn.search_for_suggestions([search_text])
    
    def grab_suggestion_list(self):
        return self.conn.grab_suggestion_list()

    def check_added_characters_table_count(self):
        counts = self.conn.check_added_characters_table_count()
        for count in counts:
            amount = count[0]
        return amount

def kivy_state_to_bool(state):
    if state == 'normal':
        return False
    elif state == 'down':
        return True
    else:
        pass