# standard
from urllib.parse import unquote

# internal
from src.constants import *

# PyQt5
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QHBoxLayout


class UrlWidget(QWidget):
    """
    Class to create a line edit for taking url from user
    """
    def __init__(self):
        super().__init__()

        self.edit_combo = QComboBox()
        self.edit_combo.setEditable(True)
        self.edit_combo.setPlaceholderText(URL_HINT_TEXT)
        self.edit_combo.setFixedWidth(URL_BOX_WIDTH)

        self.clear_history_button = QPushButton()
        self.clear_history_button.setText(CLEAR_HISTORY_BUTTON_TEXT)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.edit_combo)
        self.layout.addWidget(self.clear_history_button)


