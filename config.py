#!/usr/bin/env python
# -*- coding: utf-8 -*-

INFOBRIGHT = {
    "host": "127.0.0.1:5029",
    "user": "root",
    "password": "root",
    "database": "phonenum",
    "local_infile": 1,
}

SCRAPY = {
    "thread_num": 50,
}

SERVER = {
    "host": "127.0.0.1",
    "port": 9999,
}

"""Gunicorn setting"""
bind = "127.0.0.1:9999"
workers = 1
worker_class = "gevent"
accesslog = "-"     # log to stderr
errorlog = "-"      # log to stderr
loglevel = "info"
