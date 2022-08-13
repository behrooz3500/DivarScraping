# PyQt5
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# standard
from threading import Event

# internal
from src import scrapper as sc
from src import memory as mem
from src.constants import GlobalConstants as gc


class WorkerSignals(QObject):
    """Scraper Signals"""
    error = pyqtSignal(object)
    refresh = pyqtSignal(object)
    # pause = pyqtSignal()
    # resume = pyqtSignal()


class ScrapeEngine(QThread):
    """Scraper Engine"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine_scraper = sc.Scrapper()

        self.stopEvent = Event()
        self.resumeEvent = Event()
        self.finalEvent = Event()
        self.signals = WorkerSignals()
        self.time_out_status = True

    def start(self, *args, **kwargs):
        self.finalEvent.clear()
        self.resumeEvent.set()
        self.stopEvent.clear()
        super().start(*args, **kwargs)

    def stop(self):
        self.resumeEvent.clear()
        self.quit()
        self.stopEvent.set()
        self.resumeEvent.set()

    def resume(self):
        self.resumeEvent.set()

    def pause(self):
        self.resumeEvent.clear()

    def finish(self):
        self.finalEvent.set()

    def _do(self, url):

        self.engine_scraper.scrapping(url)
        self.time_out_status = self.engine_scraper.progress_check()
        print(f"has progress is {self.time_out_status}")

    def run(self):
        for url in list(mem.get(gc.URLS_TEXT)):
            self.engine_scraper.initialize(url)
            self.start()
            print(f"run for url: {url}")

            stop_event_status = True
            self.time_out_status = True

            while stop_event_status and self.time_out_status:
                try:
                    self._do(url)
                except Exception as e:
                    self.pause()
                    self.signals.error.emit(e)
                    print(e)
                print(f"resume is{self.resumeEvent.is_set()}")
                print(f"stop is {self.stopEvent.is_set()}")
                self.resumeEvent.wait()
                if self.stopEvent.wait(1):
                    stop_event_status = False
                print("---------------")
            print("END RUN")
            self.engine_scraper.close_current_driver()
            mem.get(gc.URLS_TEXT).remove(url)
            print(mem.get(gc.URLS_TEXT))
            self.signals.refresh.
        self.finish()
