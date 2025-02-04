#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
map http(s) service from portscan.log
"""

from gevent import monkey; monkey.patch_all()

import argparse
import logging
import warnings
import urlparse

import requests
from lxml import html
from gevent.pool import Pool


# default settings
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko)Chrome/37.0.2062.124 Safari/537.36"
}
TIMEOUT = 2


# ignore https insecure warning
warnings.filterwarnings("ignore")


# logging
logger_console_handler = logging.StreamHandler()
logger_console_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("mh")
logger_console_handler.setFormatter(logger_console_formatter)
logger.addHandler(logger_console_handler)
logger.setLevel(logging.INFO)


def maphttp(addr):
    """
    测试是否是 http(s)
    :param addr: 主机地址，192.168.0.1:21
    :type addr: str
    """
    for scheme in ("http", "https"):
        url = urlparse.urlunparse((scheme, addr, "/", "", "", ""))
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True, verify=False)
            title = html.fromstring(resp.content).find(".//title")
            resp.close()
            msg = "{}, {}, {}, {}".format(addr, resp.url, resp.status_code, title.text.strip().encode("utf-8") if title is not None else "")
            logger.info(msg)
            with open("maphttp.log", "a") as fd:
                fd.write("{}\n".format(msg))
            break
        except Exception as err:
            logger.debug("{}, {}".format(url, err))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", action="store_true", help="show debug message")
    parser.add_argument("-n", type=int, default=50, help="coroutine num")
    parser.add_argument("-t", type=int, default=2, help="timeout")
    parser.add_argument("log", type=argparse.FileType("r"), help="portscan log file")

    args = parser.parse_args()

    # log level
    if args.v:
        logger.setLevel(logging.DEBUG)

    # 超时
    global TIMEOUT
    TIMEOUT = args.t

    # 识别
    pool = Pool(args.n)
    pool.map(maphttp, args.log.read().splitlines())
    pool.join()
    args.log.close()


if __name__ == "__main__":
    main()
