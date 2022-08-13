# PyQt5
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout,\
    QFormLayout, QPushButton, QLineEdit, QScrollArea,\
    QPlainTextEdit, QWidget

# internal
from src.constants import MainTabConstants as mtc


class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()

        self.line_one_layout = QHBoxLayout()
        self.url_form = QFormLayout()
        self.url_text_edit = QLineEdit()
        self.url_form.addRow(mtc.URL_LABEL_TEXT, self.url_text_edit)
        self.url_text_edit.setFixedWidth(mtc.URL_EDIT_BOX_WIDTH)
        self.url_add_btn = QPushButton()
        self.url_add_btn.setText(mtc.URL_ADD_BUTTON)
        self.line_one_layout.addLayout(self.url_form)
        self.line_one_layout.addWidget(self.url_add_btn)

        self.pattern_form = QFormLayout()
        self.pattern_box_edit = QLineEdit()
        self.pattern_form.addRow(mtc.PATTERN_LABEL_TEXT, self.pattern_box_edit)
        self.pattern_box_edit.setFixedWidth(mtc.PATTERN_EDIT_BOX_WIDTH)
        self.pattern_box_edit.setText(mtc.DEFAULT_URL_PATTERN)

        # self.url_list_box = QScrollArea()
        self.url_list = QPlainTextEdit()
        self.url_list.setReadOnly(True)
        self.url_list.setFixedWidth(mtc.URL_LIST_WIDTH)
        # self.url_list_box.setWidget(self.url_list)

        self.line_four_layout = QHBoxLayout()
        self.start_btn = QPushButton()
        self.start_btn.setText(mtc.START_BUTTON_TEXT)
        self.pause_btn = QPushButton()
        self.pause_btn.setText(mtc.PAUSE_BUTTON_TEXT)
        self.stop_btn = QPushButton()
        self.stop_btn.setText(mtc.STOP_BUTTON_TEXT)
        self.line_four_layout.addWidget(self.start_btn)
        self.line_four_layout.addWidget(self.pause_btn)
        self.line_four_layout.addWidget(self.stop_btn)

        self.main_layout.addLayout(self.line_one_layout)
        self.main_layout.addLayout(self.pattern_form)
        self.main_layout.addWidget(self.url_list)
        self.main_layout.addLayout(self.line_four_layout)
