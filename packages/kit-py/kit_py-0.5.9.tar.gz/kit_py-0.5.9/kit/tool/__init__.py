# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse
from uuid import uuid4
from .import_object import import_object
from .current_platform import current_platform
from .date_time import *
from .random_useragent import get_useragent
from .clean_html import clean_html

__all__ = [
    'cookies_to_dict',
    'headers_to_dict',
    'data_to_dict',
    'import_object',
    'current_platform',
    'get_timestamp',
    'get_timestamp13',
    'get_now',
    'get_useragent',
    'datetime_to_str',
    'date_to_str',
    'str_to_datetime',
    'gen_unique_id',
    'get_domain',
    'clean_html',
]


def cookies_to_dict(cookies: str):
    return {cookie.split('=')[0]: cookie.split('=')[-1] for cookie in cookies.split('; ')}


def headers_to_dict(headers: str) -> dict:
    return {header.split(':')[0]: header.split(':')[-1] for header in headers.split('\r\n')}


def data_to_dict(data: str) -> dict:
    return {item.split('=')[0]: item.split('=')[-1] for item in data.split('&')}


def gen_unique_id():
    return f"{uuid4().hex}"


def get_domain(url: str, filter_ports=None) -> str:
    """从URL中获取域名"""
    if filter_ports is None:
        filter_ports = [80, 443]
    netloc = urlparse(url).netloc
    split_netloc = netloc.split(':')
    if len(split_netloc) == 1:
        return netloc

    if len(split_netloc) == 2:
        if int(split_netloc[-1]) in filter_ports:
            return split_netloc[0]
        return netloc



