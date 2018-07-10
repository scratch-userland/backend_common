# -*- coding: utf-8 -*-
from functools import wraps

from ..base import raise_400_response


def digit_value(f):
    @wraps(f)
    def decorated_function(value, field):
        if value is None or value == '':
            return 0
        if isinstance(value, (str, unicode)):
            if not value.isdigit():
                raise_400_response(message=u'请输入数字')
        elif not isinstance(value, int):
            raise_400_response(message=u'请输入数字')
        return f(int(value), field)

    return decorated_function


def string_value(f):
    @wraps(f)
    def decorated_function(value, *args, **kwargs):
        if not isinstance(value, (str, unicode)):
            raise_400_response(message=u'请输入合法字符串')
        value = value.strip()
        return f(value, *args, **kwargs)

    return decorated_function
