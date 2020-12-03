

def assign_filter_values(self,):
    self.lewdFilter = self.character.lewd
    self.wholesomeFilter = self.character.wholesome
    self.duplicateFilter = self.character.duplicate

def ratingCheck(self, safeRating):
    # Will return states of Wholesome, and lewd, respectively
    safeRating = safeRating.replace('Rating: ', '')
    safeRating = safeRating.replace(' ', '')
    if self.wholesomeFilter:
        if safeRating == 'Safe':
            return True, False
        else:
            return False, True
    if self.lewdFilter:
        if safeRating != 'Safe':
            return False, True
        else:
            return True, False