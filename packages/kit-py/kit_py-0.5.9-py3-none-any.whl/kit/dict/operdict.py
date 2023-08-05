# -*- coding: utf-8 -*-
def find_keys(original_dict: dict, val: any) -> list:
    """
    查找字典中指定值的所有键
    :param original_dict: 原始字典
    :param val: 指定值
    :return: 键列表
    >>> find_keys({'a': 1, 'b': 2, 'c': 3}, 2)
    ['b']
    """
    return list(key for key, value in original_dict.items() if value == val)


def reverse(original_dict: dict) -> dict:
    """
    反转字典
    :param original_dict: 原始字典
    :return: 反转后的字典
    >>> reverse({'a': 1, 'b': 2, 'c': 3})
    {1: 'a', 2: 'b', 3: 'c'}
    """
    return {v: k for k, v in original_dict.items()}


def sort_by_key(original_dict: dict, az: bool = False) -> dict:
    """
    按键排序
    :param original_dict: 原始字典
    :param az: 是否升序 True: 升序 False: 降序
    :return: 排序后的字典
    >>> sort_by_key({'c': 1, 'b': 2, 'a': 3})
    {'a': 3, 'b': 2, 'c': 1}
    """
    return dict(sorted(original_dict.items(), reverse=az))


def sort_by_value(original_dict: dict, az: bool = False) -> dict:
    """
    按值排序
    :param original_dict: 原始字典
    :param az: 是否升序 True: 升序 False: 降序
    :return: 排序后的字典
    >>> sort_by_value({'c': 1, 'b': 2, 'a': 3})
    {'c': 1, 'b': 2, 'a': 3}
    """
    return dict(sorted(original_dict.items(), key=lambda x: x[1], reverse=az))


def merge(original_dict: dict, *others) -> dict:
    """
    合并字典
    :param original_dict: 原始字典
    :param others: 其他字典
    :return: 合并后的字典
    >>> merge({'a': 1, 'b': 2}, {'c': 3, 'd': 4})
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    """
    merged_dict = {}
    for other in others:
        merged_dict.update(other)
    return {**original_dict, **merged_dict}


def merge_with_list(original_dict: dict, other_dict: dict) -> dict:
    """
    合并字典中的列表
    :param original_dict: 原始字典
    :param other_dict: 其他字典
    :return: 合并后的字典
    >>> merge_with_list({'a': [1, 2], 'b': 2}, {'a': [3, 4], 'd': 4})
    {'a': [1, 2, 3, 4], 'b': 2, 'd': 4}
    """
    combined_keys = original_dict.keys() | other_dict.keys()
    for key in combined_keys:
        if isinstance(original_dict.get(key), list) and isinstance(other_dict.get(key), list):
            original_dict[key] = original_dict.get(key, []) + other_dict.get(key, [])
        else:
            original_dict[key] = other_dict.get(key, original_dict.get(key))
    return original_dict
