# PyQt5
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget,\
    QLabel, QTabWidget, QFormLayout,\
    QPushButton, QLineEdit, QScrollArea,\
    QPlainTextEdit, QRadioButton, QCheckBox, QDesktopWidget, QComboBox

# internal
from src.constants import ResultTabConstants as rtc


class ResultTab(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.line_one_layout = QHBoxLayout()
        self.url_combo_list = QComboBox()
        self.url_combo_list.setFixedWidth(rtc.COMBO_BOX_WIDTH)
        self.show_btn = QPushButton()
        self.show_btn.setText(rtc.SHOW_BUTTON_TEXT)

        self.result_links = QPlainTextEdit()

        self.line_one_layout.addWidget(self.url_combo_list)
        self.line_one_layout.addWidget(self.show_btn)

        self.main_layout.addLayout(self.line_one_layout)
        self.main_layout.addWidget(self.result_links)
