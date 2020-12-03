class AddedCharacter:
    def __init__(self, name, amount, lewd, wholesome, duplicate, url=''):
        DEFAULT_AMOUNT = 20
        self.name = name
        self.url = url
        if amount == '':
            self.amount = DEFAULT_AMOUNT
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