#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   http://chenjiehua.me
# @date     2016-01
#

import sys
import logging
import requests
import gevent
from gevent import monkey; monkey.patch_all()
from bs4 import BeautifulSoup
from config import SCRAPY

reload(sys)
sys.setdefaultencoding('utf8')

def scrapy_phone():
    instance = Scrapy()
    instance.run()


class Scrapy:

    fh = None
    thread_num = 1

    def __init__(self):
        self.thread_num = SCRAPY['thread_num']

    def run(self):
        with open("phonenum.dat", "wb") as self.fh:
            prefixs = self.generate_prefix()
            for prefix in prefixs:
                phone_list = [str(prefix) + format(i, '04') for i in range(9999)]
                self.process_with_gevent(phone_list)

    def generate_prefix(self):
        """ 生成收集号码前缀 """
        prefixs = [145, 147, 149]
        prefixs.extend(range(130, 140))
        prefixs.extend(range(150, 160))
        prefixs.extend(range(170, 190))
        return prefixs

    def process_with_gevent(self, phone_list):
        """ 采用gevent进行处理 """
        jobs = [gevent.spawn(self.worker, phone_list) for i in range(self.thread_num)]
        gevent.joinall(jobs)

    def worker(self, phone_list):
        while len(phone_list) > 0:
            phone = phone_list.pop()
            print "validating: ", phone
            info = self.validate(phone)
            if info is not None:
                print phone, 'is ok.'
                self.fh.write("%(phone)s\t%(region)s\t%(cardtype)s\t%(regioncode)s\t%(postcode)s\n" % info)

    def validate(self, phone):
        url = "http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile" % phone
        r = requests.get(url)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, "html5lib")
        s = soup.find_all('td', class_="tdc2")
        #for a in s:
        #    print a.contents
        #print region, cardtype, regioncode, postcode
        try:
            result = {
                "phone": phone,
                "region": s[1].contents[-1].strip(),
                "cardtype": s[2].contents[-1].strip(),
                "regioncode": s[3].contents[0].strip(),
                "postcode": s[4].contents[0].strip(),
            }
            return result

        except Exception as e:
            pass

        return None


