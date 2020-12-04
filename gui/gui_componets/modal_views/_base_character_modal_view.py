from common import CommonClasses
from database import DbManager
from kivy.uix.modalview import ModalView


class BaseCharacterModalView(ModalView):

    def start_up(self):
        self.dbManager = DbManager()
        self.commonClasses = CommonClasses()
        self.get_characters()
        self.update_modal_view()

    def create_connection(self):
        self.dbManager.create_connection()

    def close_connection(self):
        self.dbManager.close_connection()
