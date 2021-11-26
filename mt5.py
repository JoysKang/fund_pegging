import re
import json
import requests
import datetime

import akshare as ak
import easyquotation

from utils.trading_day import is_trading_day
from utils.conf import load_json

conf = load_json("./conf.json")


def mt5_down(close_list, index=4, down=False):
    """九转序列判断：连续 9 天收盘价低于前 4 天的收盘价"""
    if index == 13:
        return down

    if close_list[index] < min(close_list[index-4:index]):   # 小于前四日的收盘价
        return mt5_up(close_list, index + 1, True)
    else:
        return False


def mt5_up(close_list, index=4, up=False):
    """九转序列判断：连续 9 天收盘价高于前 4 天的收盘价"""
    if index == 13:
        return up

    if close_list[index] > max(close_list[index-4:index]):   # 大于前四日的收盘价
        return mt5_up(close_list, index + 1, True)
    else:
        return False


def get_symbols():
    """通过 Notion API 获取指定 database 里的数据"""
    headers = {
        'Authorization': conf.get('authorization'),
        'Notion-Version': '2021-05-13',
        'Content-Type': 'application/json',
    }

    _data = '{ "filter": { "and": [{"property":"Status","select":{"equals":"启用"}},{"property":"Type","select":{' \
            '"equals":"股票"}}] } }'.encode()

    response = requests.post(
        f'https://api.notion.com/v1/databases/{conf.get("databases_id")}/query',
        headers=headers, data=_data)
    content = json.loads(response.content)

    return [r['properties']['Code']['rich_text'][0]['plain_text'] for r in content['results']]


def get_12days_data(symbol='sz300015'):
    """获取前12天的数据"""
    data = ak.stock_zh_a_daily(symbol).sort_values(by='date', ascending=False).iloc[:12]
    close_list = data['close'].tolist()[::-1]

    symbol = re.findall(r"\d+\.?\d*", symbol)
    return {symbol[0]: close_list}
    # close_list = [48.22, 47.59, 48.34, 48.35, 49.43, 49.5, 49.6, 49.69, 49.86, 49.95, 49.99, 50.11]
    # print(close_list)
    # print(mt5_up(close_list), "===")
    # # print("00000")
    # # print(mt5_down(close_list), "===")


def get_price(symbol_list=None):
    """获取 14:30 的价格"""
    if symbol_list is None:
        return {}

    quotation = easyquotation.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    quotation.market_snapshot(prefix=False)  # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
    prices = quotation.stocks(symbol_list)

    for price in prices:
        prices[price] = prices[price]['now']

    return prices


async def main():
    """主函数"""
    # 如果不是交易日，则直接结束
    if not is_trading_day():
        print(f"日期：{datetime.date.today()}，当前不是交易日")
        return

    symbols = get_symbols()

    data = get_12days_data('sz300015')
    prices = get_price(['sz300015'])


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())
    loop.close()
