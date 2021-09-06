import requests
import json
from utils.conf import load_json

conf = load_json("./conf.json")


def send_lark(message=""):
    """通过飞书群组机器人发送消息"""
    url = conf.get("lark_webhook")

    payload = json.dumps({
        "msg_type": "text",
        "content": {
            "text": message
        }
    })

    headers = {
        'Hack-Auth': '2478',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        print("发送成功")


if __name__ == '__main__':
    conf = load_json("../conf.json")
    send_lark("test")
