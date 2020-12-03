from common import CommonClasses
from database import DbManager
from kivy.uix.modalview import ModalView
from settings import settings


class DefaultValuesModalView(ModalView):

    def start_up(self):
        self.get_default_values()
        self.update_page()

    def get_default_values(self):
        self.amount, self.max_amount, self.min_amount = settings.get_default_values()

    def update_page(self):
        self.ids.default_amount_text_input.hint_text = str(self.amount)
        self.ids.max_amount_for_collection_text_input.hint_text = str(
            self.max_amount)
        self.ids.min_amount_of_pics_required_to_start_download_text_input.hint_text = str(
            self.min_amount)

    def apply_changes(self):
        self.grab_and_set_all_values()
        settings.set_default_values(str(self.amount), str(
            self.max_amount), str(self.min_amount))
        self.dismiss()

    def grab_and_set_all_values(self):
        if self.ids.default_amount_text_input.text == '':
            pass
        else:
            self.amount = self.ids.default_amount_text_input.text
        if self.ids.max_amount_for_collection_text_input.text == '':
            pass
        else:
            self.max_amount = self.ids.max_amount_for_collection_text_input.text
        if self.ids.min_amount_of_pics_required_to_start_download_text_input.text == '':
            pass
        else:
            self.min_amount = self.ids.min_amount_of_pics_required_to_start_download_text_input.text
