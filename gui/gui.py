import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from settings import settings
#from database import charactermanager

import multiprocessing
import threading
import concurrent.futures

from database import DbManager
from common import CommonClasses
from web_scraper import scraper

from web_scraper.scrapper_support import CharacterDbManager, SuggestionUpdater
import os
from gui.gui_componets.modal_views.working_modal_view.working_modal_view import WorkingModalView
from gui.gui_componets.modal_views.warning_modal_view.warning_modal_view import WarningModalView
from gui.gui_support_functions.initiation import grab_default_values
from gui.gui_support_functions import MainPage

class ScraperApp(App):

    def build(self):
        return MainPage()


def start_app():
    ScraperApp().run()


if __name__ == '__main__':
    ScraperApp().run()
