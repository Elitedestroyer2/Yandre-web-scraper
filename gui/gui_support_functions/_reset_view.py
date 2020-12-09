from kivy.app import App

def reset_view(self):
    App.get_running_app().root.ids.search_box.text = ''
    App.get_running_app().root.ids.amount.text = ''
    App.get_running_app().root.ids.lewd.state = self.default_values.lewd
    App.get_running_app().root.ids.wholesome.state = self.default_values.wholesome
    App.get_running_app().root.ids.duplication.state = self.default_values.duplication