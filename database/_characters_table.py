
def check_character_exists(self, characterName):
    #See if character's name exsits
    self.cursor.execute('''SELECT count(Name) FROM Characters WHERE Name=? ''', characterName)
    if self.cursor.fetchone()[0] == 1:
        return True
    else:
        return False

def enter_new_character(self, character):
    self.cursor.execute('INSERT INTO Characters VALUES (?,?)', character)
    self.conn.commit()

def update_character_amount(self, character):
    self.cursor.execute('''UPDATE Characters SET Amount=? WHERE Name=? ''', character)
    self.conn.commit()

def get_characters_names(self):
    return self.cursor.execute('''SELECT Name FROM characters ''')

def delete_character(self, character):
    self.cursor.execute('''DELETE FROM characters WHERE Name='hatsune_miku' ''')
    self.conn.commit()

def get_character_table(self):
    return self.cursor.execute('''SELECT * FROM Characters ''')

def delete_table(self):
    self.cursor.execute('''DROP TABLE Characters''')

def create_table(self):
    self.cursor.execute('''CREATE TABLE Characters(Name, Amount)''')
