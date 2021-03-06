# -*- coding: utf-8 -*-

import datetime
import json
import requests
import akshare as ak

from utils.trading_day import is_trading_day
from utils.conf import load_json
from utils.util import send_to_message

conf = load_json("./conf.json")

# 1 钉钉 2 飞书 3 企业微信(openapi) 4 企业微信(腾讯云函数)
send_func = {
    "1": "text(message)",
    "2": "send_lark(message)",
    "3": "send_to_wecom(message)",
    "4": "send_to_wecom_by_txy(message)",
    "5": "send_bark(message)",
    "6": "send_chanify(message)",
}


def get_all_fund_estimation():
    """通过 akshare 获取所有基金(天天基金)的估值
    返回值类型 pandas
    """
    return ak.fund_em_value_estimation()


def get_data():
    """通过 Notion API 获取指定 database 里的数据"""
    headers = {
        'Authorization': conf.get('authorization'),
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
    }

    _data = '{"filter":{"or":[{"and":[{"property":"Status","select":{"equals":"启用"}},{"property":"Type","select":{' \
            '"equals":"场内"}}]},{"and":[{"property":"Status","select":{"equals":"启用"}},{"property":"Type",' \
            '"select":{"equals":"场外"}}]}]}}'.encode()

    response = requests.post(
        f'https://api.notion.com/v1/databases/{conf.get("databases_id")}/query',
        headers=headers, data=_data)
    content = json.loads(response.content)
    return {result['properties']['Code']['rich_text'][0]['plain_text']: {
            "name": result['properties']['Name']['title'][0]['plain_text'],
            "cordon": result['properties']['Decline']['select']['name'],
            "communication": ""
        } for result in content['results']}


async def task(code=None, percent="", content=None):
    """处理盯盘任务"""
    if "-" not in percent:  # 上涨的不处理
        return None

    if content is None:
        return None

    percent = percent.replace("-", '').replace("%", '')
    cordon = content.get('cordon')
    if percent < cordon:  # 不需要发通知
        print(f"{code}，{content.get('name')}，-{percent}%，-{cordon}%，不需要发通知")
        return None

    # message IDE 会提示没有使用，但其实下边的 eval 使用了
    message = f"基金盯盘: {content.get('name')} 今日跌幅超过 {cordon}% 警戒线, 当前跌幅 {percent}% , 基金代码 {code} ."
    send_to_message(message)
    return code


async def pegging():
    """主函数"""
    # 如果不是交易日，则直接结束
    if not is_trading_day():
        print(f"日期：{datetime.date.today()}，当前不是交易日")
        return

    try:
        df = get_all_fund_estimation()
    except Exception as e:  # 重试
        print(e)
        print("获取基金估值失败，重试中...")
        df = get_all_fund_estimation()
    data = get_data()
    code_list = data.keys()

    funds = df[df['基金代码'].isin(code_list)].iloc[:, [1, 4]]
    results = []
    for _, row in funds.iterrows():
        code = row[0]
        results.append(await task(code, row[1], data[code]))  # 编码，涨跌幅，警戒线

    if results := list(filter(None, results)):
        print(f"日期：{datetime.date.today()}，报警的监控条数{len(results)}")
    else:
        print(f"日期：{datetime.date.today()}，没有需要报警的监控")


if __name__ == '__main__':
    # get_data()

    import asyncio
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(pegging())
    loop.close()
