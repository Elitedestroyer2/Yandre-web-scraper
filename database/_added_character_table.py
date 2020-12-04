
def check_added_character_exists(self, characterName):
    # See if character's name exists
    self.cursor.execute(
        '''SELECT count(Name) FROM AddedCharacters WHERE Name=? ''', characterName)
    if self.cursor.fetchone()[0] == 1:
        return True
    else:
        return False


def enter_added_new_character(self, character):
    self.cursor.execute(
        'INSERT INTO AddedCharacters VALUES (?,?,?,?,?)', character)
    self.conn.commit()


def update_added_character(self, character):
    self.cursor.execute(
        '''UPDATE AddedCharacters SET Amount=?, Lewd=?, Wholesome=?, Duplicate=? WHERE Name=? ''', character)
    self.conn.commit()


def get_added_characters_names(self):
    return self.cursor.execute('''SELECT Name FROM AddedCharacters ''')


def get_added_characters_table(self):
    return self.cursor.execute('''SELECT * FROM AddedCharacters ''')


def delete_added_character(self, character):
    self.cursor.execute(
        '''DELETE FROM AddedCharacters WHERE Name=? ''', [character])
    self.conn.commit()


def delete_added_table(self):
    self.cursor.execute('''DROP TABLE AddedCharacters''')


def create_added_table(self):
    self.cursor.execute(
        '''CREATE TABLE AddedCharacters(Name, Amount, Lewd, Wholesome, Duplicate)''')


def get_added_character(self):
    return self.cursor.execute('''SELECT * FROM AddedCharacters ORDER BY ROWID ASC LIMIT 1 ''')


def check_added_characters_table_count(self):
    return self.cursor.execute('''SELECT count(*) FROM AddedCharacters''')
