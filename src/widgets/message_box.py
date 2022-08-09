# PyQt5
from PyQt5.QtWidgets import QMessageBox

# internal
from src.constants import *


class BaseMessageBox:
    def __init__(self):
        super().__init__()
        self.title = BOX_TITLE
        self.message = ""

    def pop_up_box(self):
        message = QMessageBox()
        message.setWindowTitle(self.title)
        message.setText(self.message)
        message.exec_()


class MessageBox(BaseMessageBox):
    def __init__(self, message):
        super().__init__()
        self.message = message


class QuestionMessage(BaseMessageBox):
    def __init__(self, parent):
        super().__init__()
        self.message = QMessageBox.question(parent, self.title, CLEAR_HISTORY_TEXT,
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def close_event(self):
        if self.message == QMessageBox.Yes:
            return True
        else:
            return False


