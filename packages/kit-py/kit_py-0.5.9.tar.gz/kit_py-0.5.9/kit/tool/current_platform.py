# -*- coding: utf-8 -*-
"""
@Author  : miclon
@Time    : 2022/8/17
@Desc    : 获取当前系统平台
@Example
    process:
    current_platform()

    output:
    mac

"""
import sys


def current_platform() -> str:
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    elif sys.platform.startswith('win') or sys.platform.startswith('msys') or sys.platform.startswith('cyg'):
        if sys.maxsize > 2 ** 31 - 1:
            return 'win64'
        return 'win32'
    raise OSError('Unsupported platform: ' + sys.platform)


if __name__ == '__main__':
    print(current_platform())  # mac
