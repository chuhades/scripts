#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
requests 补丁，上下文，User-Agent，超时，忽略 ssl 错误，stream
"""

from contextlib import contextmanager
from functools import partial

import requests


@contextmanager
def request(method, url, *args, **kwargs):
    """
    request 基础函数
    :param method: HTTP method
    :type method: str
    :param url: 链接地址
    :type url: str
    :param timeout: 超时时间
    :type timeout: int

    :return: 请求对象
    :rtype: requests.models.Response
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko)Chrome/37.0.2062.124 Safari/537.36"
    }
    custom = {
        "headers": headers,
        "timeout": 10,
        "verify": False,
        "stream": True
    }
    for key, value in custom.items():
        if key not in kwargs:
            kwargs[key] = value
    req = requests.request(method, url, *args, **kwargs)

    try:
        yield req
    except Exception:
        pass
    finally:
        req.close()


get = partial(request, "GET")
post = partial(request, "POST")
options = partial(request, "OPTIONS")
head = partial(request, "HEAD")
put = partial(request, "PUT")
patch = partial(request, "PATCH")
delete = partial(request, "DELETE")