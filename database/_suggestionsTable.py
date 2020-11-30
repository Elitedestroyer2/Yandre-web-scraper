
def delete_suggestions_table(self):
    self.cursor.execute('''DROP TABLE Suggestions''')

def create_suggestions_table(self):
    self.cursor.execute('''CREATE TABLE Suggestions(Name, count)''')

def added_character_to_suggest_list(self, character):
    self.cursor.execute('''INSERT INTO Suggestions VALUES (?, ?)''', character)
    self.conn.commit()

def search_for_suggestions(self, search_text):
    return self.cursor.execute('''SELECT Name FROM Suggestions WHERE Name LIKE ? ''', [search_text])

def grab_suggestion_list(self):
    return self.cursor.execute('''SELECT * FROM Suggestions ''')