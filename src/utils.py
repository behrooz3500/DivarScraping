import sys


def file_writer(filename, data):
    with open(f"{filename}.txt", "wt", encoding="utf-8") as f:
        f.write(f"{data}\n")


def file_reader(filename):
    read_set = set()
    with open(f"{filename}.txt", "rt", encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            read_set.add(stripped_line)

    return read_set


def file_appender(filename, data):
    with open(f"{filename}.txt", "at", encoding="utf-8") as f:
        f.write(f"{data}\n")


def file_name_edit(name):
    char_to_replace = {".": "_",
                       "/": "_",
                       "*": "",
                       "-": "",
                       ":": ""}
    for k, v in char_to_replace.items():
        name = name.replace(k, v)

    return name



