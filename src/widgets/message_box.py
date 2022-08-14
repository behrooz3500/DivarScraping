# PyQt5
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

# internal
from src.constants import MessageBoxConstants as mbc


class BaseMessageBox:
    def __init__(self):
        super().__init__()
        self.title = mbc.BOX_TITLE
        self.message = ""
        self.icon = QIcon("./resources/scrape.ico")

    def pop_up_box(self):
        message = QMessageBox()
        message.setWindowIcon(self.icon)
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

    def close_event(self):
        if self.message == QMessageBox.Yes:
            return True
        else:
            return False


