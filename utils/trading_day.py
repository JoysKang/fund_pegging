import datetime

from chinese_calendar import is_workday, is_holiday


def is_trading_day():
    """今天是否是交易日"""
    today = datetime.date.today()
    if is_workday(today) and not is_holiday(today):
        return True

    return False


if __name__ == '__main__':
    print(is_trading_day())
