import sqlite3
from sqlite3 import Error

class Connection(object):

    def create_connection(self):
        """ create a database connection to a SQLite database """
        #characters = (Name, Url, Count, Amount)
        conn = None
        try:
            conn = sqlite3.connect(f'characters.db')

            c = conn.cursor()

            #Check if tabel exists
            c.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='characters' ''')
            
            #Create Table if it doesn't exist
            if c.fetchone()[0] == 0:
                #Bad practice to make this dynamic due to possible sql injections
                c.execute('''CREATE TABLE characters(Name, Url, Count, Amount)''')
            self.conn = conn
            self.c = c
            return conn, c

        except Error as e:
            print(e)

    def close_connection(self):
        self.conn.close()

    def check_character_exsits(self, characterName):
        #See if character's name exsits
        self.c.execute('''SELECT count(Name) FROM characters WHERE Name=? ''', characterName)
        if self.c.fetchone()[0] == 1:
            return True
        else:
            return False

    def enter_new_character(self, character):
        self.c.execute('INSERT INTO characters VALUES (?,?,?,?)', character)
        self.conn.commit()

    def update_character_amount(self, characterAmountAndName):
        self.c.execute('''UPDATE characters SET Amount=? WHERE Name=? ''', characterAmountAndName)
        self.conn.commit()

    def get_characters_names(self):
        return self.c.execute('''SELECT Name FROM characters ''')
    
    def delete_character(self, character):
        self.c.execute('''DELETE FROM characters WHERE Name='hatsune_miku' ''')
        self.conn.commit()


class tempConnection(object):
    def create_connection(self):
        """ create a database connection to a SQLite database """
        #characters = (Name, Url, Count, Amount)
        conn = None
        try:
            conn = sqlite3.connect('file::memory:?cache=shared', uri=True)

            c = conn.cursor()

            #Check if tabel exists
            c.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='addedCharacters' ''')
            
            #Create Table if it doesn't exist
            if c.fetchone()[0] == 0:
                #Bad practice to make this dynamic due to possible sql injections
                c.execute('''CREATE TABLE addedCharacters(Name, Amount)''')
            self.conn = conn
            self.c = c
            self.currentId = [1]
            return conn, c

        except Error as e:
            print(e)

    def close_connection(self):
        self.conn.close()

    def check_character_exsits(self, characterName):
        #See if character's name exsits
        self.c.execute('''SELECT count(Name) FROM addedCharacters WHERE Name=? ''', characterName)
        if self.c.fetchone()[0] == 1:
            return True
        else:
            return False

    def enter_new_character(self, character):
        self.c.execute('INSERT INTO addedCharacters VALUES (?,?)', character)
        self.conn.commit()

    def update_character_amount(self, characterAmountAndName):
        self.c.execute('''UPDATE addedCharacters SET Amount=? WHERE Name=? ''', characterAmountAndName)
        self.conn.commit()

    def get_characters_names(self):
        return self.c.execute('''SELECT Name FROM addedCharacters ''')
    
    def get_entry(self):
        characterInfo = self.c.execute('''SELECT * FROM addedCharacters WHERE rowid = ? ''', self.currentId)
        self.currentId[0] += 1
        return characterInfo
    
    def get_characters_table(self):
        return self.c.execute('''SELECT * FROM addedCharacters ''')

    def delete_character(self, character):
        self.c.execute('''DELETE FROM addedCharacters WHERE Name=? ''', character)
        self.conn.commit()
    
    def delete_table(self):
        self.c.execute('''DROP TABLE addedCharacters''')
