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

    # signal when an error occurs(error object, number of errors happened)
    error = pyqtSignal(object, int)

    # signal to refresh main gui when a url is finished
    refresh = pyqtSignal(str)

    # signal to show that scraping is finished
    completed = pyqtSignal()

    # signal for starting a new url
    begin_a_url = pyqtSignal(str)

    # signal for counting scroll count for current url
    scroll_counter = pyqtSignal(str, int)


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
            error_count = 0
            try:
                self.engine_scraper.initialize(url)
            except Exception as e:
                self.signals.error.emit(e, error_count)
                error_count += 1
            self.start()
            print(f"run for url: {url}")
            self.signals.begin_a_url.emit(url)
            stop_event_status = True
            self.time_out_status = True
            count = 1
            while stop_event_status and self.time_out_status:
                try:
                    self._do(url)
                    self.signals.scroll_counter.emit(url, count)
                    count += 1
                except Exception as e:
                    self.stop()
                    self.signals.error.emit(e, error_count)
                    error_count += 1
                    print("caught in while")
                print(f"resume is{self.resumeEvent.is_set()}")
                print(f"stop is {self.stopEvent.is_set()}")
                self.resumeEvent.wait()
                if self.stopEvent.wait(1):
                    stop_event_status = False
                print("---------------")
            self.signals.refresh.emit(url)
            print("END RUN")
            try:
                self.engine_scraper.close_current_driver()
            except Exception as e:
                self.signals.error.emit(e, error_count)
                error_count += 1
                print("caught in for")
                
            print(mem.get(gc.URLS_TEXT))

        self.signals.completed.emit()
