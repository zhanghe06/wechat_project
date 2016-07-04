#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: views.py
@time: 16-6-6 下午1:07
"""

import json
import os
import time
import hashlib
from app import app
from app.lib.sign import Sign
from flask import request, make_response, render_template
import xml.etree.ElementTree as ET
from requests import get, post
from tools.wechat import get_access_token, get_jsapi_ticket


@app.route('/')
def demo():
    sign = Sign(get_jsapi_ticket(), request.url)
    sign.sign()
    data = {
        'appId': app.config['APPID'],
        'timestamp': sign.ret['timestamp'],
        'nonceStr': sign.ret['nonceStr'],
        'signature': sign.ret['signature']
    }
    return render_template('demo.html', **data)


@app.route('/weixin', methods=['GET', 'POST'])
def wechat_auth():
    """
    验证服务器地址的有效性
    接口配置信息
        URL
        http://zhanghe.ngrok.cc/weixin
        Token
        wechat_token
    GET /weixin?signature=0a96c67c0adf58d79ee57d5ee6837f896f70f9ec&echostr=601962190953118907&timestamp=1467559097&nonce=1527000568 HTTP/1.0
    """
    if request.method == 'GET':
        token = 'wechat_token'  # your token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if hashlib.sha1(s).hexdigest() == signature:
            return make_response(echostr)

    if request.method == 'POST':
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        # xml_rec = ET.fromstring(request.data)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu, tou, str(int(time.time())), content))
        response.content_type = 'application/xml'
        return response


@app.route('/create_menu', methods=['GET', 'POST'])
def create_menu():
    """
    创建自定义菜单
    """
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
    menu_data = {
        "button": [
            {
                "type": "click",
                "name": "今日歌曲",
                "key": "V1001_TODAY_MUSIC"
            },
            {
                "type": "click",
                "name": "歌手简介",
                "key": "V1001_TODAY_SINGER"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "视频",
                        "url": "http://v.qq.com/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    },
                    {
                        "type": "view",
                        "name": "demo",
                        "url": "http://zhanghe.ngrok.cc/"
                    }]
            }]
    }

    res = post(url, data=json.dumps(menu_data, ensure_ascii=False))
    return json.dumps(res.json())
