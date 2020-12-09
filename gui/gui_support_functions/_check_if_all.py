
def check_if_all(self):
    self.characterDbManager.create_connection()
    character = list(self.characterDbManager.get_added_character())
    self.characterDbManager.close_connection()
    for c in character:
        character = c
    if character[0] == 'ALL':
        self.grab_suggestion_list()