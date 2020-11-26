import sqlite3
from sqlite3 import Error
import threading

lock = threading.Lock()

class Connection(object):

    def create_connection(self):
        lock.acquire(True)
        """ create a database connection to a SQLite database """
        #characters = (Name, Url, Count, Amount)
        conn = None
        try:
            conn = sqlite3.connect('database/db/characters.db')

            c = conn.cursor()

            #Check if tabel exists
            c.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='Characters' ''')
            
            #Create Table if it doesn't exist
            if c.fetchone()[0] == 0:
                #Bad practice to make this dynamic due to possible sql injections
                c.execute('''CREATE TABLE Characters(Name, Amount)''')
            
            c.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='Suggestions' ''')

            #Create Table if it doesn't exist
            if c.fetchone()[0] == 0:
                #Bad practice to make this dynamic due to possible sql injections
                c.execute('''CREATE TABLE Suggestions(Name)''')
            
            c.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='AddedCharacters' ''')

            #Create Table if it doesn't exist
            if c.fetchone()[0] == 0:
                #Bad practice to make this dynamic due to possible sql injections
                c.execute('''CREATE TABLE AddedCharacters(Name, Amount, Lewd, Wholesome, Duplicate)''')

            self.conn = conn
            self.c = c
            return conn, c

        except Error as e:
            print(e)

    def close_connection(self):
        self.c.close()
        self.conn.close()
        lock.release()

    def check_character_exsits(self, characterName):
        #See if character's name exsits
        self.c.execute('''SELECT count(Name) FROM Characters WHERE Name=? ''', characterName)
        if self.c.fetchone()[0] == 1:
            return True
        else:
            return False

    def enter_new_character(self, character):
        self.c.execute('INSERT INTO Characters VALUES (?,?)', character)
        self.conn.commit()

    def update_character_amount(self, character):
        self.c.execute('''UPDATE Characters SET Amount=? WHERE Name=? ''', character)
        self.conn.commit()

    def get_characters_names(self):
        return self.c.execute('''SELECT Name FROM characters ''')
    
    def delete_character(self, character):
        self.c.execute('''DELETE FROM characters WHERE Name='hatsune_miku' ''')
        self.conn.commit()

    def get_character_table(self):
        return self.c.execute('''SELECT * FROM Characters ''')

    def delete_table(self):
        self.c.execute('''DROP TABLE Characters''')
    
    def create_table(self):
        self.c.execute('''CREATE TABLE Characters(Name, Amount)''')
    
    def delete_suggestions_table(self):
        self.c.execute('''DROP TABLE Suggestions''')

    def create_suggestions_table(self):
        self.c.execute('''CREATE TABLE Suggestions(Name, count)''')

    def added_character_to_suggest_list(self, character):
        self.c.execute('''INSERT INTO Suggestions VALUES (?, ?)''', character)
        self.conn.commit()
    
    def search_for_suggestions(self, search_text):
        return self.c.execute('''SELECT Name FROM Suggestions WHERE Name LIKE ? ''', search_text)

    def grab_suggestion_list(self):
        return self.c.execute('''SELECT * FROM Suggestions ''')


    def check_added_character_exsits(self, characterName):
        #See if character's name exsits
        self.c.execute('''SELECT count(Name) FROM AddedCharacters WHERE Name=? ''', characterName)
        if self.c.fetchone()[0] == 1:
            return True
        else:
            return False

    def enter_added_new_character(self, character):
        self.c.execute('INSERT INTO AddedCharacters VALUES (?,?,?,?,?)', character)
        self.conn.commit()

    def update_added_character_amount(self, character):
        self.c.execute('''UPDATE AddedCharacters SET Amount=?, Lewd=?, Wholesome=?, Duplicate=? WHERE Name=? ''', character)
        self.conn.commit()

    def get_added_characters_names(self):
        return self.c.execute('''SELECT Name FROM AddedCharacters ''')
    
    def get_added_entry(self):
        characterInfo = self.c.execute('''SELECT * FROM AddedCharacters WHERE rowid = ? ''', self.currentId)
        self.currentId[0] += 1
        return characterInfo
    
    def get_added_characters_table(self):
        return self.c.execute('''SELECT * FROM AddedCharacters ''')

    def delete_added_character(self, character):
        self.c.execute('''DELETE FROM AddedCharacters WHERE Name=? ''', character)
        self.conn.commit()
    
    def delete_added_table(self):
        self.c.execute('''DROP TABLE AddedCharacters''')

    def create_added_table(self):
        self.c.execute('''CREATE TABLE AddedCharacters(Name, Amount, Lewd, Wholesome, Duplicate)''')

    def get_added_characters_table_first_name(self):
        return self.c.execute('''SELECT * FROM AddedCharacters ORDER BY ROWID ASC LIMIT 1 ''')
    
    def check_added_characters_table_count(self):
        return self.c.execute('''SELECT count(*) FROM AddedCharacters''')
