def ratingCheck(self, safeRating):
    # Will return states of Wholesome, and lewd, respectively
    safeRating = safeRating.replace('Rating: ', '')
    safeRating = safeRating.replace(' ', '')
    if self.character.wholesome:
        if safeRating == 'Safe':
            return True, False
        else:
            return False, True
    if self.character.lewd:
        if safeRating != 'Safe':
            return False, True
        else:
            return True, False