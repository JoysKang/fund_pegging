import json


def load_json(file_path="../conf.json"):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except:
        return {}


# 同一级目录可直接引用
conf = load_json()
