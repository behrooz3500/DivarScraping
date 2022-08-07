# PyQt5
from PyQt5.QtWidgets import QMessageBox

# internal
from src.Constants import *


class MessageBox:
    def __init__(self, message):
        super().__init__()
        self.title = BOX_TITLE
        self.message = message

    def pop_up_box(self):
        message = QMessageBox()
        message.setWindowTitle(self.title)
        message.setText(self.message)
        message.exec_()