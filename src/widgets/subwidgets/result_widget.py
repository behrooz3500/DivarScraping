# PyQt5
from PyQt5.QtWidgets import QWidget, QScrollArea, QPlainTextEdit

# internal
from src.Constants import *


class ResultWidget(QWidget):
    """
    Class to create a scrollable box for the results
    """
    def __init__(self):
        super().__init__()

        self.scroll_box = QScrollArea()
        self.links_box = QPlainTextEdit()
        self.links_box.setDisabled(False)
        self.links_box.setFixedSize(LINKS_BOX_WIDTH, LINKS_BOX_HEIGHT)
        self.scroll_box.setWidget(self.links_box)
