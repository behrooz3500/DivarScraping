# standard
from urllib.parse import unquote

# internal
from src.Constants import *

# PyQt5
from PyQt5.QtWidgets import QLineEdit, QWidget
from PyQt5.QtCore import Qt


class UrlWidget(QWidget):
    """
    Class to create a line edit for taking url from user
    """
    def __init__(self):
        super().__init__()

        self.lb = QLineEdit()
        self.lb.setPlaceholderText(URL_HINT_TEXT)
        self.lb.setAlignment(Qt.AlignLeft)
        self.lb.setText(unquote(DEFAULT_URL))



