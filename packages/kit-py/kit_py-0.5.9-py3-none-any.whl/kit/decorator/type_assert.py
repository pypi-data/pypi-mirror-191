# -*- coding: utf-8 -*-
"""
@Author  : miclon
@Time    : 2022/9/9
@Desc    : 校验函数参数类型
@Example

    @type_assert(int, list, str)
    def fn(a, b, c): ...

    process:
    fn(1, [], 'miclon') # pass
    fn(1, 'm', 'miclon')  # b must be <class 'list'>

"""
import inspect


def type_assert(*ty_args, **ty_kwargs):
    def decorator(func):
        func_sig = inspect.signature(func)
        bind_type = func_sig.bind_partial(*ty_args, **ty_kwargs).arguments

        def wrap(*args, **kwargs):
            for name, obj in func_sig.bind(*args, **kwargs).arguments.items():
                type_ = bind_type.get(name)
                if type_:
                    if not isinstance(obj, type_):
                        raise TypeError('%s must be %s' % (name, type_))
            return func(*args, **kwargs)

        return wrap

    return decorator


@type_assert(int, list, str)
def fn(a, b, c):
    pass


@type_assert(c=int)
def fn2(a, b, c):
    pass


if __name__ == '__main__':
    fn(1, [], 'miclon')  # pass
    # fn(1, 'm', 'miclon')  # b must be <class 'list'>

    fn2(1, 2, 3)  # pass
    # fn2("1", {}, [])    # c must be <class 'int'>
