from ._selectableLabel import SelectableLabel


class AddedCharacterSelect(SelectableLabel):
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            pass
        else:
            try:
                pass
            except:
                pass
