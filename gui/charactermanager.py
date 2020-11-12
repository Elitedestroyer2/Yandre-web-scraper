import databasecomm

class Character:
    def __init__(self, name, url = '', count = 0, amount = 20):
        self.name = name
        self.url = url
        self.count = count
        self.amount = amount


def return_characters(table):
    conn = databasecomm.Connection()
    conn.create_connection(table)
    return conn.get_characters_names()
    #close connection or maybe character for character then send

def add_character(characterName, amount, table):
    character = (Character(characterName, amount = amount))
    conn = databasecomm.Connection()
    conn.create_connection(table)
    if not conn.check_character_exsits([character.name]):
        conn.enter_new_character([character.name, character.url, character.count, character.amount])
    else:
        conn.update_character_amount([character.amount, character.name])

    