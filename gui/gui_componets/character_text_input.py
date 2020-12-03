from database import DbManager
from kivy.app import App
from kivy.uix.textinput import TextInput

from ._common_functions import hide_widget


class CharacterTextInput(TextInput):

    def __init__(self, **kwargs):
        super(CharacterTextInput, self).__init__(**kwargs)

    def keyboard_on_key_down(self, instance, keycode, text, modifiers):
        self.create_database_manager()
        self.create_connection()
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
        self.close_connection()

    def create_database_manager(self):
        self.dbManager = DbManager()

    def create_connection(self):
        self.dbManager.create_connection()

    def close_connection(self):
        self.dbManager.close_connection()

    def update_suggestion_data(self, suggestions):
        if len(suggestions) == 0:
            self.hide_drop_down()
        else:
            # change suggestions into proper format for the suggestions_dropdown
            for suggestion in suggestions:
                self.suggestions_data.append({'text': str(suggestion)})
            self.update_suggestions()
            self.suggestions_data.clear()
            self.show_drop_down()

    def update_suggestions(self):
        # update and refresh suggestions_dropdown
        App.get_running_app().root.ids.suggestions_dropdown.data = self.suggestions_data
        App.get_running_app().root.ids.suggestions_dropdown.refresh_from_data()

    def hide_drop_down(self):
        hide_widget(App.get_running_app().root.ids.suggestions_dropdown)

    def show_drop_down(self):
        hide_widget(App.get_running_app().root.ids.suggestions_dropdown, False)

    def move_cursor_left(self):
        self.do_cursor_movement(action='cursor_left')

    def move_cursor_right(self):
        self.do_cursor_movement(action='cursor_right')

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
            # Fixes visual cursor position bug
            CharacterTextInput.move_cursor_left(self)
            CharacterTextInput.move_cursor_right(self)
        else:
            self.do_backspace()

    def get_suggestions(self, keycode):
        if keycode[1] == 'backspace':
            suggestions_from_sql = self.dbManager.search_for_suggestions(
                self.convert_search_text_to_sql(self.text))
        else:
            suggestions_from_sql = self.dbManager.search_for_suggestions(
                self.convert_search_text_to_sql(self.text + keycode[1]))
        suggestions = self.sql_to_list(suggestions_from_sql)
        return suggestions

    def sql_to_list(self, sql_cursor):
        item_list = []
        for item in sql_cursor:
            item_list.append(item[0])
            if len(item_list) >= 10:
                return item_list
        return item_list

    def convert_search_text_to_sql(self, search_text):
        # modify for 'like' command in sqlite
        search_text = '%' + search_text + '%'
        return search_text
