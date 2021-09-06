import requests
from utils.conf import load_json

conf = load_json("./conf.json")


def send_bark(message):
    """使用 bark 发送消息"""
    url = f"https://api.day.app/{conf.get('bark_token')}/{message}?group=fundPegging"
    print(url)
    requests.get(url)


if __name__ == '__main__':
    conf = load_json("../conf.json")
    send_bark("没有有用的信息")
