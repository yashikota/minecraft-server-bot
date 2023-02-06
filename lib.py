import re
from collections import Counter


def get_logged_in_user():
    file_path = "../mc/nohup.out"
    regex = r"\[\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\]"
    with open(file_path, "r") as f:
        return [re.sub(regex, "", (line.split(" ")[4])) for line in f if "logged in with entity" in line]


def get_logged_out_user():
    file_path = "../mc/nohup.out"
    with open(file_path, "r") as f:
        return [line.split(" ")[4] for line in f if "left the game" in line]


def get_active_user():
    return list(Counter(get_logged_in_user()) - Counter(get_logged_out_user()))
