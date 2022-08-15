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
        self.do_initialize = True
        self.added_url = []
        self.stop_event_status = True
        self.count = 0
        self.current_url = ""

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

    def _enhanced_do(self):
        self.do_initialize = False
        self.engine_scraper.scrapping(self.current_url)
        self.time_out_status = self.engine_scraper.progress_check()
        print(f"has progress is {self.time_out_status}")

    def set_urls(self):
        self.added_url = list(mem.get(gc.URLS_TEXT))

    def start_current_url(self):
        if self.do_initialize:
            print(f"new method:{self.added_url[0]}")
            self.engine_scraper.initialize(self.added_url[0])
            self.start()
            self.signals.begin_a_url.emit(self.added_url[0])
            self.stop_event_status = True
            self.time_out_status = True
            self.count = 1
            self.current_url = self.added_url[0]
            self.added_url.pop(0)

    def run(self):
        self.set_urls()
        while self.added_url:
            if self.stop_event_status and self.time_out_status:
                try:
                    self.start_current_url()
                    self._enhanced_do()
                    self.signals.scroll_counter.emit(self.current_url, self.count)
                    self.count += 1
                except Exception as e:
                    self.stop()
                    self.signals.error.emit(e, 1)
                self.resumeEvent.wait()
                if self.stopEvent.wait(1):
                    self.stop_event_status = False
            else:
                self.do_initialize = True
        self.signals.completed.emit()

    # def run(self):
    #
    #     for url in list(mem.get(gc.URLS_TEXT)):
    #         error_count = 0
    #         try:
    #
    #             # initialize scrapper setting and driver for new url
    #             self.engine_scraper.initialize(url)
    #
    #         except Exception as e:
    #
    #             # error signal (count = number of errors detected)
    #             self.signals.error.emit(e, error_count)
    #             error_count += 1
    #
    #         self.start()
    #
    #         # signal to inform gui a new url is initializing
    #         self.signals.begin_a_url.emit(url)
    #         stop_event_status = True
    #         self.time_out_status = True
    #
    #         # number of scrolls
    #         count = 1
    #         while stop_event_status and self.time_out_status:
    #             try:
    #                 self._do(url)
    #
    #                 # signal for current scroll number (updated with each _do execution)
    #                 self.signals.scroll_counter.emit(url, count)
    #                 count += 1
    #             except Exception as e:
    #                 self.stop()
    #                 self.signals.error.emit(e, error_count)
    #                 error_count += 1
    #             self.resumeEvent.wait()
    #             if self.stopEvent.wait(1):
    #                 stop_event_status = False
    #
    #         # signal to inform a url scrapping has finished
    #         self.signals.refresh.emit(url)
    #         try:
    #             self.engine_scraper.close_current_driver()
    #         except Exception as e:
    #             self.signals.error.emit(e, error_count)
    #             error_count += 1
    #
    #     # signal to inform scrapping is completely finished for all urls
    #     self.signals.completed.emit()

    def new_url_slot(self):
        pass

