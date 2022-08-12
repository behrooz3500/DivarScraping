# standard
import sys

# internal
from src.widgets.subwidgets import tab_widget as tw

# PyQt
from PyQt5.QtWidgets import QApplication


def main():

    app = QApplication(sys.argv)
    window = tw.TabWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
