# standard
import os

# internal
from src.constants import GlobalConstants as gc


class LinkList:

    def __init__(self):
        self.my_list = []

    def add(self, link):
        if link not in self.my_list:
            self.my_list.append(link)

    def remove(self, link):
        if link in self.my_list:
            self.my_list.remove(link)

    def replace(self, link1, link2):
        if link1 in self.my_list:
            self.my_list.remove(link1)
            self.my_list.__add__(link2)

    def len(self):
        return len(self.my_list)

    def get_all(self):
        return self.my_list

    def clear_all(self):
        self.my_list.clear()
        return self.my_list


def file_writer(filename, data):
    with open(f"{filename}.txt", "wt", encoding="utf-8") as f:
        f.write(f"{data}\n")


def file_reader(url):
    filename = file_name_edit(url)
    read_list = LinkList()
    with open(f"{filename}.txt", "rt", encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            read_list.add(stripped_line)

    return read_list


def file_appender(filename, data):
    with open(f"{filename}.txt", "at", encoding="utf-8") as f:
        f.write(f"{data}\n")


def file_name_edit(name):
    """change urls to be appliable for a text file"""
    char_to_replace = {".": "_",
                       "/": "_",
                       "*": "",
                       "-": "",
                       ":": "",
                       "=": "",
                       "?": "",
                       "+": "",
                       "^": "",
                       '"': "",
                       "<": "",
                       ">": ""}
    for k, v in char_to_replace.items():
        name = name.replace(k, v)

    return name


def check_url_existence(url):
    file_name = f"{file_name_edit(url)}.txt"
    if file_name in os.listdir(gc.ROOT_DIR):
        return True
    else:
        return False

