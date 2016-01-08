#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import argparse
import torndb
import ib
import scrapy
import config

def main():
    args = parse_cmdline()
    ib.ib = torndb.Connection(**config.INFOBRIGHT)
    if args.initdb:
        ib.init_infobright()

    if args.scrapy:
        scrapy.scrapy_phone()


def parse_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scrapy', default=0, const=1, type=int, choices=[0, 1], nargs='?')
    parser.add_argument('--initdb', default=0, const=1, type=int, choices=[0, 1], nargs='?')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
