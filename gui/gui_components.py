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

from web_scraper import scraper
from settings import settings
from database import charactermanager

class Blank(Label):
    pass
class TabLabel(Label):
    pass
class SaveDirButton(Button):
    def on_press(self):
        self.get_path()

    def get_path(self):
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        if directory:
            settings.set_path(directory)
        else:
            pass

class CharacterTextInput(TextInput):

    def __init__(self, **kwargs):
        super(CharacterTextInput, self).__init__(**kwargs)
        self.create_connection()

    def keyboard_on_key_down(self, instance, keycode, text, modifiers):
        self.suggestions_data = []
        if keycode[1] == 'backspace':
            self.backspace()
        if keycode[1] == 'left':
            self.move_cursor_left(self)
            return
        if keycode[1] == 'right':
            self.move_cursor_right(self)
            return
        if self.check_length(keycode):
            suggestions = self.get_suggestions(keycode)
            self.update_suggestion_data(suggestions)
        elif not self.check_length(keycode):
            self.hide_drop_down()
        else:
            pass

    def create_connection(self):
        self.conn = charactermanager.dbConnection()
        self.conn.connect()

    def update_suggestion_data(self, suggestions):
        if len(suggestions) == 0:
            self.hide_drop_down()
        else:
            #change suggestions into proper format for the suggestions_dropdown
            for suggestion in suggestions:
                self.suggestions_data.append({'text': str(suggestion)})
            self.update_suggestions()
            self.suggestions_data.clear()
            self.show_drop_down()

    def update_suggestions(self):
        # update and referesh suggestions_dropdown
        App.get_running_app().root.ids.suggestions_dropdown.data = self.suggestions_data
        App.get_running_app().root.ids.suggestions_dropdown.refresh_from_data()
    
    def hide_drop_down(self):
        hide_widget(App.get_running_app().root.ids.suggestions_dropdown)
    
    def show_drop_down(self):
        hide_widget(App.get_running_app().root.ids.suggestions_dropdown, False)

    def move_cursor_left(self):
        self.do_cursor_movement(action = 'cursor_left')

    def move_cursor_right(self):
        self.do_cursor_movement(action = 'cursor_right')

    def check_length(self, keycode):
        if len(self.text) >= 3:
            return True
        elif len(self.text + keycode[1]) >= 3 and keycode[1] != 'backspace':
            return True
        else:
            False

    def backspace(self):
        if self.selection_text != '':
            self.delete_selection()
            #Fixes visual cursor posistion bug
            CharacterTextInput.move_cursor_left(self)
            CharacterTextInput.move_cursor_right(self)
        else:
            self.do_backspace()
    
    def get_suggestions(self, keycode):
        if keycode[1] == 'backspace':
            suggestions_from_sql = self.conn.search_for_suggestions(self.text)
        else:
            suggestions_from_sql = self.conn.search_for_suggestions(self.text + keycode[1])
        suggestions = self.sql_to_list(suggestions_from_sql)
        return suggestions

    def sql_to_list(self, sql_cursor):
        item_list =  []
        for item in sql_cursor:
            item_list.append(item[0])
            if len(item_list) >= 10:
                return item_list
        return item_list



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
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            pass
        else:
            pass

class CharacterSelect(SelectableLabel):
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            if not App.get_running_app().root.ids.suggestions_dropdown.data[self.index]['text'] == 'No Suggestions':
                App.get_running_app().root.ids.search_box.text = App.get_running_app().root.ids.suggestions_dropdown.data[self.index]['text']
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown)


class CharacterModalView(ModalView):
    charactesToRemove = []

    def start_up(self):
        self.create_connection()
        self.get_characters()
        self.update_modal_view()

    def get_characters(self):
        self.characterList = []
        characters = self.conn.return_added_characters()
        if characters:
            for character in characters:
                self.characterList.append({'text': self.create_string_for_added_character_list(character)})
        hide_widget(self.ids.character_list, False)
        self.close_connection()

    def create_string_for_added_character_list(self, character):
        string = character.name + ', ' + str(character.amount)
        if character.lewd and not character.duplicate:
            string = string + ', ' + 'Lewd'
        elif character.lewd and character.duplicate:
            string = string + ', ' + 'Lewd' + ', ' + 'Duplication check'
        elif character.wholesome and not character.duplicate:
            string = string + ', ' + 'Wholesome'
        elif character.wholesome and character.duplicate:
            string = string + ', ' + 'Wholesome' + ', ' + 'Duplication check'
        elif not character.lewd and character.duplicate:
            string = string + ', ' + 'Duplication check'
        elif not character.wholesome and character.duplicate:
            string = string + ', ' + 'Duplication check'
        return string

    def update_modal_view(self):
        self.ids.character_list.data = self.characterList
        self.ids.character_list.refresh_from_data()
    
    def remove_character(self, characterName):
        self.conn.remove_added_character(characterName)

    def create_connection(self):
        self.conn = charactermanager.dbConnection()
        self.conn.connect()
    
    def close_connection(self):
        self.conn.close_connection()

    def remove_character_button(self):
        self.create_connection()
        characterNames = self.get_selected_remove_characters()
        for characterName in characterNames:
            self.remove_character(characterName)
        self.get_characters()
        #reset selected nodes
        self.ids.character_list.children[0].selected_nodes = []
        self.update_modal_view()
        self.close_connection()
    
    def get_selected_remove_characters(self):
        characters_to_remove = []
        #the node provides the index for the character that is selected
        for node in self.ids.character_list.children[0].selected_nodes:
            #appends the name to list of characters to remove
            character_to_remove = (self.ids.character_list.data[node]['text']).split(',',1)
            characters_to_remove.append(character_to_remove[0])
        return characters_to_remove

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

class CollectionModalView(CharacterModalView):

    def start_up(self):
        self.create_connection()
        self.get_characters()
        self.update_modal_view()

    def get_characters(self):
        self.characterList = []
        characters = self.conn.return_characters()
        if characters:
            for character in characters:
                self.characterList.append({'text': character.name + ', ' + str(character.amount)})
        hide_widget(self.ids.character_list, False)
        self.close_connection()

class DefaultValuesModalView(CharacterModalView):
        def start_up(self):
            self.get_default_values()
            self.update_page()

        def get_default_values(self):
            self.amount, self.max_amount, self.min_amount =  settings.get_default_values()
        
        def update_page(self):
            self.ids.default_amount_text_input.hint_text = self.amount
            self.ids.max_amount_for_collection_text_input.hint_text = self.max_amount
            self.ids.min_amount_of_pics_required_to_start_download_text_input.hint_text = self.min_amount
        
        def apply_changes(self):
            self.grab_and_set_all_values()
            settings.set_default_values(self.amount, self.max_amount, self.min_amount)
            self.dismiss()
        
        def grab_and_set_all_values(self):
            if self.ids.default_amount_text_input.text == '':
                pass
            else:
                self.amount = self.ids.default_amount_text_input.text
            if self.ids.max_amount_for_collection_text_input.text == '':
                pass
            else:
                self.max_amount = self.ids.max_amount_for_collection_text_input.text
            if self.ids.min_amount_of_pics_required_to_start_download_text_input.text == '':
                pass
            else:
                self.min_amount = self.ids.min_amount_of_pics_required_to_start_download_text_input.text



class WarningModalView(ModalView):
    def start_up(self):
        pass


def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

class WorkingModalView(ModalView):
    def start_up(self):
        pass