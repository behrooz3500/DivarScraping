# PyQt5
from PyQt5.QtWidgets import QWidget, QTabWidget, QDesktopWidget
from PyQt5.QtGui import QIcon

# internal constants
from src.constants import SettingsParameterConstants as spc
from src.constants import TabWidgetConstants as twc
from src.constants import GlobalConstants as gc
from src.constants import MessageBoxConstants as mbc
from src.constants import DefaultSettingsParameters as dfp

# internal
from src.widgets.subwidgets import main_tab as mt
from src.widgets.subwidgets import result_tab as rt
from src.widgets.subwidgets import settings_tab as st
from src import memory as mem
from src import thread as th
from src import utils
from src.widgets.message_box import MessageBox as mb
from resources import resources_rc

# standard
import json
import requests
import re

# selenium
from selenium.common import exceptions as seleniumE


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.boot_strap()

        self.url_set = set()
        self.thread = th.ScrapeEngine()
        self.change_mode = 1

        # defining tabs for the tab widget
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
        self.thread.signals.completed.connect(self.completed_scraping_slot)
        self.thread.signals.begin_a_url.connect(self.add_new_url_to_combobox)
        self.thread.signals.error.connect(self.error_manage_slot)
        self.thread.signals.scroll_counter.connect(self.update_link_count)

    def boot_strap(self):
        # setting main window fixed size
        self.setFixedSize(twc.WINDOW_WIDTH, twc.WINDOW_HEIGHT)

        # open window in the center of the screen
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.setWindowTitle(twc.WINDOWS_TITLE)
        icon = QIcon(":/resources/scrape.ico")
        self.setWindowIcon(icon)

    def add_btn_clicked(self, url):

        # checking urls (must be valid urls from divar.ir)
        regex_str = "^https://divar.ir"
        try:
            if re.search(regex_str, url):
                if requests.get(url).status_code == 200:
                    self.url_set.add(url)
                    mem.set_mem(gc.URLS_TEXT, self.url_set)
                    self.main_tab.url_list.clear()
                    self.main_tab.url_text_edit.clear()
                    for url in self.url_set:
                        self.main_tab.url_list.appendPlainText(url)
                    self.main_tab.start_btn.setDisabled(False)
                else:
                    mb(mbc.NOT_FOUND_URL).pop_up_box()
            else:
                mb(mbc.DIVAR_URL).pop_up_box()
        except Exception as e:
            print(str(e))
            mb(mbc.NO_URL_EXIST).pop_up_box()

    def start_btn_clicked(self):
        if self.url_set:
            with open(gc.SETTINGS_FILE_NAME, 'r') as f:
                setting = json.load(f)

            # storing setting parameters in memory dict
            mem.set_mem(spc.SCROLL_MODE, setting.get(spc.SCROLL_MODE))
            mem.set_mem(spc.SCROLL_COUNT, setting.get(spc.SCROLL_COUNT))
            mem.set_mem(spc.SCROLL_WAIT_TIME, setting.get(spc.SCROLL_WAIT_TIME))
            mem.set_mem(spc.SCROLL_TIME_OUT, setting.get(spc.SCROLL_TIME_OUT))
            mem.set_mem(spc.HIDE_IMAGE_SETTING, setting.get(spc.HIDE_IMAGE_SETTING))
            mem.set_mem(spc.MAXIMIZE_PAGE_SETTING, setting.get(spc.MAXIMIZE_PAGE_SETTING))
            mem.set_mem(gc.PATTERN_TEXT, self.main_tab.pattern_box_edit.text())
            mem.set_mem(spc.ERROR_TIME_OUT, self.settings_tab.error_loading_wait_time.text())

            self.result_tab.url_combo_list.clear()
            self.thread.start()
            self.main_tab.start_btn.setDisabled(True)
            self.main_tab.pause_btn.setDisabled(False)
            self.main_tab.stop_btn.setDisabled(False)
            self.main_tab.url_add_btn.setDisabled(True)
            self.main_tab.url_text_edit.setDisabled(True)
            self.main_tab.pattern_box_edit.setDisabled(True)
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
        self.settings_tab.automatic_radio_btn.setChecked(dfp.AUTOMATIC_COMBO_CHECKED)
        self.settings_tab.time_out_edit.setText(dfp.SCROLL_TIME_OUT)
        self.settings_tab.scroll_wait_time_edit.setText(dfp.SCROLL_WAIT_TIME)
        self.settings_tab.error_loading_wait_time.setText(dfp.ERROR_TIME_OUT)
        self.settings_tab.hide_image_checkbox.setChecked(dfp.HIDE_IMAGE_SETTING)
        self.settings_tab.windows_maximized_checkbox.setChecked(dfp.MAXIMIZE_PAGE_SETTING)

        dic = {spc.SCROLL_MODE: spc.SCROLL_MODE_AUTO,
               spc.SCROLL_COUNT: dfp.SCROLL_COUNT,
               spc.SCROLL_WAIT_TIME: dfp.SCROLL_WAIT_TIME,
               spc.SCROLL_TIME_OUT: dfp.SCROLL_TIME_OUT,
               spc.ERROR_TIME_OUT: dfp.ERROR_TIME_OUT,
               spc.HIDE_IMAGE_SETTING: dfp.HIDE_IMAGE_SETTING,
               spc.MAXIMIZE_PAGE_SETTING: dfp.MAXIMIZE_PAGE_SETTING
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
               spc.ERROR_TIME_OUT: self.settings_tab.error_loading_wait_time.text(),
               spc.SCROLL_TIME_OUT: self.settings_tab.time_out_edit.text(),
               spc.HIDE_IMAGE_SETTING: self.settings_tab.hide_image_checkbox.isChecked(),
               spc.MAXIMIZE_PAGE_SETTING: self.settings_tab.windows_maximized_checkbox.isChecked()
               }

        with open(gc.SETTINGS_FILE_NAME, "w") as f:
            json.dump(dic, f)

        mb(mbc.SAVE_SETTINGS).pop_up_box()

    def update_gui(self, text):
        url_list = self.main_tab.url_list.toPlainText()
        url_list = url_list.replace(text, f"Scraping links finished>>{text}<<")
        self.main_tab.url_list.clear()
        self.main_tab.url_list.setPlainText(url_list)
        self.url_set.remove(text)

    def update_link_count(self, text, count):
        url_list = self.main_tab.url_list.toPlainText()
        if count == 1:
            url_list = url_list.replace(text, f"{text}: had {count} scrolls")
        else:
            url_list = url_list.replace(f"{text}: had {count-1} scrolls", f"{text}: had {count} scrolls")
        self.main_tab.url_list.clear()
        self.main_tab.url_list.setPlainText(url_list)

    def completed_scraping_slot(self):
        mb(mbc.SCRAPING_FINISHED).pop_up_box()
        self.main_tab.start_btn.setDisabled(False)
        self.main_tab.pause_btn.setDisabled(True)
        self.main_tab.stop_btn.setDisabled(True)
        self.main_tab.url_add_btn.setDisabled(False)
        self.main_tab.url_text_edit.setDisabled(False)
        self.main_tab.pattern_box_edit.setDisabled(False)

    def add_new_url_to_combobox(self, text):

        self.result_tab.url_combo_list.addItem(text)

    def error_manage_slot(self, obj, count):
        if isinstance(obj, seleniumE.WebDriverException) and count == 0:
            mb(mbc.BROWSER_CLOSED_ERROR).pop_up_box()
            print(type(obj))
        print(type(obj))


