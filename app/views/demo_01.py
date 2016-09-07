#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: demo_01.py
@time: 16-7-21 下午2:16
"""


from config import APPID, APPSECRET
import time
import json
from app.lib.sign import Sign
from tools.wechat import get_access_token, get_jsapi_ticket, xml_rep_text, make_xml_response
from flask import Blueprint, request, make_response, render_template, redirect, url_for, session
import logging
log = logging.getLogger('app')


demo_01_bp = Blueprint('demo_01', __name__, url_prefix='/demo/01')


@demo_01_bp.route('/')
@demo_01_bp.route('/home/')
def home():
    """
    http://127.0.0.1:5000/demo/01/
    http://127.0.0.1:5000/demo/01/home
    """
    return render_template('demo_01/slide_home.html')


@demo_01_bp.route('/search/')
def search():
    """
    http://127.0.0.1:5000/demo/01/search
    """
    return render_template('demo_01/slide_search.html')


@demo_01_bp.route('/product/')
def product():
    """
    http://127.0.0.1:5000/demo/01/product
    """
    return render_template('demo_01/slide_product.html')


@demo_01_bp.route('/order/')
def order():
    """
    http://127.0.0.1:5000/demo/01/order
    """
    if 'openid' not in session:
        return redirect('http://gwm.91shixing.com/_gwm/zhanghe/weixin/oauth')
    log.info(request.url)
    # sign = Sign(get_jsapi_ticket(), request.url)
    sign = Sign(get_jsapi_ticket(), 'http://gwm.91shixing.com/_gwm/zhanghe/demo/01/order/')
    sign.sign()
    data = {
        # 配置信息
        'appId': APPID,
        'timestamp': sign.ret['timestamp'],
        'nonceStr': sign.ret['nonceStr'],
        'signature': sign.ret['signature'],
    }
    order_info = {
        # 订单信息
        'out_trade_no': 'PO001'+time.strftime("%Y%m%d%H%M%S"),
        'attach': 'testattach',
        'body': '测试订单',
        'total_fee': 1,
        'trade_type': 'JSAPI',
        'openid': session['openid'],
        'device_info': 'WEB'
    }
    order_info = json.dumps(order_info)
    return render_template('demo_01/slide_order.html', order_info=order_info, **data)


@demo_01_bp.route('/pay/')
def pay():
    """
    http://127.0.0.1:5000/demo/01/pay
    """
    if 'openid' not in session:
        return redirect('http://gwm.91shixing.com/_gwm/zhanghe/weixin/oauth')
    log.info(request.url)
    # sign = Sign(get_jsapi_ticket(), request.url)
    sign = Sign(get_jsapi_ticket(), 'http://gwm.91shixing.com/_gwm/zhanghe/demo/01/order/')
    sign.sign()
    data = {
        # 配置信息
        'appId': APPID,
        'timestamp': sign.ret['timestamp'],
        'nonceStr': sign.ret['nonceStr'],
        'signature': sign.ret['signature'],
    }
    order_info = {
        # 订单信息
        'out_trade_no': 'PO001'+time.strftime("%Y%m%d%H%M%S"),
        'attach': 'testattach',
        'body': '测试订单',
        'total_fee': 1,
        'trade_type': 'JSAPI',
        'openid': session['openid'],
        'device_info': 'WEB'
    }
    order_info = json.dumps(order_info)
    return render_template('demo_01/slide_order.html', order_info=order_info, **data)


@demo_01_bp.route('/me/')
def me():
    """
    http://127.0.0.1:5000/demo/01/me
    """
    sign = Sign(get_jsapi_ticket(), request.url)
    sign.sign()
    data = {
        'appId': APPID,
        'timestamp': sign.ret['timestamp'],
        'nonceStr': sign.ret['nonceStr'],
        'signature': sign.ret['signature']
    }
    return render_template('demo_01/slide_me.html', **data)
