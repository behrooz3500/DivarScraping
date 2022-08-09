# PyQt5
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QComboBox

# INTERNAL
from src.constants import *


class LabelWidget(QWidget):
    """
    Class for user input field\n
    scroll_count_box = number of scrolls in the browser\n
    delay_box = delay time in seconds after each scroll\n
    pattern_box = pattern of the links to gather
    """
    def __init__(self):
        super().__init__()

        self.scroll_count_label = QLabel()
        self.scroll_count_label.setText(SCROLL_COUNT_LABEL_TEXT)
        self.scroll_count_box = QLineEdit()
        self.scroll_count_box.setFixedSize(SCROLL_INPUT_WIDTH, INPUT_HEIGHT)

        self.delay_label = QLabel()
        self.delay_label.setText(DELAY_LABEL_TEXT)
        self.delay_box = QLineEdit()
        self.delay_box.setFixedSize(DELAY_INPUT_WIDTH, INPUT_HEIGHT)

        self.pattern_label = QLabel()
        self.pattern_label.setText(PATTERN_LABEL_TEXT)
        self.pattern_box = QLineEdit()
        self.pattern_box.setText(PATTERN_BOX_DEFAULT)
        self.pattern_box.setFixedSize(PATTERN_INPUT_WIDTH, INPUT_HEIGHT)

        self.combo_label = QLabel()
        self.combo_label.setText("Browser")
        self.browser_select = QComboBox()
        self.browser_select.setObjectName("MyComboBox")
        self.browser_select.addItems(BROWSER_LIST)

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.scroll_count_label)
        self.layout.addWidget(self.scroll_count_box)

        self.layout.addWidget(self.delay_label)
        self.layout.addWidget(self.delay_box)

        self.layout.addWidget(self.pattern_label)
        self.layout.addWidget(self.pattern_box)

        self.layout.addWidget(self.combo_label)
        self.layout.addWidget(self.browser_select)
