import json


def get_config():
    return json.load(open("config.json"))
