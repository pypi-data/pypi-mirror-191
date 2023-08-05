import json


def load_json(path):
    with open(path, mode="r") as f:
        text = json.load(f)
    return text


def load_css(path):
    with open(path, mode="r") as f:
        text = f.read()
    return text
