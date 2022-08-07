# standard
from urllib.parse import unquote
import time
import os

# selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService

# internal
from src.widgets import Message_Box as MB
from src.Constants import *


from webdriver_manager.chrome import ChromeDriverManager


class Scrapper:
    """
    Class to define scraping method from defined url\n
    url: url to get the links from\n
    scroll_count = number of scrolls in the browser\n
    delay_time = delay time in seconds after each scroll to get the links\n
    pattern = pattern of the links to obtain\n
    """
    def __init__(self, url, scroll_count='2', delay_time='1', pattern='', browser='Firefox'):

        self.URL = url
        self.scroll_count = scroll_count
        self.delay_time = delay_time
        self.pattern = pattern
        self.browser = browser

    def scrapping(self):

        dirname = os.path.dirname(__file__)
        if self.browser == 'Firefox':
            file_name = "geckodriver.exe"
            my_dir = os.path.join(dirname, file_name)
            service = Service(executable_path=my_dir)
            driver = webdriver.Firefox(service=service)

        else:
            MB.MessageBox(IN_PROGRESS_MESSAGE).pop_up_box()
            # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        try:
            # open base url
            driver.get(self.URL)

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

            return links
        except:
            pass

    def load_files(self):
        try:
            with open('links.txt', 'r', encoding="utf-8") as f:
                old_set = set()
                for line in f:

                    strip_lines = line.strip()
                    old_set.add(strip_lines)
            return old_set
        except:
            return set()
