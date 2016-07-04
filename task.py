#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task.py
@time: 16-7-2 下午5:21
"""


import schedule
import time


def get_access_token():
    """
    获取微信开放平台 access_token
    """
    from requests import get
    from config import APPID, APPSECRET
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID, APPSECRET)
    response = get(url)
    result = response.json()
    access_token = result['access_token']
    # expires_in = result['expires_in']  # 7200
    with open('access_token', 'w') as f:
        f.write(access_token)
    print result


def run():
    """
    启动
    """
    schedule.every().hour.do(get_access_token)  # 每小时调度一次

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
