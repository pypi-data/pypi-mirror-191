# -*- coding: utf-8 -*-
"""
@Author  : miclon
@Time    : 2022/9/6
@Desc    : 字符串导入模块
@Example
    process:
    import_object('this')

    output:
    The Zen of Python, by Tim Peters
    ……

"""
import functools
import importlib


def import_object(value):
    modname, varname = value, None
    if ":" in value:
        modname, varname = value.split(":", 1)

    module = importlib.import_module(modname)
    if varname is not None:
        varnames = varname.split(".")
        try:
            return module, functools.reduce(getattr, varnames, module)
        except AttributeError:
            raise ImportError("Module %r does not define a %r variable." % (modname, varname)) from None
    return module, None


if __name__ == '__main__':
    # obj = import_object('this')
    obj = import_object('kit.dict:Dict')
    print(obj)
