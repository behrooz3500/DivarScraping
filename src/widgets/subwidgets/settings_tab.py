# PyQt5
# standard
import json

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, \
    QLabel, QFormLayout, QPushButton, QLineEdit, QRadioButton, QCheckBox

# internal
from src.constants import SettingsTabConstants as stc
from src.constants import SettingsParameterConstants as spc
from src.constants import GlobalConstants as gc


class SettingTab(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.line_one_layout = QFormLayout()
        self.scroll_mode = QHBoxLayout()
        self.automatic_radio_btn = QRadioButton(stc.AUTOMATIC_RADIO_BUTTON_TEXT)
        self.manual_radio_btn = QRadioButton(stc.MANUAL_RADIO_BUTTON_TEXT)

        self.scroll_mode.addWidget(self.automatic_radio_btn)
        self.scroll_mode.addWidget(self.manual_radio_btn)

        self.line_one_layout.addRow(QLabel(stc.SCROLL_MODE_TEXT), self.scroll_mode)
        self.scroll_number = QLineEdit()
        self.line_one_layout.addRow(stc.SCROLL_NUMBER_TEXT, self.scroll_number)
        self.scroll_number.setFixedWidth(stc.TEXT_EDIT_WIDTH)
        self.time_out_edit = QLineEdit()
        self.line_one_layout.addRow(stc.TIME_OUT_TEXT, self.time_out_edit)
        self.time_out_edit.setFixedWidth(stc.TEXT_EDIT_WIDTH)
        self.scroll_wait_time_edit = QLineEdit()
        self.line_one_layout.addRow(stc.SCROLL_WAIT_TIME_TEXT, self.scroll_wait_time_edit)
        self.scroll_wait_time_edit.setFixedWidth(stc.TEXT_EDIT_WIDTH)

        self.hide_image_checkbox = QCheckBox()
        self.line_one_layout.addRow(stc.HIDE_IMAGE_TEXT, self.hide_image_checkbox)
        self.windows_maximized_checkbox = QCheckBox()
        self.line_one_layout.addRow(stc.MAXIMIZED_WINDOW_TEXT, self.windows_maximized_checkbox)

        self.btn_layout = QHBoxLayout()
        self.save_btn = QPushButton()
        self.default_btn = QPushButton()
        self.save_btn.setText(stc.SAVE_BUTTON_TEXT)
        self.default_btn.setText(stc.DEFAULT_BUTTON_TEXT)
        self.btn_layout.addWidget(self.save_btn)
        self.btn_layout.addWidget(self.default_btn)

        with open(gc.SETTINGS_FILE_NAME, "rt") as f:
            setting = json.load(f)

        if setting.get(spc.SCROLL_MODE) == spc.SCROLL_MODE_AUTO:
            self.automatic_radio_btn.setChecked(True)
            self.scroll_number.setDisabled(True)
        elif setting.get(spc.SCROLL_MODE) == spc.SCROLL_MODE_MANUAL:
            self.manual_radio_btn.setChecked(True)
            self.scroll_number.setDisabled(False)
        self.scroll_wait_time_edit.setText(setting.get(spc.SCROLL_WAIT_TIME))
        self.time_out_edit.setText(setting.get(spc.SCROLL_TIME_OUT))
        self.hide_image_checkbox.setChecked(setting.get(spc.HIDE_IMAGE_SETTING))
        self.windows_maximized_checkbox.setChecked(setting.get(spc.MAXIMIZE_PAGE_SETTING))

        self.main_layout.addLayout(self.line_one_layout)
        self.main_layout.addLayout(self.btn_layout)
