#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 ___________
< DirBuster >
 -----------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||

Usage:
    dirbuster.py <baseurl> <dict> [-t thread_num] [-k keyword] [-o output_file]
    dirbuster.py -h

Options:
    -t thread_num       线程数 [default: 20]
    -k keyword          404 页面关键字
    -o output_file      输出文件
    -h                  show help

Example:
    dirbuster.py http://sh3ll.me/www/ PHP.txt
    dirbuster.py http://sh3ll.me/www/ PHP.txt -t 30

"""
from gevent import monkey
from gevent.lock import BoundedSemaphore
from gevent.pool import Pool
monkey.patch_all()

import requests
from docopt import docopt


lock = BoundedSemaphore()
results = []


def judge(url, keyword=None):
    """
    判断是否存在文件
    :param url: 链接
    :type url: str
    :param keyword: 404 页面关键字
    :type keyword: str
    """
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
                             " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                             "39.0.2171.95 Safari/537.36"}
    try:
        result = ""
        r = requests.get(url,
                         headers=headers,
                         stream=True,
                         allow_redirects=False,
                         timeout=3)
        if r.status_code in (200, 403):
            if keyword:
                if "content-length" in r.headers \
                        and r.headers["content-length"] / 1000000:
                    result = "[%d] %s" % (r.status_code, url)
                else:
                    r.encoding = r.apparent_encoding
                    if keyword not in r.text:
                        result = "[%d] %s" % (r.status_code, url)
            else:
                result = "[%d] %s" % (r.status_code, url)
        r.close()
        if result:
            with lock:
                print result
                results.append(result)
    except:
        pass


def main():
    arguments = docopt(__doc__, version="1.0")
    base_url = arguments["<baseurl>"]
    dict_file = arguments["<dict>"]
    thread_num = int(arguments["-t"])
    keyword = arguments["-k"]
    output_file = arguments["-o"]

    base_url = base_url[:-1] if base_url.endswith("/") else base_url
    pool = Pool(thread_num)
    print "-" * 80
    with open(dict_file) as _dict:
        for line in _dict:
            url = base_url + line.strip()
            pool.spawn(judge, url, keyword)
    pool.join()
    if output_file:
        with open(output_file, "w") as log:
            for result in results:
                log.write(result + "\r\n")
    print "-" * 80

if __name__ == "__main__":
    main()