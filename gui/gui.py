import importlib

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.actionbar import ActionBar
from kivy.config import Config


from scraper import grab_pictures, searchSuggest


class CharacterTextInput(TextInput):

    def keyboard_on_key_down(self, instance, keycode, text, modifiers):
        suggestions = []
        suggestions_data = []
        if keycode[1] == 'backspace':
            self.text = self.text[:-1]
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown, False)
        if len(self.text) <= 3:
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown)
        if len(self.text + keycode[1]) >= 3 and keycode[1] != 'backspace' or len(self.text) >= 3:
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
            # Unhide suggestions_dropdown
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown, False)
        else:
            pass

            # index search may speed up the time of this action
            # maybe Pandas HDF5



class Blank(Label):
    pass
class TabLabel(Label):
    pass


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
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            App.get_running_app().root.ids.search_box.text = App.get_running_app().root.ids.suggestions_dropdown.data[self.index]['text']
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown)
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            pass
            # deselect? In other words, reset function
        else:
            pass


class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)

    def send(self, lewd, wholesome, duplicate, search):
        grab_pictures(lewd, wholesome, duplicate, search)


class ScraperApp(App):

    def build(self):
        return Launch()


def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

class Monitor:
    def __init__(self, width, height):
        self.width = width
        self.height = height

if __name__ == '__main__':
    ScraperApp().run()
