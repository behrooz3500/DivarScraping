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

# internal
from src.widgets import Message_Box as MB
from src.Constants import *


class Scrapper:
    """
    Class to define scraping method from defined url\n
    url: url to get the links from\n
    scroll_count = number of scrolls in the browser\n
    delay_time = delay time in seconds after each scroll to get the links\n
    pattern = pattern of the links to obtain\n
    """
    def __init__(self, url, scroll_count=2, delay_time=1, pattern='', browser='Firefox'):

        self.URL = url
        self.scroll_count = scroll_count
        self.delay_time = delay_time
        self.pattern = pattern
        self.browser = browser

    def scrapping(self):

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.dirname(__file__)
            return os.path.join(base_path, relative_path)

        if self.browser == 'Firefox':
            if self.win_arch() == "64":
                file_name = FIREFOX_64_DRIVER_DIR
            else:
                file_name = FIREFOX_32_DRIVER_DIR

            my_dir = resource_path(file_name)
            service = Service(executable_path=my_dir)
            driver = webdriver.Firefox(service=service)

        else:
            MB.MessageBox(IN_PROGRESS_MESSAGE).pop_up_box()

        try:
            # open base url
            driver.get(self.URL)

            # maximizing windows
            driver.maximize_window()

            # find body
            body = driver.find_element(By.TAG_NAME, "body")

            # links
            links = set()

            for i in range(self.scroll_count):
                anchors = body.find_elements(By.TAG_NAME, 'a')
                for a in anchors:
                    href = a.get_attribute('href')
                    if href.startswith(self.pattern):
                        links.add(unquote(href))
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(self.delay_time)

            driver.close()
            self.save_history()
            return links
        except:
            pass

    def load_files(self):
        try:
            with open(OUTPUT_TEXT_FILE_NAME, 'r', encoding="utf-8") as f:
                old_set = set()
                for line in f:
                    strip_lines = line.strip()
                    old_set.add(strip_lines)
            return old_set
        except:
            return set()

    def win_arch(self):
        return '64' if machine().endswith('64') else '32'

    def save_history(self):
        try:
            with open(HISTORY_TEXT_FILE_NAME, 'a', encoding="utf-8") as f:
                f.write(f"{self.URL}\n\n")
        except:
            pass
