# PyQt5
from PyQt5.QtWidgets import QWidget, QTabWidget, QDesktopWidget

# internal constants
from src.constants import SettingsParameterConstants as spc
from src.constants import TabWidgetConstants as twc
from src.constants import GlobalConstants as gc
from src.constants import MessageBoxConstants as mbc

# internal
from src.widgets.subwidgets import main_tab as mt
from src.widgets.subwidgets import result_tab as rt
from src.widgets.subwidgets import settings_tab as st
from src import memory as mem
from src import thread as th
from src import utils
from src.widgets.message_box import MessageBox as mb

# standard
import json


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        # setting main window fixed size
        self.setFixedSize(twc.WINDOW_WIDTH, twc.WINDOW_HEIGHT)

        # open window in the center of the screen
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.setWindowTitle(twc.WINDOWS_TITLE)
        self.url_set = set()
        self.thread = th.ScrapeEngine()
        self.change_mode = 1

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")

        self.main_tab = mt.MainTab()
        self.main_tab.url_add_btn.clicked.connect(lambda: self.add_btn_clicked(self.main_tab.url_text_edit.text()))
        self.main_tab.start_btn.clicked.connect(self.start_btn_clicked)
        self.main_tab.stop_btn.clicked.connect(self.stop_btn_clicked)
        self.main_tab.pause_btn.clicked.connect(self.pause_btn_clicked)
        self.main_tab.pause_btn.setDisabled(True)
        self.main_tab.stop_btn.setDisabled(True)
        self.setTabText(0, twc.TAB_1_NAME)
        self.tab1.setLayout(self.main_tab.main_layout)

        self.result_tab = rt.ResultTab()
        self.result_tab.show_btn.clicked.connect(self.show_links_btn_clicked)
        self.setTabText(1, twc.TAB_2_NAME)
        self.tab2.setLayout(self.result_tab.main_layout)
        self.result_tab.url_combo_list.addItems(self.url_set)

        self.settings_tab = st.SettingTab()
        self.setTabText(2, twc.TAB_3_NAME)
        self.settings_tab.manual_radio_btn.toggled.connect(
            lambda: self.manual_radio_button_trigger(self.settings_tab.manual_radio_btn))

        self.settings_tab.default_btn.clicked.connect(self.restore_defaults_clicked)
        self.settings_tab.save_btn.clicked.connect(self.save_settings_btn_clicked)
        self.tab3.setLayout(self.settings_tab.main_layout)
        self.thread.signals.refresh.connect(self.update_gui)

    def add_btn_clicked(self, url):
        self.url_set.add(url)
        mem.set(gc.URLS_TEXT, self.url_set)
        self.main_tab.url_list.clear()
        self.main_tab.url_text_edit.clear()
        for url in self.url_set:
            self.main_tab.url_list.appendPlainText(url)
        self.main_tab.start_btn.setDisabled(False)

    def start_btn_clicked(self):
        if self.url_set:
            with open(gc.SETTINGS_FILE_NAME, 'r') as f:
                setting = json.load(f)

            mem.set(spc.SCROLL_MODE, setting.get(spc.SCROLL_MODE))
            mem.set(spc.SCROLL_COUNT, setting.get(spc.SCROLL_COUNT))
            mem.set(spc.SCROLL_WAIT_TIME, setting.get(spc.SCROLL_WAIT_TIME))
            mem.set(spc.SCROLL_TIME_OUT, setting.get(spc.SCROLL_TIME_OUT))
            mem.set(spc.HIDE_IMAGE_SETTING, setting.get(spc.HIDE_IMAGE_SETTING))
            mem.set(spc.MAXIMIZE_PAGE_SETTING, setting.get(spc.MAXIMIZE_PAGE_SETTING))
            mem.set(gc.PATTERN_TEXT, self.main_tab.pattern_box_edit.text())

            self.result_tab.url_combo_list.addItems(mem.get(gc.URLS_TEXT))
            self.thread.start()
            self.main_tab.start_btn.setDisabled(True)
            self.main_tab.pause_btn.setDisabled(False)
            self.main_tab.stop_btn.setDisabled(False)
        else:
            mb(mbc.NO_URL_EXIST).pop_up_box()

    def pause_btn_clicked(self):
        if self.change_mode == 1:
            self.thread.pause()
            self.main_tab.pause_btn.setText(twc.RESUME_BUTTON_TEXT)
        elif self.change_mode == -1:
            self.thread.resume()
            self.main_tab.pause_btn.setText(twc.PAUSE_BUTTON_TEXT)
        self.change_mode *= -1

    def stop_btn_clicked(self):
        self.thread.stop()
        if self.thread.finalEvent.is_set():
            self.main_tab.start_btn.setDisabled(False)
            self.main_tab.pause_btn.setDisabled(True)
            self.main_tab.stop_btn.setDisabled(True)

    def show_links_btn_clicked(self):
        text = self.result_tab.url_combo_list.currentText()
        self.result_tab.result_links.clear()
        temp_list = utils.file_reader(utils.file_name_edit(text))
        for link in temp_list:
            self.result_tab.result_links.appendPlainText(link)

    def manual_radio_button_trigger(self, tr):
        if tr.isChecked():
            self.settings_tab.scroll_number.setDisabled(False)
        else:
            self.settings_tab.scroll_number.setDisabled(True)

    def restore_defaults_clicked(self):
        self.settings_tab.automatic_radio_btn.setChecked(True)
        self.settings_tab.time_out_edit.setText("4")
        self.settings_tab.scroll_wait_time_edit.setText("2")
        self.settings_tab.hide_image_checkbox.setChecked(True)
        self.settings_tab.windows_maximized_checkbox.setChecked(True)

        dic = {spc.SCROLL_MODE: spc.SCROLL_MODE_AUTO,
               spc.SCROLL_COUNT: "1",
               spc.SCROLL_WAIT_TIME: "2",
               spc.SCROLL_TIME_OUT: "4",
               spc.HIDE_IMAGE_SETTING: True,
               spc.MAXIMIZE_PAGE_SETTING: True
               }

        with open(gc.SETTINGS_FILE_NAME, "w") as f:
            json.dump(dic, f)

    def save_settings_btn_clicked(self):
        if self.settings_tab.automatic_radio_btn.isChecked():
            scroll_mode = spc.SCROLL_MODE_AUTO
        else:
            scroll_mode = spc.SCROLL_MODE_MANUAL
        dic = {spc.SCROLL_MODE: scroll_mode,
               spc.SCROLL_COUNT: self.settings_tab.scroll_number.text(),
               spc.SCROLL_WAIT_TIME: self.settings_tab.scroll_wait_time_edit.text(),
               spc.SCROLL_TIME_OUT: self.settings_tab.time_out_edit.text(),
               spc.HIDE_IMAGE_SETTING: self.settings_tab.hide_image_checkbox.isChecked(),
               spc.MAXIMIZE_PAGE_SETTING: self.settings_tab.windows_maximized_checkbox.isChecked()
               }

        with open(gc.SETTINGS_FILE_NAME, "w") as f:
            json.dump(dic, f)

    def update_gui(self, text):
        url_list = self.main_tab.url_list.toPlainText()
        url_list = url_list.replace(text, f"Scraping links finished>>{text}<<")
        self.main_tab.url_list.clear()
        self.main_tab.url_list.setPlainText(url_list)
        self.url_set.remove(text)


