#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: wechat.py
@time: 16-7-4 上午11:11
"""


import os
from flask import make_response
import xml.etree.ElementTree as ET
import hashlib
import time
import json
import random
import string
from urllib import quote_plus
from requests import get, post
from config import APPID, APPSECRET, MCHID, WECHAT_TOKEN, WECHAT_PAY_KEY, WECHAT_NOTIFY_URL
import logging
log = logging.getLogger('app')
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


def get_access_token():
    """
    读取微信开放平台 access_token
    """
    access_token_file_name = '/'.join((os.path.dirname(os.path.abspath(__file__)), '../access_token'))
    with open(access_token_file_name, 'r') as f:
        access_token = f.read().rstrip()
    return access_token


def get_jsapi_ticket():
    """
    读取微信开放平台 jsapi_ticket
    """
    jsapi_ticket_file_name = '/'.join((os.path.dirname(os.path.abspath(__file__)), '../jsapi_ticket'))
    with open(jsapi_ticket_file_name, 'r') as f:
        jsapi_ticket = f.read().rstrip()
    return jsapi_ticket


def make_xml_response(xml_rep_tpl, *args):
    """
    创建 xml 响应消息
    """
    response = make_response(xml_rep_tpl % args)
    response.content_type = 'application/xml'
    return response


# 被动回复用户消息 http://mp.weixin.qq.com/wiki/14/89b871b5466b19b3efa4ada8e577d45e.html

# 回复文本消息
xml_rep_text = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>'''


# 回复图片消息
xml_rep_img = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<Image>
<MediaId><![CDATA[%s]]></MediaId>
</Image>
</xml>'''


# 回复语音消息
xml_rep_voice = '''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[voice]]></MsgType>
<Voice>
<MediaId><![CDATA[%s]]></MediaId>
</Voice>
</xml>
'''


# 回复视频消息
xml_rep_video = '''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[video]]></MsgType>
<Video>
<MediaId><![CDATA[%s]]></MediaId>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
</Video>
</xml>
'''


# 回复音乐消息
xml_rep_music = '''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[music]]></MsgType>
<Music>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<MusicUrl><![CDATA[%s]]></MusicUrl>
<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>
</Music>
</xml>
'''


# 回复图文消息  todo 多条记录
xml_rep_articles = '''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>%s</ArticleCount>
<Articles>
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
</Articles>
</xml>
'''


def dict_to_xml(dict_data):
    """
    dict转xml
    """
    xml = ['<xml>']
    for k, v in dict_data.iteritems():
        if v.isdigit():
            xml.append('<{0}>{1}</{0}>'.format(k, v))
        else:
            xml.append('<{0}><![CDATA[{1}]]></{0}>'.format(k, v))
    xml.append('</xml>')
    return ''.join(xml)


def xml_to_dict(xml):
    """
    将xml转为dict
    """
    dict_data = {}
    root = ET.fromstring(xml)
    for child in root:
        value = child.text
        dict_data[child.tag] = value
    return dict_data


def check_required_params(params, dict_data):
    """
    校验必填项
    """
    for param in params:
        if param not in dict_data:
            raise Exception(u'缺少必填参数: %s' % param)
    return True


def create_nonce_str(length=32):
    """
    产生随机字符串，不长于32位
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def format_biz_query_para_map(para_map):
    """
    格式化参数，签名过程需要使用
    :param para_map:
    :return:
    """
    params_str = '&'.join(['%s=%s' % (k, v) for k, v in sorted(para_map.items()) if k != 'sign' and v != ''])
    return params_str


def create_sign(params_dict):
    """
    生成签名
    :param params_dict: 去除sign之后的参数
    :return:
    """
    # 签名步骤一：按字典序排序参数
    params_str = format_biz_query_para_map(params_dict)
    # 签名步骤二：在string后加入KEY
    params_str = '{0}&key={1}'.format(params_str, WECHAT_PAY_KEY)
    # 签名步骤三：MD5加密
    params_str = hashlib.md5(params_str).hexdigest()
    # 签名步骤四：所有字符转为大写
    result = params_str.upper()
    return result


