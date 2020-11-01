import kivy
import importlib
from scapper import apple
from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout


from kivy.lang import Builder

class Launch(FloatLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)

    def send(self, lewd, wholesome, duplicate, search):
        grab_pictures(lewd, wholesome, duplicate, search)


class ScrapperApp(App):

    def build(self):
        return Launch()

if __name__ == '__main__':
    ScrapperApp().run()