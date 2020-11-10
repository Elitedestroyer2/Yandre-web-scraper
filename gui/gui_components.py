from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.app import App

from kivy.uix.modalview import ModalView

import tkinter as tk
from tkinter import filedialog

from scraper import grab_pictures, searchSuggest, set_path, return_characters

class Blank(Label):
    pass
class TabLabel(Label):
    pass
class SaveDirButton(Button):
    def on_press(self):
        SaveDirButton.get_path(self)


    @staticmethod
    def get_path(self):
        root = tk.Tk()
        root.withdraw()

        set_path((filedialog.askdirectory()))

class CharacterTextInput(TextInput):

    #Used to visually fix Kivy cursor posistion bug after .do_backspace() is used.
    def move_cursor_left(self):
        self.do_cursor_movement(action = 'cursor_left')
    def move_cursor_right(self):
        self.do_cursor_movement(action = 'cursor_right')

    def keyboard_on_key_down(self, instance, keycode, text, modifiers):
        suggestions = []
        suggestions_data = []
        if keycode[1] == 'backspace':
            if self.selection_text != '':
                self.delete_selection()
                #Fixes visual cursor posistion bug
                CharacterTextInput.move_cursor_left(self)
                CharacterTextInput.move_cursor_right(self)
            else:
                self.do_backspace()
                return
        if keycode[1] == 'left':
            CharacterTextInput.move_cursor_left(self)
            return
        if keycode[1] == 'right':
            CharacterTextInput.move_cursor_right(self)
            return
        if len(self.text) <= 3:
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown)
        if len(self.text + keycode[1]) >= 3 or len(self.text) >= 3:
            if keycode[1] == 'backspace':
                suggestions = searchSuggest(self.text)
            else:
                suggestions = searchSuggest(self.text + keycode[1])
            if len(suggestions) == 0:
                suggestions_data.append({'text': 'No suggestions'})
            else:
                # change suggestions into proper format for the suggestions_dropdown
                for suggestion in suggestions:
                    suggestions_data.append({'text': str(suggestion)})
            # update and referesh suggestions_dropdown
            App.get_running_app().root.ids.suggestions_dropdown.data = suggestions_data
            App.get_running_app().root.ids.suggestions_dropdown.refresh_from_data()
            #clear lists
            suggestions.clear()
            suggestions_data.clear()
            # Unhide suggestions_dropdown
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown, False)
        else:
            pass

            # index search may speed up the time of this action
            # maybe Pandas HDF5


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        hide_widget(self)

    def reset(self):
        self.parent.children[1].text = ""

        for child in self.children[0].children:
            if child.selected:
                child.selected = False


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True)


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            if not isinstance(App.get_running_app().root_window.children[0], ModalView):
                App.get_running_app().root.ids.search_box.text = App.get_running_app().root.ids.suggestions_dropdown.data[self.index]['text']
                hide_widget(App.get_running_app().root.ids.suggestions_dropdown)
            else:
                return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            pass
            # deselect? In other words, reset function
        else:
            pass

class CharacterModalView(ModalView):
    def get_characters(self):
        characterList = []
        characters = return_characters()
        for character in characters:
            characterList.append({'text': str(character.name)})
        self.ids.character_list.data = characterList
        self.ids.character_list.refresh_from_data()
        hide_widget(self.ids.character_list, False)

def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True