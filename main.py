# standard
import sys

# internal
from src.widgets import main_window as wd
from src.widgets.subwidgets import tab_widget as tw

# PyQt
from PyQt5.QtWidgets import QApplication


def main():

    app = QApplication(sys.argv)
    # window = wd.MainWindow()
    window = tw.TabWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