def check_sign(params_dict, signature):
    """
    检测支付签名
    :param params_dict: 去除sign之后的参数
    :param signature:
    :return:
    """
    if create_sign(params_dict) == signature:
        return True
    raise Exception(u'签名错误！')


def get_prepay_id(dict_data):
    """
    获取预支付交易会话标识
    :param dict_data: 订单数据
    :return:
    """
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    # 必填参数检测
    params = ['out_trade_no', 'body', 'total_fee', 'trade_type']
    check_required_params(params, dict_data)
    # 关联参数检测
    if dict_data.get('trade_type') == 'JSAPI' and not dict_data.get('openid'):
        raise Exception(u'trade_type为JSAPI时，openid为必填参数！')
    if dict_data.get('trade_type') == 'NATIVE' and not dict_data.get('product_id'):
        raise Exception(u'trade_type为NATIVE时，product_id为必填参数！')
    # 异步通知url未设置，则使用配置文件中的url
    if not dict_data.get('notify_url'):
        dict_data['notify_url'] = WECHAT_NOTIFY_URL

    dict_data['appid'] = APPID  # 公众账号ID
    dict_data['mch_id'] = MCHID  # 商户号
    dict_data['nonce_str'] = create_nonce_str()  # 随机字符串
    dict_data['sign'] = create_sign(dict_data)  # 签名
    log.info(json.dumps(dict_data, indent=4, ensure_ascii=False))
    xml = dict_to_xml(dict_data)
    log.info(xml)
    headers = {'Content-Type': 'application/xml'}
    res = post(url, data=xml, headers=headers)
    res.encoding = 'utf-8'
    log.info(res.text)
    res_dict = xml_to_dict(res.text)
    if res_dict.get('return_code') == 'FAIL':  # 此字段是通信标识，非交易标识，交易是否成功需要查看result_code来判断
        raise Exception(res_dict.get('return_msg') or u'请求服务失败')
    if res_dict.get('result_code') == 'FAIL':  # 业务结果
        raise Exception(res_dict.get('err_code_des') or u'申请支付失败')
    # 申请成功，校验签名(如果WECHAT_PAY_KEY泄露，结果可以伪造)
    res_sign_str = res_dict.pop('sign')
    if create_sign(res_dict) != res_sign_str:
        raise Exception(u'签名校验失败')
    log.info(json.dumps(res_dict, indent=4, ensure_ascii=False))
    return res_dict['prepay_id']


def get_js_api_parameters(prepay_id):
    """
    获取jsapi的参数
    :param prepay_id:
    :return:
    """
    js_api_obj = dict()
    js_api_obj['appId'] = APPID
    js_api_obj['timeStamp'] = int(time.time())
    js_api_obj['nonceStr'] = create_nonce_str()
    js_api_obj['package'] = 'prepay_id={0}'.format(prepay_id)
    js_api_obj['signType'] = 'MD5'
    js_api_obj['paySign'] = create_sign(js_api_obj)
    parameters = json.dumps(js_api_obj)
    return parameters


def create_oauth_url_for_code(redirect_url, scope='snsapi_base'):
    """
    生成可以获得code的url
    :param redirect_url:
    :param scope:
    :return:
    """
    url_obj = dict()
    url_obj['appid'] = APPID
    url_obj['redirect_uri'] = quote_plus(redirect_url)
    url_obj['response_type'] = 'code'
    url_obj['scope'] = scope  # (snsapi_base/snsapi_userinfo)
    url_obj['state'] = 'STATE#wechat_redirect'
    biz_str = format_biz_query_para_map(url_obj)
    return 'https://open.weixin.qq.com/connect/oauth2/authorize?' + biz_str


def create_oauth_url_for_openid(code):
    """
    生成可以获得openid的url
    :param code:
    :return:
    """
    url_obj = dict()
    url_obj['appid'] = APPID
    url_obj['secret'] = APPSECRET
    url_obj['code'] = code
    url_obj['grant_type'] = 'authorization_code'
    biz_str = format_biz_query_para_map(url_obj)
    return 'https://api.weixin.qq.com/sns/oauth2/access_token?' + biz_str


if __name__ == '__main__':
    print get_access_token()
    print get_jsapi_ticket()
    print create_nonce_str()
