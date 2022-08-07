# internal
from src import Scrapper
from src.Constants import *
from src.widgets.subwidgets import Url_Widget as UW,\
                                    Label_Widget as LW, \
                                    Result_Widget as RW, \
                                    Button_Widget as BW

# PyQt5
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QDesktopWidget


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
        self.button_widget = BW.ButtonWidget(self.execute_button_clicked, self.export_button_clicked)

        # adding subwidgets to the main window
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.url_widget.lb)
        self.main_layout.addLayout(self.label_widget.layout)
        self.main_layout.addWidget(self.result_widget.scroll_box)
        self.main_layout.addLayout(self.button_widget.layout)

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    def execute_button_clicked(self):
        """Execute button slot: Gather links from Url"""

        u = self.url_widget.lb.text()
        s = self.label_widget.scroll_count_box.text(),
        d = self.label_widget.delay_box.text()
        p = self.label_widget.pattern_box.text()

        old_set = set()

        # checking that user filled all inputs
        if u == "" or s == "" or d == "" or p == "":
            self.result_widget.links_box.setPlainText(FILL_THE_BLANKS_ERROR)
            self.is_generated = False
        else:
            self.result_widget.links_box.clear()
            scrapper = Scrapper.Scrapper(self.url_widget.lb.text(),
                                         self.label_widget.scroll_count_box.text(),
                                         self.label_widget.delay_box.text(),
                                         self.label_widget.pattern_box.text(),
                                         self.label_widget.browser_select.currentText()
                                         )

            old_set = scrapper.load_files()
            self.links.clear()
            self.links = old_set
            new_set = scrapper.scrapping()

            for i in new_set:
                self.links.add(i)

            for i, link in enumerate(self.links, 1):
                self.result_widget.links_box.appendPlainText(f'{link}\n')
            self.is_generated = True

    def export_button_clicked(self):
        """Export button slot: Export results to a txt file"""

        if self.is_generated:
            with open(OUTPUT_TEXT_FILE_NAME, 'wt', encoding="utf-8") as f:
                for i, link in enumerate(self.links, 1):
                    f.write(f'{link}\n\n')
        else:
            self.result_widget.links_box.setPlainText(EXECUTE_FIRST_ERROR)
