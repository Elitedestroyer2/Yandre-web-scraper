from kivy.app import App

from .._common_functions import hide_widget
from ._selectable_label import SelectableLabel


class CharacterSelect(SelectableLabel):
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            if not App.get_running_app().root.ids.suggestions_dropdown.data[self.index]['text'] == 'No Suggestions':
                App.get_running_app().root.ids.search_box.text = App.get_running_app(
                ).root.ids.suggestions_dropdown.data[self.index]['text']
            hide_widget(App.get_running_app().root.ids.suggestions_dropdown)
