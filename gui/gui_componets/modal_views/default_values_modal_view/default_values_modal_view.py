from common import CommonClasses
from database import DbManager
from kivy.uix.modalview import ModalView
from settings import settings
from kivy.app import App


class DefaultValuesModalView(ModalView):

    def start_up(self):
        self.get_default_values()
        self.update_page()

    def get_default_values(self):
        self.default_values = settings.get_default_values()

    def update_page(self):
        self.ids.default_amount_text_input.hint_text = str(self.default_values.amount)
        self.ids.max_amount_for_collection_text_input.hint_text = str(
            self.default_values.max_amount)
        self.ids.min_amount_of_pics_required_to_start_download_text_input.hint_text = str(
            self.default_values.min_amount)
        self.ids.lewd.state = self.default_values.lewd
        self.ids.wholesome.state = self.default_values.wholesome
        self.ids.duplication.state = self.default_values.duplication

    def apply_changes(self):
        self.grab_and_set_all_values()
        settings.set_default_values(str(self.default_values.amount), str(
            self.default_values.max_amount), str(self.default_values.min_amount), 
            self.default_values.lewd, self.default_values.wholesome,
            self.default_values.duplication)
        self.reset_view()
        self.dismiss()

    def grab_and_set_all_values(self):
        if self.ids.default_amount_text_input.text == '':
            pass
        else:
            self.default_values.amount = self.ids.default_amount_text_input.text
        if self.ids.max_amount_for_collection_text_input.text == '':
            pass
        else:
            self.default_values.max_amount = self.ids.max_amount_for_collection_text_input.text
        if self.ids.min_amount_of_pics_required_to_start_download_text_input.text == '':
            pass
        else:
            self.default_values.min_amount = self.ids.min_amount_of_pics_required_to_start_download_text_input.text
        self.default_values.lewd = self.ids.lewd.state
        self.default_values.wholesome = self.ids.wholesome.state
        self.default_values.duplication = self.ids.duplication.state 


    def reset_view(self):
        App.get_running_app().root.ids.search_box.text = ''
        App.get_running_app().root.ids.amount.text = ''
        App.get_running_app().root.ids.lewd.state = self.default_values.lewd
        App.get_running_app().root.ids.wholesome.state = self.default_values.wholesome
        App.get_running_app().root.ids.duplication.state = self.default_values.duplication