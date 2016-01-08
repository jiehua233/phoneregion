#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   http://chenjiehua.me
# @date     2016-01
#

""" falcon server api """

import torndb
import falcon
from wsgiref import simple_server

import config


def validate_phonenum(req, resp, resource, params):
    print params
    params['phonenum'] = '123'


class PhoneResource(object):

    def __init__(self, ib):
        self.ib = torndb.Connection(**ib)
        pass

    @falcon.before(validate_phonenum)
    def on_get(self, req, resp, phonenum):
        print phonenum
        resp.status = falcon.HTTP_200
        resp.body = ""


app = falcon.API()
phone = PhoneResource(config.INFOBRIGHT)
app.add_route('/phone/{phonenum}', phone)


if __name__ == "__main__":
    host = config.SERVER['host']
    port = config.SERVER['port']
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
