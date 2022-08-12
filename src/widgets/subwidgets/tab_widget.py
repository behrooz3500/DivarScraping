# PyQt5
from PyQt5.QtWidgets import QWidget, QTabWidget, QDesktopWidget

# internal
from src.constants import *
from src.widgets.subwidgets import main_tab as mt
from src.widgets.subwidgets import result_tab as rt
from src.widgets.subwidgets import settings_tab as st
from src import memory as mem
from src import thread as th
from src import utils

# standard
import json


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        # setting main window fixed size
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # open window in the center of the screen
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.setWindowTitle(WINDOWS_TITLE)
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
        self.main_tab.start_btn.setDisabled(True)
        self.setTabText(0, "Main")
        self.tab1.setLayout(self.main_tab.main_layout)

        self.result_tab = rt.ResultTab()
        self.result_tab.show_btn.clicked.connect(self.show_links_btn_clicked)
        self.setTabText(1, "Result Tab")
        self.tab2.setLayout(self.result_tab.main_layout)
        self.result_tab.url_combo_list.addItems(self.url_set)

        self.settings_tab = st.SettingTab()
        self.setTabText(2, "Settings")
        self.settings_tab.manual_radio_btn.toggled.connect(
            lambda: self.manual_radio_button_trigger(self.settings_tab.manual_radio_btn))

        self.settings_tab.default_btn.clicked.connect(self.restore_defaults_clicked)
        self.settings_tab.save_btn.clicked.connect(self.save_settings_btn_clicked)
        self.tab3.setLayout(self.settings_tab.main_layout)

    def add_btn_clicked(self, url):
        self.url_set.add(url)
        mem.set("urls", self.url_set)
        self.main_tab.url_list.clear()
        self.main_tab.url_text_edit.clear()
        for url in self.url_set:
            self.main_tab.url_list.appendPlainText(url)
        self.main_tab.start_btn.setDisabled(False)

    def start_btn_clicked(self):
        with open("settings.json", 'r') as f:
            setting = json.load(f)

        mem.set("scroll_mode", setting.get("Scroll mode"))
        mem.set("scroll_count", setting.get("Number of scrolls"))
        mem.set("delay_time", setting.get("Scroll wait"))
        mem.set("time_out", setting.get("Time out"))
        mem.set("hide_images", setting.get("Hide images"))
        mem.set("maximize_window", setting.get("Maximize window"))
        mem.set("pattern", self.main_tab.pattern_box_edit.text())

        self.result_tab.url_combo_list.addItems(mem.get("urls"))
        self.thread.start()
        self.main_tab.start_btn.setDisabled(True)
        self.main_tab.pause_btn.setDisabled(False)
        self.main_tab.stop_btn.setDisabled(False)

    def pause_btn_clicked(self):
        if self.change_mode == 1:
            self.thread.pause()
            self.main_tab.pause_btn.setText("Resume")
        elif self.change_mode == -1:
            self.thread.resume()
            self.main_tab.pause_btn.setText("Pause")
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

        dic = {"Scroll mode": "automatic",
               "Number of scrolls": "1",
               "Scroll wait": "2",
               "Time out": "4",
               "Hide images": True,
               "Maximize window": True
               }

        with open("settings.json", "w") as f:
            json.dump(dic, f)

    def save_settings_btn_clicked(self):
        if self.settings_tab.automatic_radio_btn.isChecked():
            scroll_mode = "automatic"
        else:
            scroll_mode = "manual"
        dic = {"Scroll mode": scroll_mode,
               "Number of scrolls": self.settings_tab.scroll_number.text(),
               "Scroll wait": self.settings_tab.scroll_wait_time_edit.text(),
               "Time out": self.settings_tab.time_out_edit.text(),
               "Hide images": self.settings_tab.hide_image_checkbox.isChecked(),
               "Maximize window": self.settings_tab.windows_maximized_checkbox.isChecked()
               }

        with open("settings.json", "w") as f:
            json.dump(dic, f)
