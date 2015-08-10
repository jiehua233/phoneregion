#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import torndb
from bs4 import BeautifulSoup

db = torndb.Connection('localhost', 'phonenum', 'root', 'jiehua123')

def main():
    pres = db.query("SELECT * FROM `prefix`")
    for pre in pres:
        for i in range(9999):
            phone = pre['num'] + format(i, '04')
            print phone
            getip138(phone)


def getip138(phone):
    url = "http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile" % phone
    r = requests.get(url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.find_all('td', class_="tdc2")
    #for a in s:
    #    print a.contents
    try:
        region = s[1].contents[-1].strip()
        cardtype = s[2].contents[-1].strip()
        regioncode = s[3].contents[0].strip()
        postcode = s[4].contents[0].strip()
        #print region, cardtype, regioncode, postcode
        db.execute("INSERT INTO `ip138`(`phone`, `region`, `cardtype`, `regioncode`, `postcode`)"
                "VALUES(%s, %s, %s, %s, %s)", phone, region, cardtype, regioncode, postcode)
    except Exception, e:
        print e


if __name__ == "__main__":
    main()

