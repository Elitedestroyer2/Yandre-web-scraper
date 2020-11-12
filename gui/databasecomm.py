import sqlite3
from sqlite3 import Error

class Connection(object):

    def create_connection(self, tableName):
        """ create a database connection to a SQLite database """
        #characters = (Name, Url, Count, Amount)
        conn = None
        self.tableName =  tableName
        try:
            conn = sqlite3.connect(f'{tableName}.db')

            c = conn.cursor()

            #Check if tabel exists
            c.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name= ? ''', [self.tableName])
            
            #Create Table if it doesn't exist
            if c.fetchone()[0] == 0:
                #Bad practice to make this dynamic due to possible sql injections
                if self.tableName == 'characters':
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
        if self.tableName == 'characters':
            self.c.execute('''SELECT count(Name) FROM characters WHERE Name=? ''', characterName)
            if self.c.fetchone()[0] == 1:
                return True
            else:
                return False

    def enter_new_character(self, character):
        if self.tableName == 'characters':
            self.c.execute('INSERT INTO characters VALUES (?,?,?,?)', character)
        self.conn.commit()

    def update_character_amount(self, characterAmountAndName):
        if self.tableName == 'characters':
            self.c.execute('''UPDATE characters SET Amount=? WHERE Name=? ''', characterAmountAndName)
        self.conn.commit()

    def get_characters_names(self):
        if self.tableName == 'characters':
            return self.c.execute('''SELECT Name FROM characters ''')
    
    def delete_character(self, character):
        if self.tableName == 'characters':
            self.c.execute('''DELETE FROM characters WHERE Name=?''', character)
