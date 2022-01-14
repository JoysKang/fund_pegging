import requests
import traceback
from utils.conf import load_json

conf = load_json("./conf.json")

# dingding 相关文档：https://developers.dingtalk.com/document/app/custom-robot-access
webhook_url = conf.get('ding_webhook')


class FError(Exception):
    pass


def text(content=""):
    """
    发送 text 类型信息到钉钉
    参数示例：
    {
        "text": {
            "content":"我就是我, @XXX 是不一样的烟火"
        },
        "msgtype":"text"
    }
    """
    # 发送钉钉机器人通知
    msg_data = dict(msgtype='text', text=dict(content=content))
    print(webhook_url, "//")
    response = requests.post(webhook_url, json=msg_data)
    if response.status_code != 200:
        print(response.text)


def link(content=None):
    """
    发送 link 类型信息到钉钉
    参数示例：
    {
        "msgtype": "link",
        "link": {
            "text": "这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林",
            "title": "时代的火车向前开",
            "picUrl": "图片地址",
            "messageUrl": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"
        }
    }
    """
    # 发送钉钉机器人通知
    if not isinstance(content, dict):
        raise FError("content must be a dictionary")

    msg_data = dict(msgtype='link', link=content)
    response = requests.post(webhook_url, json=msg_data)
    if response.status_code != 200:
        print(response.text)


if __name__ == '__main__':
    conf = load_json("../conf.json")
    webhook_url = conf.get('ding_webhook')
    text("基金盯盘：我就是我, @XXX 是不一样的烟火")
