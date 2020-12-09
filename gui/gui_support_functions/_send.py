import threading


def send(self):
    # Kivy must stay on the main thread, other wise Kivy pauses
    self.check_if_all()
    self.start_gif()
    self.download_thread = threading.Thread(target=self.download)
    self.check_thread = threading.Thread(target=self.check_if_done)
    self.download_thread.start()
    self.check_thread.start()
