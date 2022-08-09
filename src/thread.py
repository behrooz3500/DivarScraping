# PyQt5
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# standard
from threading import Event


class WorkerSignals(QObject):
    """Scraper Signals"""
    start = pyqtSignal()
    stop = pyqtSignal()
    pause = pyqtSignal()
    resume = pyqtSignal()


class ScrapeEngine(QThread):
    """Scraper Engine"""
    def __init__(self):
        super().__init__()
        self.stopEvent = Event()
        self.resumeEvent = Event()
        self.signals = WorkerSignals()

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



