# internal
from src import scrapper
from src.constants import *
from src.widgets.subwidgets import url_widget as UW,\
                                    label_widget as LW, \
                                    result_widget as RW, \
                                    button_widget as BW
from src.widgets import message_box as MB

# PyQt5
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QDesktopWidget

# standard
from urllib.parse import unquote


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # setting main window fixed size
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # open window in the center of the screen
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.setWindowTitle(WINDOWS_TITLE)

        # boolean to insure results are generated before exporting anything
        self.is_generated = False

        # set for storing gathered links
        self.links = set()

        # declaring sub widgets
        self.url_widget = UW.UrlWidget()
        self.label_widget = LW.LabelWidget()
        self.result_widget = RW.ResultWidget()
        self.button_widget = BW.ButtonWidget(self.execute_button_clicked)
        self.url_widget.edit_combo.addItems(self.load_history())

        # adding subwidgets to the main window
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.url_widget.layout)
        self.main_layout.addLayout(self.label_widget.layout)
        self.main_layout.addWidget(self.result_widget.scroll_box)
        self.main_layout.addLayout(self.button_widget.layout)
        self.url_widget.clear_history_button.clicked.connect(self.clear_history_button_clicked)

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    def execute_button_clicked(self):
        """Execute button slot: Gather links from Url"""

        u = self.url_widget.edit_combo.currentText()
        s = self.label_widget.scroll_count_box.text()
        d = self.label_widget.delay_box.text()
        p = self.label_widget.pattern_box.text()

        # checking that user filled all inputs
        if u == "" or s == "" or d == "" or p == "":
            MB.MessageBox(FILL_THE_BLANKS_ERROR).pop_up_box()
            self.is_generated = False
        else:
            self.result_widget.links_box.clear()
            try:
                scrapper_method = scrapper
                old_set = scrapper_method.load_files()
                self.links.clear()
                self.links = old_set
                new_set = scrapper_method.Scrapper(u, int(s), int(d), p).scrapping()

                for i in new_set:
                    self.links.add(i)

                for i, link in enumerate(self.links, 1):
                    self.result_widget.links_box.appendPlainText(f'{link}\n')
                self.is_generated = True
                self.url_widget.edit_combo.addItems(self.load_history())

            except:
                MB.MessageBox(WRONG_INPUT).pop_up_box()

    def clear_history_button_clicked(self):
        if MB.QuestionMessage(self).close_event():
            with open(OUTPUT_TEXT_FILE_NAME, 'wt', encoding="utf-8") as f:
                f.write(' ')
            with open(HISTORY_TEXT_FILE_NAME, 'wt', encoding="utf-8") as f:
                f.write(' ')
            self.url_widget.edit_combo.clear()

    def load_history(self):
        history_set = set()
        try:
            with open('history.txt', 'rt', encoding="utf-8") as f:
                for line in f:
                    strip_lines = line.strip()
                    history_set.add(unquote(strip_lines))
        except:
            pass
        self.url_widget.edit_combo.clear()
        return history_set

