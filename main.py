from gui import gui
from settings import settings
from kivy import Config

# set default view
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '500')

# set up settings
settings.start_up()

# start the app
gui.start_app()
