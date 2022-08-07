# standard
from urllib.parse import unquote

# internal
from src.Constants import *

# PyQt5
from PyQt5.QtWidgets import QLineEdit, QWidget, QComboBox
from PyQt5.QtCore import Qt


class UrlWidget(QWidget):
    """
    Class to create a line edit for taking url from user
    """
    def __init__(self):
        super().__init__()

        self.edit_combo = QComboBox()
        self.edit_combo.setEditable(True)
        self.edit_combo.setPlaceholderText(URL_HINT_TEXT)
        self.edit_combo.addItems(self.load_history())

    def load_history(self):
        history_set = set()
        try:
            with open('history.txt', 'rt', encoding="utf-8") as f:
                for line in f:
                    strip_lines = line.strip()
                    history_set.add(strip_lines)
        except:
            pass

        return history_set
