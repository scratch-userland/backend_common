# -*- coding: utf-8 -*-
import base64
import functools
import hashlib
import json
import os
import random
from threading import Thread

import datetime as dt
import time
from Crypto.Cipher import AES


def generate_trade_no():
    return ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(16)))


def generate_no(now=None):
    now = now or dt.datetime.now()
    return '%s%s%s' % (now.strftime('%Y%m%d%H%M%S'),
                       int(round(time.time() * 1000)),
                       random.randint(10, 99))


def compare_list(ori_list, new_list):
    unchanged_list = list(set(ori_list).intersection(set(new_list)))
    deleted_list = list(set(ori_list) - set(new_list))
    newly_list = list(set(new_list) - set(ori_list))
    return unchanged_list, deleted_list, newly_list


def get_hash(obj):
    """:return Hash result by md5."""
    return hashlib.md5(obj).hexdigest()


def encrypt(rawstr):
    cipher = AES.new("ot-$7Y0z(WH=3l>re_XC|t0?%T^Ka|dd")
    bs = AES.block_size

    def pad(s):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    rawstr = base64.b64encode(rawstr)
    result = cipher.encrypt(pad(rawstr)).encode('hex')
    return result


def decrypt(ciphertext):
    def unpad(s):
        return s[0: -ord(s[-1])]

    cipher = AES.new("ot-$7Y0z(WH=3l>re_XC|t0?%T^Ka|dd")
    result = unpad(cipher.decrypt(ciphertext.decode('hex')))
    result = base64.b64decode(result)
    return result


def decipher_url(temp_url):
    url_args = decrypt(temp_url)
    return parse_url_args_to_dict(url_args)


def parse_url_args_to_dict(args):
    _dict = {}
    args = args.split('&')
    for arg in args:
        k_v = arg.split('=')
        _dict.setdefault(k_v[0], k_v[1])
    return _dict


def json_safe_dumps(params):
    return json.dumps({k: v or '' for k, v in params.items()})


def async(func):
    """
    A decorator to handle asynchronous job.
    :param func:
    :return:
    """

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return decorator
