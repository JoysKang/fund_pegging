"""
趋势模型的逻辑（来自微信公众号:量化投基）：
沪深300、中证500、创业板，

逻辑：
    每个交易日的 14:30 与自己前 22 个交易日的 14:30 对比，按照涨幅排序，谁的涨势好，满仓买入谁。
    什么时候会清仓？
    当涨幅排序的第一名的涨跌幅为负数时，就会清仓。

    什么时候会换仓？
    举例，假设今天两点半之前，正在持有的品种是【创业板】，但两点半时，我们拿第一名的涨跌幅和持有的【创业板】进行比较，假设
    第一名【沪深300】的涨跌幅已经远高于正在持有的【创业板】，这时就进行了调仓。

策略特点：能抓住大涨，并能躲过大跌，收益高，交易次数少。

https://cloud.tencent.com/developer/article/1429693  学习资料
https://doc.shinnytech.com/tqsdk/latest/index.html
"""

import decimal

import requests
from tqsdk import TqApi, TqAuth


# 修改舍入方式为四舍五入
decimal.getcontext().rounding = "ROUND_HALF_UP"
code = {
    'sz399300': 510300,
    'sz399905': 510500,
    'sz399006': 159915
}


def get_data(symbol=None):
    """获取前 22 个交易的 14:30 数据 和 当前交易日的 14:30 数据的涨跌幅度"""
    if symbol is None:
        return 0

    response = requests.get(
        f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={symbol}&scale=30&ma=&datalen=220')
    data = response.json()
    data = [d for d in data if "14:30:00" in d['day']]
    increase = (float(data[-1]['close']) - float(data[-22]['close'])) / float(data[-22]['close']) * 100
    increase = float(decimal.Decimal(str(increase)).quantize(decimal.Decimal("0.00")))
    # print(f'{symbol} 涨跌幅度: {increase}')
    return {"symbol": symbol, "increase": increase}


def get_current_symbol():
    """获取当前持有的品种"""
    api = TqApi(auth=TqAuth("joyskang", "kang5113"))
    account = api.get_account()
    print(account)


def main():
    """主函数"""
    increases = [get_data('sz399300'), get_data('sz399905'), get_data('sz399006')]
    increases.sort(key=lambda k: -k['increase'])
    print(f'涨跌幅度排序: {increases}')


if __name__ == '__main__':
    # main()
    get_current_symbol()

