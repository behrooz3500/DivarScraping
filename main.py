# standard
import sys
import os

# internal
from src.widgets import Main_Window as wd

# PyQt
from PyQt5.QtWidgets import QApplication


def main():

    app = QApplication(sys.argv)
    window = wd.MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
