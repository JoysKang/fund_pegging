from urllib import request, parse

from utils.conf import load_json

conf = load_json("./conf.json")


def send_chanify(message=""):
    data = parse.urlencode({'title': 'fundPegging', 'text': message, 'sound': 1}).encode()
    req = request.Request(f"https://api.chanify.net/v1/sender/{conf.get('chanify_token')}", data=data)
    request.urlopen(req)


if __name__ == "__main__":
    conf = load_json("../conf.json")
    message = "明月几时有，把酒问青天。"
    send_chanify(message)
