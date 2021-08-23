import json
import requests
from urllib.parse import quote
from utils.conf import load_json

conf = load_json("./conf.json")
wecom_cid = conf.get("wecom_cid")  # 企业微信自建公司ID
wecom_aid = conf.get("wecom_aid")  # 自建应用ID
wecom_secret = conf.get("wecom_secret")  # 应用secret
url = f"{conf.get('wecom_network_url')}?sendkey={conf.get('wecom_sendkey')}&msg_type=text"


def send_to_wecom(text, wecom_touid='@all'):
    """使用 企业微信 openapi 发送消息"""
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_to_wecom_by_txy(message, to_user=''):
    """通过腾讯云部署的云函数发送消息
    to_user: User1|User2，默认为空，发送给全部
    """
    message = quote(message, 'utf-8')
    full_url = f"{url}&msg={message}&to_user={to_user}"
    response = requests.get(full_url)
    if response.status_code == 200:
        print("发送成功")


if __name__ == '__main__':
    # send_to_wecom("推送测试\r\n测试换行")
    send_to_wecom_by_txy("推送测试\r\n测试换行")
