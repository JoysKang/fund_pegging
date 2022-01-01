"""
趋势模型的逻辑（来自微信公众号:量化投基）：
沪深300、中证500、创业板，

每个交易日的 14:30 与自己前 22 个交易日的 14:30 对比，谁的涨势好，满仓买入谁。

策略特点：能抓住大涨，并能躲过大跌，收益高，交易次数少。
"""

import json
import datetime

import akshare as ak
import requests


# https://cloud.tencent.com/developer/article/1429693  学习资料


def get_data(symbol=None):
    """获取前 22 个交易的 14:30 数据"""
    if symbol is None:
        return 0

    params = (
        ('symbol', symbol),
        ('scale', '30'),
        ('ma', 'no'),
        ('datalen', '1023'),
    )

    response = requests.get(
        f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={symbol}&scale=30&ma=&datalen=220',
        params=params)
    data = response.json()
    data = [d for d in data if "14:30:00" in d['day']]
    close = data[-22]['close']
    print(f'{symbol} 前 22 个交易日的 14:30 收盘价为 {close}')


def main():
    """主函数"""
    get_data('sz399300')    # 沪深300
    get_data('sz399905')    # 中证500
    get_data('sz399006')    # 创业板


if __name__ == '__main__':
    main()

