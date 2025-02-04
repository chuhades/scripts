#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import sys
from urlparse import urlparse


class IPToDomain(object):
    """
    Bing API 反查域名
    """
    @classmethod
    def get_domains_per_page(cls, url):
        """
        获取Bing API 中每一页返回的域名
        @param url: API 地址
        @type url: str

        @return: domains, next_page
        @rtype: tuple, (set, str)
        """
        auth_key = "qDHY+qgadeaiRPiM3znc5pnUJvTxuk9+7MNSosTjUjo="
        r = requests.get(url=url, auth=("", auth_key))
        r.close()
        results = r.json().get("d").get("results")
        next_page = r.json().get("d").get("__next")
        domains = set()
        for result in results:
            domain = "://".join(urlparse(result.get("Url"))[0:2])
            domains.add(domain)
        return domains, next_page

    @classmethod
    def get_domains(cls, ip):
        """
        Bing API 反查域名
        @param ip: IP 地址
        @type ip: str

        @return: domains
        @rtype: set
        """
        domains = set()
        next_page = "https://api.datamarket.azure.com/Bing/Search/v1/Web?" \
                    "Query='ip:%s'&$format=JSON" % ip
        while next_page:
            domains_per_page, next_page = cls.get_domains_per_page(next_page)
            if next_page:
                next_page += "&$format=JSON"
            domains = domains.union(domains_per_page)
        return domains


def main():
    domains = IPToDomain.get_domains(sys.argv[1])
    for domain in domains:
        print domain

if __name__ == "__main__":
    main()