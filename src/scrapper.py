# standard
from urllib.parse import unquote
import time
import os
import sys
from platform import machine
from subprocess import CREATE_NO_WINDOW

# selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
# from pyautogui import keyUp, keyDown, press

# internal constants
from src.constants import ScrapperConstants as sc
from src.constants import SettingsParameterConstants as spc
from src.constants import GlobalConstants as gc

# internal
from src import memory as mem
from src import utils
from src.utils import LinkList


class Scrapper:
    """
    Class to define scraping method from defined url\n
    """

    def __init__(self, browser=sc.FIREFOX_BROWSER_NAME):
        # number of scrolls in manual mode
        self.scroll_count = mem.get(spc.SCROLL_COUNT)

        # number of scroll execution to wait for new data
        self.delay_time = mem.get(spc.SCROLL_WAIT_TIME)

        # link patterns
        self.pattern = mem.get(gc.PATTERN_TEXT)

        # waiting time in seconds before clicking try again button of the webpage
        self.time_out = mem.get(spc.SCROLL_TIME_OUT)

        self.browser = browser
        self.driver = None

        # if there is progress in scrolling
        self.has_progress = True

        # set for storing scrapped links
        self.links = LinkList()

        # number of scrolls in current page
        self.scroll_count = 0

        # a list to detect store advertisements
        self.store_name = []
        self.saved_stores = LinkList()
        self.continue_from_history = False
        self.count = 0
        self.added_link = 0

        # if a timeout has happened
        self.no_time_out = True

    def initialize(self, url):
        """
        initialize webdriver for a new url
        """

        # initializing parameters for new url
        self.scroll_count = mem.get(spc.SCROLL_COUNT)
        self.delay_time = mem.get(spc.SCROLL_WAIT_TIME)
        self.pattern = mem.get(gc.PATTERN_TEXT)
        self.time_out = mem.get(spc.SCROLL_TIME_OUT)
        self.no_time_out = True
        self.count = 0
        self.has_progress = True
        self.links.clear_all()
        self.saved_stores.clear_all()
        print(mem.keys())
        if url in mem.keys():
            self.links = utils.file_reader(url)
            self.saved_stores = utils.file_reader(f"stores{url}")
            self.continue_from_history = True
        else:
            self.continue_from_history = False
        self.scroll_count = 0
        self.store_name.clear()

        self.added_link = 0

        def resource_path(relative_path):
            """locating webDriver for the browsser in debug mode and exe mode"""
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.dirname(__file__)
            return os.path.join(base_path, relative_path)

        # selecting correct driver based on system architecture
        if self.browser == sc.FIREFOX_BROWSER_NAME:
            if win_arch() == "64":
                file_name = sc.FIREFOX_64_DRIVER_DIR
            else:
                file_name = sc.FIREFOX_32_DRIVER_DIR
            firefox_profile = webdriver.FirefoxProfile()

            # block image load to improve page loading speed based on setting parameter
            if mem.get(spc.HIDE_IMAGE_SETTING):
                firefox_profile.set_preference('permissions.default.image', 2)
                firefox_profile.set_preference(' javascript.enabled', False)
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
                firefox_profile.set_preference('toolkit.legacyUserProfileCustomizations.stylesheets', 'true')

            my_dir = resource_path(file_name)

            service = Service(executable_path=my_dir)
            service.creationflags = CREATE_NO_WINDOW
            self.driver = webdriver.Firefox(firefox_profile, service=service)

        # for future development and adding new browsers
        else:
            pass

        # open a new url
        self.driver.get(url)

        # maximizing opened browser windows based on setting parameters
        if mem.get(spc.MAXIMIZE_PAGE_SETTING):
            self.driver.maximize_window()

            # zooming out the page (not stable)
            # if True:
            #     for i in range (5):
            #         keyDown('ctrl')
            #         press('-')
            #         keyUp('ctrl')
            #     keyDown('ctrl')
            #     press('r')
            #     keyUp('ctrl')
            #     time.sleep(3)

    def scrapping(self, url):
        """
        scrapping link from selected url using selenium
        """
        print(f"store:{self.saved_stores.len()}")
        print(f"links:{self.links.len()}")
        self.no_time_out = True

        # size of the link set before executing a page_down scroll
        # i_len = len(self.links)
        i_len = self.driver.execute_script("return document.body.scrollHeight")

        # find body
        body = self.driver.find_element(By.TAG_NAME, "body")

        # finding page section with advertisements
        anchors = body.find_elements(By.TAG_NAME, 'a')

        # finding time_out button of the web page
        errors = body.find_elements(By.CLASS_NAME, 'kt-button--small')

        # when time_out button appears, scrapper will wait for a defined
        # time specified in settings and then executes button click

        for e in errors:
            for i in range(int(mem.get(spc.ERROR_TIME_OUT))):
                time.sleep(1)
                print(i + 1)
            try:
                e.click()
            except:
                print("DO NOT TOUCH ME!")

            # waiting for some time to let windows elements load
            time.sleep(sc.WAIT_TIME_AFTER_TIMEOUT_CLICK)

            # time_out detected
            self.no_time_out = False

        if self.no_time_out:
            try:
                for a in anchors:
                    href = a.get_attribute('href')
                    if href.startswith(mem.get(gc.PATTERN_TEXT)):

                        # finding store advertisements by their class name
                        class_name = a.find_elements(By.CLASS_NAME, sc.DIVAR_STORE_CLASS_NAME)
                        for cl in class_name:
                            attr = cl.get_attribute('title')
                            if (attr.find(sc.DIVAR_ATT1) == -1
                                    and attr.find(sc.DIVAR_ATT2) == -1
                                    and attr.find(sc.DIVAR_ATT3) == -1):
                                self.store_name.append(attr)
                            if self.continue_from_history:
                                if (attr not in self.saved_stores.get_all()
                                        and self.store_name.count(attr) < 2):
                                    self.links.add(unquote(href))
                                    self.added_link += 1
                            else:
                                if self.store_name.count(attr) < 2:
                                    self.links.add(unquote(href))
                                    self.added_link += 1
            except:
                print("JUST PASSED EVERYTHING")

        # execute a page_down scroll
        body.send_keys(Keys.PAGE_DOWN)

        # wait for new data to load
        time.sleep(int(mem.get(spc.SCROLL_WAIT_TIME)))

        # final size of gathered links
        # f_len = len(self.links)
        f_len = self.driver.execute_script("return document.body.scrollHeight")
        print(self.links.len())
        for stores in self.store_name:
            self.saved_stores.add(stores)
        export_links(self.saved_stores.get_all(), f"stores{url}")
        export_links(self.links.get_all(), url)
        print(f"{self.count}>>before checks")
        print(f"scroll height diff:{f_len - i_len}")
        # comparing size of gathered link before and after the scroll
        if i_len == f_len:
            self.count += 1
        else:
            self.count = 0
        print(self.time_out)
        if self.count > int(self.time_out):
            self.has_progress = False

        print(f"{self.count}>>after checks")
        self.scroll_count += 1
        print(f"{self.added_link} new links added")

    def close_current_driver(self):
        self.driver.close()

    def progress_check(self):
        return self.has_progress


def export_links(generated_links, url):
    """Export results to a txt file"""
    name = utils.file_name_edit(url)
    action = 'wt'
    # if url in mem.keys():
    #     print("existing")
    #     action = 'at'
    # else:
    #     print("new text file")

    with open(f"{name}.txt", action, encoding="utf-8") as f:
        for i, link in enumerate(generated_links, 1):
            f.write(f'{link}\n\n')


def win_arch():
    return '64' if machine().endswith('64') else '32'
