#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   https://chenjiehua.me
# @date     2017-01-03
#

import sys
import gzip
import logging
import argparse
import gevent
import torndb
import requests
from gevent import monkey
from bs4 import BeautifulSoup
from etc import config


reload(sys)
sys.setdefaultencoding("utf-8")
monkey.patch_all()
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO)
db = torndb.Connection(**config.MYSQL)


def main():
    args = parse_cmdline()

    if args.scrapy:
        instance = Scrapy()
        instance.run()

    if args.loaddb:
        init_database()


def parse_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scrapy', default=0, const=1, type=int, choices=[0, 1], nargs='?')
    parser.add_argument('--loaddb', default=0, const=1, type=int, choices=[0, 1], nargs='?')
    args = parser.parse_args()
    return args


def init_database():
    logging.info("Truncate table...")
    db.execute("TRUNCATE `phonenum`")
    logging.info("Load data into table...")
    with gzip.open("etc/phonenum.dat.gz") as f:
        for line in f:
            try:
                p, r, c, rc, pc = line.strip().split("\t")
                db.execute(
                    "INSERT INTO `phonenum`(`phone`, `region`, `cardtype`, `regioncode`, `postcode`)"
                    "VALUES(%s, %s, %s, %s, %s)", p, r, c, rc, pc)
            except Exception as e:
                logging.error("line: %s, err: %s", line, e)


class Scrapy:

    fh = None
    thread_num = 1

    def __init__(self):
        self.thread_num = config.SCRAPY['thread_num']

    def run(self):
        with gzip.open("etc/phonenum.dat.gz", "wb") as self.fh:
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
            logging.info("total: %s, validating %s", len(phone_list), phone)
            info = self.validate(phone)
            if info is not None:
                logging.info("%s is ok.", phone)
                self.fh.write("%(phone)s\t%(region)s\t%(cardtype)s\t%(regioncode)s\t%(postcode)s\n" % info)

    def validate(self, phone):
        url = "http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile" % phone
        r = requests.get(url)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, "html5lib")
        s = soup.find_all('td', class_="tdc2")
        try:
            region = s[1].contents[-1].strip()
            # print "region:", region
            cardtype = s[2].contents[-1].strip()
            # print "cardtype", cardtype
            regioncode = s[3].contents[0].strip()
            # print "regioncode", regioncode
            postcode = s[4].contents[0].strip()
            # print "postcode", postcode
            result = {
                "phone": phone,
                "region": region,
                "cardtype": cardtype,
                "regioncode": regioncode,
                "postcode": postcode,
            }
            return result
        except:
            pass

        return None


if __name__ == "__main__":
    main()
