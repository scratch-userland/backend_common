# -*- coding: utf-8 -*-

from decimal import Decimal

from flask_restful import fields


def cent_to_yuan(cent):
    if cent is None:
        return 0.00
    return float(Decimal(str(cent / 100.00)))


def yuan_to_cent(yuan):
    if yuan is None:
        return 0
    value = Decimal(str(yuan * 100.0))
    return int(value)


class YuanFormat(fields.Raw):
    def format(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return value / 100.00
        else:
            return value


class DateFormat(fields.Raw):
    def format(self, value):
        return unicode(value)


class TimeFormat(fields.Raw):
    def format(self, value):
        return unicode(value)
