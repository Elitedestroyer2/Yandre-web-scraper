from gui import gui
from settings import settings

# set up settings
settings.start_up()

# start the app
gui.start_app()


# TODO: Move added_character list grab to gui.py from scraper.py so multi thread pool executer can be used

# TODO fix filters from kivy to bool