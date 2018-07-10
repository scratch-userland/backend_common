# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

from flask_restful import fields
from pytz import timezone


def get_beijing_time(utc_time, utc_fmt='%Y-%m-%dT%H:%M:%SZ'):
    return datetime.strptime(utc_time, utc_fmt) + timedelta(hours=8)


def get_timezone_datetime(local_datetime, zone_name):
    sh_zone = timezone('Asia/Shanghai')
    target_zone = timezone(zone_name)
    local_datetime = sh_zone.localize(local_datetime)
    target_datetime = local_datetime.astimezone(target_zone)
    return target_datetime


def time_to_str(t):
    if t:
        return t.strftime('%H:%M:%S')
    else:
        return None


def date_to_str(date):
    if date:
        return date.strftime('%Y-%m-%d')
    else:
        return None


def datetime_to_str(datetime):
    if datetime:
        return datetime.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None


def timedelta_to_minutes(td):
    return td.seconds // 60


def get_monday_and_sunday(_date=None):
    if _date:
        _monday = _date - timedelta(_date.weekday())
    else:
        _monday = datetime.now() - timedelta(datetime.now().weekday())
    return _monday, _monday + timedelta(6)


def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step


class DatetimeFormat(fields.Raw):
    def format(self, value):
        try:
            return time.mktime(value.timetuple()) * 1000
        except Exception:
            return None


def Caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    return date2-date1
