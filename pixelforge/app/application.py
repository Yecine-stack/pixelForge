from ui.main_window import MainWindow


class Application:
    def __init__(self):
        self.window = MainWindow()

    def start(self):
        self.window.show()