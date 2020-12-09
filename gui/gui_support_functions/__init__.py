import kivy
from kivy.uix.floatlayout import FloatLayout
from database import DbManager
from web_scraper.scrapper_support import CharacterDbManager, SuggestionUpdater
from common import CommonClasses
from gui.gui_support_functions.initiation import grab_default_values
from web_scraper.scraper import scraper
from gui.gui_componets.modal_views.working_modal_view.working_modal_view import WorkingModalView
from settings import settings

class MainPage(FloatLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.dbManager = DbManager()
        self.characterDbManager = CharacterDbManager()
        self.commonClasses = CommonClasses()
        self.suggestionUpdater = SuggestionUpdater()
        self.default_values = grab_default_values()
        self.mainPageSuggestionsUpdater = MainPageSuggestionsUpdater()


    from ._additions import add, add_added_character
    from ._check_if_all import check_if_all
    from ._grab_suggestion_list import grab_suggestion_list
    from ._reset_view import reset_view
    from ._send import send
    from ._updates import update_collection, update_collection_check, update_suggestions
    from ._warnings import check_first_time_duplication, sav_dir_warning


    # Minor functions
    def download(self):
        scrap = scraper()
        scrap.grab_pictures()

    def start_gif(self):
        self.workingmv = WorkingModalView()
        self.workingmv.open()

    def check_if_done(self):
        while True:
            if not self.download_thread.is_alive():
                self.workingmv.dismiss()
                break

    def sav_dir_check(self):
        if settings.read_settings() != '':
            return True
        else:
            return False

class MainPageSuggestionsUpdater(object):

    from ._threads import start_threads, update_suggestions_workers

