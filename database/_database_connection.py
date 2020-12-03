import sqlite3
from sqlite3 import Error
import threading

lock = threading.Lock()

def create_connection(self):
    lock.acquire(True)
    """ create a database connection to a SQLite database """
    #characters = (Name, Url, Count, Amount)
    conn = None
    try:
        conn = sqlite3.connect('database/db/characters.db')

        cursor = conn.cursor()

        #Check if tabel exists
        cursor.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='Characters' ''')
        
        #Create Table if it doesn't exist
        if cursor.fetchone()[0] == 0:
            #Bad practice to make this dynamic due to possible sql injections
            cursor.execute('''CREATE TABLE Characters(Name, Amount)''')
        
        cursor.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='Suggestions' ''')

        #Create Table if it doesn't exist
        if cursor.fetchone()[0] == 0:
            #Bad practice to make this dynamic due to possible sql injections
            cursor.execute('''CREATE TABLE Suggestions(Name)''')
        
        cursor.execute('''SELECT count(Name) FROM sqlite_master WHERE type='table' AND Name='AddedCharacters' ''')

        #Create Table if it doesn't exist
        if cursor.fetchone()[0] == 0:
            #Bad practice to make this dynamic due to possible sql injections
            cursor.execute('''CREATE TABLE AddedCharacters(Name, Amount, Lewd, Wholesome, Duplicate)''')

        self.conn = conn
        self.cursor = cursor

    except Error as e:
        print(e)

def close_connection(self):
    self.cursor.close()
    self.conn.close()
    lock.release()

