#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: wechat.py
@time: 16-7-4 上午11:11
"""


import os


def get_access_token():
    """
    读取微信开放平台 access_token
    """
    access_token_file_name = '/'.join((os.path.dirname(os.path.abspath(__file__)), '../access_token'))
    with open(access_token_file_name, 'r') as f:
        access_token = f.read()
    return access_token


def get_jsapi_ticket():
    """
    读取微信开放平台 jsapi_ticket
    """
    jsapi_ticket_file_name = '/'.join((os.path.dirname(os.path.abspath(__file__)), '../jsapi_ticket'))
    with open(jsapi_ticket_file_name, 'r') as f:
        jsapi_ticket = f.read()
    return jsapi_ticket


if __name__ == '__main__':
    print get_access_token()
    print get_jsapi_ticket()
