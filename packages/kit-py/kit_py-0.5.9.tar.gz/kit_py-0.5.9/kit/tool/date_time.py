# -*- coding: utf-8 -*-
from itertools import chain
from datetime import datetime, timedelta

# 较为通用的时间格式
DATETIME_COMMON = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y年%m月%d日%H:%M:%S",
    "%Y年%m月%d日 %H:%M:%S",
    "%Y年%m月%d日%H时%M分%S秒",
    "%Y年%m月%d日 %H时%M分%S秒"
)
DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y%m%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%d.%m.%y",
    "%d.%m.%Y",
    "%Y %m %d",
    "%m/%d/%Y",
)

DATETIME_FORMATS = list(
    chain.from_iterable(
        [
            ["{} %H:%M:%S".format(fmt) for fmt in DATE_FORMATS],
            ["{} %H:%M".format(fmt) for fmt in DATE_FORMATS],
            ["{}T%H:%M:%S.%f%z".format(fmt) for fmt in DATE_FORMATS]
        ]
    )
)


def get_timestamp() -> int:
    """
    获取10位当前时间戳
    :return: 时间戳
    """
    return int(datetime.now().timestamp())


def get_timestamp13() -> int:
    """
    获取13位当前时间戳
    :return: 时间戳
    """
    return int(datetime.now().timestamp() * 1000)


def get_now(fmt=None) -> str:
    """
    获取当前时间
    :param fmt: 时间格式
    :return: 时间
    """
    _fmt = fmt or '%Y-%m-%d %H:%M:%S'
    return datetime.now().strftime(_fmt)


def get_before_time(num, unit=None, fmt=None):
    """
    获取当前时间之前的时间
    :param num: 数量
    :param unit: 单位
    :param fmt: 时间格式
    :return: 时间
    """
    _fmt = fmt or '%Y-%m-%d %H:%M:%S'
    _unit = unit or 'days'
    return (datetime.now() - timedelta(**{_unit: num})).strftime(_fmt)


def datetime_to_str(date: datetime, fmt=None):
    """
    日期转字符串
    :param date: 日期
    :param fmt: 时间格式
    :return: 时间
    """
    _fmt = fmt or '%Y-%m-%d %H:%M:%S'
    return date.strftime(_fmt)


date_to_str = datetime_to_str   # 兼容旧版本


def str_to_datetime(s: str, fmt=None) -> datetime:
    """
    字符串转日期，当fmt为None时，会尝试多种格式，直到成功。
    :param s: 字符串
    :param fmt: 时间格式
    :return: 日期
    """
    s = s.strip()
    if fmt is not None:
        return datetime.strptime(s, fmt)
    for fmt in chain.from_iterable((DATETIME_COMMON,
                                    DATETIME_FORMATS,
                                    DATE_FORMATS)):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"No valid date format found for '{s}'")


if __name__ == '__main__':
    print(get_timestamp())
    print(get_timestamp13())
    print(get_before_time(30, 'days'))
    # 1639656228
