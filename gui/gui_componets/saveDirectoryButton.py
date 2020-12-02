import tkinter as tk
from tkinter import filedialog

import settings
from kivy.uix.button import Button


class SaveDirButton(Button):
    def on_press(self):
        self.get_path()

    def get_path(self):
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        if directory:
            settings.set_path(directory)
        else:
            pass
