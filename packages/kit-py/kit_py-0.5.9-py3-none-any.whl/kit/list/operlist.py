# -*- coding: utf-8 -*-
from typing import Generator, List, Dict, Callable, Optional


def split_list_average_n(origin_list: List, n: int) -> Generator[List, None, None]:
    """
    按指定数量平均分割列表
    :param origin_list: 原始列表
    :param n: 指定数量
    :return: 分割后的列表

    >>> list(split_list_average_n([1, 2, 3, 4, 5, 6, 7, 8, 9], 3))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    for i in range(0, len(origin_list), n):
        yield origin_list[i:i + n]


def objects_to_object(arr: List[Dict], key: str) -> Dict:
    """
    将对象列表转换为指定key名的对象
    :param arr: 对象列表
    :param key: 指定key名
    :return: 指定key名的对象

    >>> objects_to_object([{'id': 1, 'name': 'miclon'}, {'id': 2, 'name': 'miclon2'}], 'id')
    {1: {'id': 1, 'name': 'miclon'}, 2: {'id': 2, 'name': 'miclon2'}}
    """
    return {b[key]: b for b in arr}

def dedupe(items: List, key: Optional[Callable] = None):
    """
    列表去重，保持顺序
    >>> list(dedupe([1, 5, 2, 1, 9, 1, 5, 10]))
    [1, 5, 2, 9, 10]
    >>> list(dedupe([{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}], key=lambda d: (d['x'], d['y'])))
    [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
    """
    seen = set()
    for item in items:
        value = item if key is None else key(item)
        if value not in seen:
            yield item
            seen.add(value)