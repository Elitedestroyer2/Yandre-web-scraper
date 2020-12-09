from settings import settings
from gui.gui_componets.modal_views.warning_modal_view.warning_modal_view import WarningModalView

def check_first_time_duplication(self):
    if settings.get_first_duplication():
        warning_text = 'This will dramatically increase the time to download pictures!!!'
        self.warning = WarningModalView()
        self.warning.ids.warning_label.text = warning_text
        self.warning.open()
        settings.first_duplication_warning_done()

def sav_dir_warning(self):
    warning_text = 'Please choose a save directory!'
    self.warning = WarningModalView()
    self.warning.ids.warning_label.text = warning_text
    self.warning.open()