# -*- coding: utf-8 -*-
"""
@Author  : miclon
@Time    : 2022/8/16
@Desc    : cookies转字典
@Example

    input:
    cookie_str = "code=1000; name=miclon; UID=359FEA9A6F1C7E97BFE909A1A700F5DE"

    process:
    cookies_to_dict(cookie_str)

    output:
    {'code': '1000', 'name': 'miclon', 'UID': '359FEA9A6F1C7E97BFE909A1A700F5DE'}
"""


def cookies_to_dict(cookies: str):
    return {cookie.split('=')[0]: cookie.split('=')[-1] for cookie in cookies.split('; ')}


if __name__ == '__main__':
    cookie_str = "code=1000; name=miclon; UID=359FEA9A6F1C7E97BFE909A1A700F5DE"
    print(cookies_to_dict(cookie_str))
    # {'code': '1000', 'name': 'miclon', 'UID': '359FEA9A6F1C7E97BFE909A1A700F5DE'}
