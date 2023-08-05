# -*- coding: utf-8 -*-
import string
from random import randint, choice

from typing import Optional, Tuple

_characters = string.ascii_letters + string.digits


def to_string(s, encoding=None, errors='strict'):
    if isinstance(s, str):
        return s
    if not isinstance(s, (bytes, bytearray)):
        return str(s)
    return s.decode(encoding or 'utf-8', errors)


def to_bytes(s, encoding=None, errors='strict'):
    if isinstance(s, bytes):
        return s
    if not isinstance(s, str):
        return bytes(s)
    return s.encode(encoding or 'utf-8', errors)


def random_string(min_len=3, max_len=20, characters=None):
    characters = characters or _characters
    _len = randint(min_len, max_len) if max_len > min_len else min_len
    return ''.join((choice(characters) for _ in range(_len)))


def get_section(
        original_str: str,
        start_str: Optional[str] = None,
        end_str: Optional[str] = None
) -> Tuple[Optional[str], Optional[int], Optional[int]]:
    """
    获取字符串区间内容
    :param original_str: 原始字符串
    :param start_str: 开始字符串
    :param end_str: 结束字符串
    :return: 区间内容
    >>> get_section('abc123def', 'abc', 'def')
    ('123', 3, 6)
    >>> get_section('abc123def', 'abc')
    ('123def', 3, 9)
    >>> get_section('abc123def', end_str='def')[0]
    'abc123'
    """
    if start_str is None:
        start_ = 0
    else:
        start_ = original_str.find(start_str)
        if start_ >= 0:
            start_ += len(start_str)
        else:
            return None, start_, None
    if end_str is None:
        end_ = len(original_str)
    else:
        end_ = original_str.find(end_str, start_)
    if end_ >= 0:
        return original_str[start_:end_], start_, end_
    return None, None, None


def get_middle(
        original_str: str,
        start_str: str,
        end_str: str
) -> Optional[str]:
    """
    获取字符串中间内容
    :param original_str: 原始字符串
    :param start_str: 开始字符串
    :param end_str: 结束字符串
    :return: 中间内容
    >>> get_middle('abc123def', 'abc', 'def')
    '123'
    """
    find_str, _, _ = get_section(original_str, start_str, end_str)
    return find_str


def get_middle_batch(
        original_str: str,
        start_str: str,
        end_str: str
) -> list:
    """
    获取字符串中间内容
    :param original_str: 原始字符串
    :param start_str: 开始字符串
    :param end_str: 结束字符串
    :return: 中间内容
    >>> get_middle_batch('abc123def456abc789def', 'abc', 'def')
    ['123', '789']
    """
    result = []
    while True:
        find_str, start_, end_ = get_section(original_str, start_str, end_str)
        if find_str is None:
            break
        result.append(find_str)
        original_str = original_str[end_:]
    return result


def get_left(
        original_str: str,
        end_str: str
) -> Optional[str]:
    """
    获取字符串左边内容
    :param original_str: 原始字符串
    :param end_str: 结束字符串
    :return: 左边内容
    >>> get_left('abc123def', 'def')
    'abc123'
    """
    find_str, _, _ = get_section(original_str, end_str=end_str)
    return find_str


def get_right(
        original_str: str,
        start_str: str
) -> Optional[str]:
    """
    获取字符串右边内容
    :param original_str: 原始字符串
    :param start_str: 开始字符串
    :return: 右边内容
    >>> get_right('abc123def', 'abc')
    '123def'
    """
    find_str, _, _ = get_section(original_str, start_str=start_str)
    return find_str


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)