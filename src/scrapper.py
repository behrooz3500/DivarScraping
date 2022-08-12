# standard
from urllib.parse import unquote
import time
import os
import sys
from platform import machine


# selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from pyautogui import keyUp, keyDown, press

# internal constants
from src.constants import ScrapperConstants as sc
from src.constants import SettingsParameterConstants as spc
from src.constants import GlobalConstants as gc

# internal
from src import memory as mem
from src import utils


class Scrapper:
    """
    Class to define scraping method from defined url\n
    url: url to get the links from\n
    scroll_count = number of scrolls in the browser\n
    delay_time = delay time in seconds after each scroll to get the links\n
    pattern = pattern of the links to obtain\n
    """
    def __init__(self, browser=sc.FIREFOX_BROWSER_NAME):
        self.scroll_count = mem.get(spc.SCROLL_COUNT)
        self.delay_time = mem.get(spc.SCROLL_WAIT_TIME)
        self.pattern = mem.get(gc.PATTERN_TEXT)
        self.time_out = mem.get(spc.SCROLL_TIME_OUT)
        self.browser = browser
        self.driver = None
        self.has_progress = True
        self.links = set()
        self.count = 0
        self.scroll_count = 0
        self.store_name = []

    def initialize(self, url):

        self.scroll_count = mem.get(spc.SCROLL_COUNT)
        self.delay_time = mem.get(spc.SCROLL_WAIT_TIME)
        self.pattern = mem.get(gc.PATTERN_TEXT)
        self.time_out = mem.get(spc.SCROLL_TIME_OUT)

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.dirname(__file__)
            return os.path.join(base_path, relative_path)

        if self.browser == sc.FIREFOX_BROWSER_NAME:
            if win_arch() == "64":
                file_name = sc.FIREFOX_64_DRIVER_DIR
            else:
                file_name = sc.FIREFOX_32_DRIVER_DIR
            firefox_profile = webdriver.FirefoxProfile()
            if mem.get(spc.HIDE_IMAGE_SETTING):
                # block image load to improve page loading speed
                firefox_profile.set_preference('permissions.default.image', 2)
                firefox_profile.set_preference(' javascript.enabled', False)
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

            my_dir = resource_path(file_name)
            service = Service(executable_path=my_dir)
            self.driver = webdriver.Firefox(firefox_profile, service=service)
        else:
            pass

        # open base url
        self.driver.get(url)
        if mem.get(spc.MAXIMIZE_PAGE_SETTING):
            # maximizing windows
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
        self.count = 0
        self.has_progress = True
        self.links.clear()
        self.scroll_count = 0
        self.store_name.clear()

    def scrapping(self, url):

        # find body
        body = self.driver.find_element(By.TAG_NAME, "body")

        # links
        anchors = body.find_elements(By.TAG_NAME, 'a')
        i_len = len(self.links)

        for a in anchors:

            href = a.get_attribute('href')
            if href.startswith(mem.get(gc.PATTERN_TEXT)):
                class_name = a.find_elements(By.CLASS_NAME, sc.DIVAR_STORE_CLASS_NAME)
                for cl in class_name:
                    attr = cl.get_attribute('title')
                    if attr.find(sc.DIVAR_ATT1) == -1 and attr.find(sc.DIVAR_ATT2) == -1:
                        self.store_name.append(attr)
                    if self.store_name.count(attr) < 2:
                        self.links.add(unquote(href))

        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(int(mem.get(spc.SCROLL_WAIT_TIME)))
        f_len = len(self.links)

        a = utils.file_name_edit(url)
        export_links(self.links, a)
        print(f"{self.count}>>before checks")

        if i_len == f_len:
            self.count += 1
        else:
            self.count = 0
        print(self.time_out)
        if self.count > int(self.time_out):
            self.has_progress = False

        print(f"{self.count}>>after checks")
        self.scroll_count += 1

    def close_current_driver(self):
        self.driver.close()

    def progress_check(self):
        return self.has_progress


def export_links(generated_links, name):
    """Export results to a txt file"""

    with open(f"{name}.txt", 'wt', encoding="utf-8") as f:
        for i, link in enumerate(generated_links, 1):
            f.write(f'{link}\n\n')


def win_arch():
    return '64' if machine().endswith('64') else '32'
