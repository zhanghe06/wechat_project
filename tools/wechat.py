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


if __name__ == '__main__':
    print get_access_token()
    print get_jsapi_ticket()
