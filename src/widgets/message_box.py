# PyQt5
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

# internal
from src.constants import MessageBoxConstants as mbc
from resources import resources_rc


class BaseMessageBox:

    def __init__(self):
        super().__init__()
        self.title = mbc.BOX_TITLE
        self.message = ""
        self.icon = QIcon(":/resources/scrape.ico")
        self.button = QMessageBox.Ok
        self.ret = True

    def pop_up_box(self):
        message = QMessageBox()
        message.setWindowIcon(self.icon)
        message.setWindowTitle(self.title)
        message.setText(self.message)
        message.setStandardButtons(self.button)
        self.ret = message.exec_()


class MessageBox(BaseMessageBox):
    def __init__(self, message):
        super().__init__()
        self.message = message


class QuestionMessage(BaseMessageBox):

    def __init__(self, message):
        super().__init__()
        self.message = message
        self.button = QMessageBox.Yes | QMessageBox.No

    def pop_up_box(self):
        super().pop_up_box()
        if self.ret == QMessageBox.Yes:
            return True
        else:
            return False


