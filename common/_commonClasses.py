from settings import settings

class AddedCharacter:
    def __init__(self, name, amount, lewd, wholesome, duplicate, url=''):
        self.name = name
        self.url = url
        if amount == '':
            self.amount = get_default_amount()
        else:
            self.amount = amount
        self.lewd = lewd
        self.wholesome = wholesome
        self.duplicate = duplicate


class Character:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class CharacterSuggestion:
    def __init__(self, name, count):
        self.name = name
        self.count = count

class PageCharacter:
    def __init__(self, name, url='', amount=20):
        self.name = name
        self.url = url
        self.amount = amount


# Support Functions

def get_default_amount():
    return settings.get_default_values().amount