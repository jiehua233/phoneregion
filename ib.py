#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   http://chenjiehua.me
# @date     2016-01
#

import os.path

ib = None

def init_infobright():
    drop_table('phonenum')
    create_table('phonenum')
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phonenum.dat")
    load_data_infile(file_path, 'phonenum')

def drop_table(table_name):
    ib.execute('DROP TABLE IF EXISTS `%s`' % table_name)

def create_table(table_name):
    ib.execute('''
CREATE TABLE IF NOT EXISTS `%s` (
`phone` int(11) COLLATE utf8_unicode_ci NOT NULL COMMENT '手机号码前7位',
`region` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '卡号归属地',
`cardtype` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '卡类型',
`regioncode` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '区号',
`postcode` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '邮编'
) ENGINE=brighthouse DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
               ''' % table_name)

def load_data_infile(file_path, table_name):
    ib.execute(
        '''LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY '\\t' LINES TERMINATED BY '\\n'
        ''' % (file_path, table_name))
