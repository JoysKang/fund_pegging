from utils.ding import text
from utils.lark import send_lark
from utils.wecom import send_to_wecom_by_txy, send_to_wecom
from utils.bark import send_bark
from utils.chanify import send_chanify

from utils.conf import load_json

conf = load_json("./conf.json")


def send_to_message(message):
    """发送消息"""
    send_func = {
        "1": "text(message)",
        "2": "send_lark(message)",
        "3": "send_to_wecom(message)",
        "4": "send_to_wecom_by_txy(message)",
        "5": "send_bark(message)",
        "6": "send_chanify(message)",
    }
    eval(send_func.get((conf.get("send_type"))))  # 发送
