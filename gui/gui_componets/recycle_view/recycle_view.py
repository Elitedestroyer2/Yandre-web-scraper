from kivy.uix.recycleview import RecycleView

from .._common_functions import hide_widget


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        hide_widget(self)

    def reset(self):
        self.parent.children[1].text = ""

        for child in self.children[0].children:
            if child.selected:
                child.selected = False
