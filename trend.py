"""
趋势模型的逻辑（来自微信公众号:量化投基）：
沪深300、中证500、创业板，

每个交易日的 14:30 与自己前 22 个交易日的 14:30 对比，谁的涨势好，满仓买入谁。

策略特点：能抓住大涨，并能躲过大跌，收益高，交易次数少。
"""

import json
import datetime

import akshare as ak

# https://cloud.tencent.com/developer/article/1429693  学习资料


def get_data():
    """获取前 22 个交易的 14:30 数据"""

    import requests

    params = (
        ('symbol', 'sz399300'),
        ('scale', '30'),
        ('ma', 'no'),
        ('datalen', '1023'),
    )

    response = requests.get(
        'https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sz399300_30_1638272168085=/CN_MarketDataService.getKLineData',
        params=params)
    start = response.text.find('=(') + 2
    end = len(response.text) - 2
    data = json.loads(response.text[start:end])
    data = [d for d in data if "14:30:00" in d['day']]
    # print(data)
    print(data[-22]['close'])


if __name__ == '__main__':
    get_data()

