# PyQt5
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class WorkerSignals(QObject):
    """Scraper Signals"""
    progress = pyqtSignal(list)
    error = pyqtSignal(object)
    result = pyqtSignal(object)
    done = pyqtSignal()


class ScrapeEngine(QThread):
    """Scraper Engine"""
    def __init__(self):
        super().__init__()

    def start(self):
        pass

    def stop(self):
        pass

    def resume(self):
        pass

    def pause(self):
        pass

    def _do(self):
        pass

    def run(self):
        pass

    

