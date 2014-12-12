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

import requests
import threadpool
from docopt import docopt
from sys import exit
from time import time


class DirBuster(object):
    """
    核心类
    """

    def __init__(self, base_url, dict_file, thread_num, keyword, output_file):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.dict_file = dict_file
        self.thread_num = thread_num
        self.keyword = keyword
        self.output_file = output_file
        self.result = []
        self.ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) "
                   "Gecko/20100101 Firefox/31.0")

    def judge(self, filename):
        """
        判断是否存在文件
        :param filename: 文件名
        :return: 确定存在的文件
        """
        result = None
        url = self.base_url + filename

        try:
            r = requests.get(url,
                             headers={"User-Agent": self.ua},
                             stream=True,
                             allow_redirects=False,
                             timeout=3)
            if r.status_code in (200, 403):
                if self.keyword:
                    if "content-length" in r.headers \
                            and r.headers["content-length"] / 1000000:
                        result = "[%d] %s" % (r.status_code, url)
                    else:
                        r.encoding = r.apparent_encoding
                        if not self.keyword in r.text:
                            result = "[%d] %s" % (r.status_code, url)
                else:
                    result = "[%d] %s" % (r.status_code, url)
            r.close()
            return result
        except Exception:
            return None

    def log(self, request, result):
        """
        threadpool callback
        :param request:
        :param result:
        :return:
        """
        if result:
            print result
            self.result.append(result)

    def run(self):
        """
        主函数
        :return:
        """
        files = [i.strip() for i in open(self.dict_file)]
        pool = threadpool.ThreadPool(self.thread_num)
        reqs = threadpool.makeRequests(self.judge, files, self.log)
        for req in reqs:
            pool.putRequest(req)
        pool.wait()
        if self.output_file:
            with open(self.output_file, "w") as f:
                for i in self.result:
                    f.write(i + "\r\n")


def main():
    arguments = docopt(__doc__, version="1.0")
    dir_buster = DirBuster(arguments["<baseurl>"],
                           arguments["<dict>"],
                           int(arguments["-t"]),
                           arguments["-k"],
                           arguments["-o"])
    print "-" * 80
    dir_buster.run()
    print "-" * 80
    exit()


if __name__ == "__main__":
    main()
