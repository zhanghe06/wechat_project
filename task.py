#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task.py
@time: 16-7-2 下午5:21
"""


import sys
import schedule
import time
from requests import get
from config import APPID, APPSECRET
from tools.wechat import get_access_token, get_jsapi_ticket


def update_access_token():
    """
    更新微信开放平台 access_token
    access_token 是公众号的全局唯一票据，公众号调用各接口时都需使用 access_token
    """
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID, APPSECRET)
    response = get(url)
    result = response.json()
    access_token = result['access_token']
    # expires_in = result['expires_in']  # 7200
    with open('access_token', 'w') as f:
        f.write(access_token)
    print result


def update_jsapi_ticket():
    """
    更新微信开放平台 jsapi_ticket
    jsapi_ticket 是公众号用于调用微信JS接口的临时票据
    """
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
    response = get(url)
    result = response.json()
    if result['errcode'] == 0:
        ticket = result['ticket']
        # expires_in = result['expires_in']  # 7200
        with open('jsapi_ticket', 'w') as f:
            f.write(ticket)
    print result


def wechat():
    """
    微信定时任务调度
    """
    schedule.every().hour.do(update_access_token)  # 每小时调度一次
    schedule.every().hour.do(update_jsapi_ticket)  # 每小时调度一次

    while True:
        schedule.run_pending()
        time.sleep(1)


def usage():
    """
    使用说明
    """
    print """
更新微信开放平台 access_token
$ python task.py update_access_token

更新微信开放平台 jsapi_ticket
$ python task.py update_jsapi_ticket

微信定时任务调度
$ python task.py wechat
"""


def run():
    """
    入口
    """
    # print sys.argv
    try:
        if len(sys.argv) > 1:
            fun_name = eval(sys.argv[1])
            fun_name()
        else:
            print '缺失参数\n'
            usage()
    except NameError, e:
        print e
        print '未定义的方法[%s]' % sys.argv[1]


if __name__ == '__main__':
    run()
