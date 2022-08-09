# PyQt5
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

# internal
from src.constants import *


class ButtonWidget(QWidget):
    """
    Class for creating Buttons in the main window
    """
    def __init__(self, exec_slot, export_slot):
        super().__init__()

        self.exec_button = QPushButton()
        self.exec_button.setText(EXEC_BUTTON_TEXT)
        self.export_button = QPushButton()
        self.export_button = QPushButton(EXPORT_BUTTON_TEXT)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.exec_button)
        self.layout.addWidget(self.export_button)

        self.exec_button.clicked.connect(exec_slot)
        self.export_button.clicked.connect(export_slot)
