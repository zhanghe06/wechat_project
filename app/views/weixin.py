#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weixin.py
@time: 16-7-13 下午6:20
"""


import json
import time
import hashlib
from config import APPID, APPSECRET, WECHAT_URL, WECHAT_TOKEN
from app.lib.sign import Sign
from flask import Blueprint, request, make_response, render_template, redirect, url_for, session
import xml.etree.ElementTree as ET
from requests import get, post
from urllib import quote_plus
from tools.wechat import get_access_token, get_jsapi_ticket, xml_rep_text, make_xml_response, dict_to_xml, xml_to_dict, check_required_params, create_nonce_str, create_sign, check_sign, get_prepay_id, get_js_api_parameters, create_oauth_url_for_code, create_oauth_url_for_openid
import logging
log = logging.getLogger('app')
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


weixin_bp = Blueprint('weixin', __name__, url_prefix='/weixin')


@weixin_bp.route('/')
def demo():
    """
    JS-SDK Demo
    http://zhanghe.ngrok.cc/weixin
    """
    sign = Sign(get_jsapi_ticket(), request.url.split('#')[0])
    sign.sign()
    data = {
        'appId': APPID,
        'timestamp': sign.ret['timestamp'],
        'nonceStr': sign.ret['nonceStr'],
        'signature': sign.ret['signature']
    }
    return render_template('demo.html', **data)


@weixin_bp.route('/callback', methods=['GET', 'POST'])
def callback():
    """
    验证服务器地址的有效性
    接口配置信息
        URL
        http://zhanghe.ngrok.cc/weixin/callback
        Token
        wechat_token
    GET /weixin?signature=0a96c67c0adf58d79ee57d5ee6837f896f70f9ec&echostr=601962190953118907&timestamp=1467559097&nonce=1527000568 HTTP/1.0
    """
    if request.method == 'GET':
        token = WECHAT_TOKEN  # your token
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
        else:
            return make_response(u'验证失败')

    if request.method == 'POST':
        # rec = request.stream.read()
        # xml_rec = ET.fromstring(rec)
        xml_rec = ET.fromstring(request.data)

        from_user = xml_rec.find('FromUserName').text
        to_user = xml_rec.find('ToUserName').text
        create_time = xml_rec.find('CreateTime').text
        msg_type = xml_rec.find('MsgType').text
        content = u''

        # 处理事件推送
        if msg_type == 'event':
            event = xml_rec.find('Event').text
            # 订阅/关注
            if event == 'subscribe':
                content = u'欢迎关注本微信'
                log.info(u'欢迎关注本微信')
            # 取消订阅/取消关注
            if event == 'unsubscribe':
                content = u'我们会慢慢改进，欢迎您以后再来'
                log.info(u'我们会慢慢改进，欢迎您以后再来')
            # 点击菜单拉取消息时的事件推送
            if event == 'CLICK':
                event_key = xml_rec.find('EventKey').text
                print event_key  # 自定义菜单接口中KEY值
                log.info(event_key)
            # 点击菜单跳转链接时的事件推送
            if event == 'VIEW':
                event_key = xml_rec.find('EventKey').text
                print event_key  # 跳转URL
            # 上报地理位置事件
            if event == 'LOCATION':
                latitude = xml_rec.find('Latitude').text  # 纬度
                longitude = xml_rec.find('Longitude').text  # 经度
                precision = xml_rec.find('Precision').text  # 精度
                print latitude
                print longitude
                print precision
            # 模板消息发送完成 是否送达成功通知
            if event == 'TEMPLATESENDJOBFINISH':
                status = xml_rec.find('Status').text
                # 'success'                 发送状态为成功
                # 'failed:user block'       发送状态为用户拒绝接收
                # 'failed: system failed'   发送状态为发送失败（非用户拒绝）
                print status
        # 处理文本消息
        if msg_type == "text":
            msg_id = xml_rec.find('MsgId').text
            content = xml_rec.find('Content').text
        # 处理图片消息
        if msg_type == 'image':
            msg_id = xml_rec.find('MsgId').text
            media_id = xml_rec.find('MediaId').text
            pic_url = xml_rec.find('PicUrl').text
        # 处理语音消息
        if msg_type == 'voice':
            msg_id = xml_rec.find('MsgId').text
            media_id = xml_rec.find('MediaId').text
            Format = xml_rec.find('Format').text  # 语音格式，如amr，speex等
        # 处理视频消息
        if msg_type == 'video':
            msg_id = xml_rec.find('MsgId').text
            media_id = xml_rec.find('MediaId').text  # 视频消息媒体id
            thumb_media_id = xml_rec.find('ThumbMediaId').text  # 视频消息缩略图的媒体id
        # 处理小视频消息
        if msg_type == 'shortvideo':
            msg_id = xml_rec.find('MsgId').text
            media_id = xml_rec.find('MediaId').text  # 视频消息媒体id
            thumb_media_id = xml_rec.find('ThumbMediaId').text  # 视频消息缩略图的媒体id
        # 处理地理位置消息
        if msg_type == 'location':
            msg_id = xml_rec.find('MsgId').text
            location_x = xml_rec.find('Location_X').text  # 维度
            location_y = xml_rec.find('Location_Y').text  # 经度
            scale = xml_rec.find('Scale').text  # 地图缩放大小
            label = xml_rec.find('Label').text  # 地理位置信息
        # 处理链接消息
        if msg_type == 'link':
            msg_id = xml_rec.find('MsgId').text
            title = xml_rec.find('Title').text
            description = xml_rec.find('Description').text
            url = xml_rec.find('Url').text
        return make_xml_response(xml_rep_text, from_user, to_user, str(int(time.time())), content)


@weixin_bp.route('/create_menu', methods=['GET', 'POST'])
def create_menu():
    """
    创建自定义菜单
    http://zhanghe.ngrok.cc/weixin/create_menu
    {
        "errcode": 0,
        "errmsg": "ok"
    }
    """
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
    data = {
        'button': [
            {
                'type': 'click',
                'name': '今日歌曲',
                'key': 'V1001_TODAY_MUSIC'
            },
            {
                'type': 'click',
                'name': '歌手简介',
                'key': 'V1001_TODAY_SINGER'
            },
            {
                'name': '菜单',
                'sub_button': [
                    {
                        'type': 'view',
                        'name': '搜索',
                        'url': 'http://www.soso.com/'
                    },
                    {
                        'type': 'view',
                        'name': '视频',
                        'url': 'http://v.qq.com/'
                    },
                    {
                        'type': 'click',
                        'name': '赞一下我们',
                        'key': 'V1001_GOOD'
                    },
                    {
                        'type': 'view',
                        'name': 'demo',
                        'url': 'http://zhanghe.ngrok.cc/weixin'
                    }]
            }]
    }

    res = post(url, data=json.dumps(data, ensure_ascii=False))
    return json.dumps(res.json())


@weixin_bp.route('/oauth')
@weixin_bp.route('/oauth/<scope>')
def oauth(scope='snsapi_base'):
    """
    网页授权入口页面
    http://zhanghe.ngrok.cc/weixin/oauth
    :param scope:
    :return:
    """
    oauth_callback_url = url_for('.oauth_callback', _external=True)
    oauth_url = create_oauth_url_for_code(oauth_callback_url, scope)
    return redirect(oauth_url)


@weixin_bp.route('/oauth_callback')
def oauth_callback():
    """
    网页授权回调地址
    获取 openid access_token
    (获取 code 之后的回调地址, 不能单独调用, 因code只能使用一次，5分钟未被使用自动过期)
    正确返回：
    {
        "access_token": "yZ37EaD08h2vG4Qq-GSEFmMTKpDcrdOuZK4mqh4JfUf46ui6sga022bPMhqHNnHQFSn1UGHsVuSZDtSDVen-94KiCmiEoBHwRoGcfizhosQ",
        "expires_in": 7200,
        "openid": "o9XD1weif6-0g_5MvZa7Bx6OkwxA",
        "refresh_token": "TCfFOMfSXbN5uSXbn9aaGzZBu7PsaN7iZZWvZKT2MpDaBl0aBO5itwe-1B7POcRxz_EAX6EuOGYt_aw0Smz9HCx-QDyqAewnhZSp5p2oNG4",
        "scope": "snsapi_base"
    }
    错误返回：
    {"errcode":40029,"errmsg":"invalid code"}
    """
    code = request.args.get('code')
    next_url = request.args.get('next_url')
    # 用户拒绝, 调回首页
    if code is None:
        return next_url or url_for('.demo')
    oauth_callback_url = create_oauth_url_for_openid(code)
    res = get(oauth_callback_url)
    result = json.dumps(res.json())
    log.info(result)
    session['openid'] = res.json().get('openid')
    return redirect(next_url or url_for('.demo'))


@weixin_bp.route('/get_code')
@weixin_bp.route('/get_code/<scope>')
def get_code(scope='snsapi_base'):
    """
    网页授权获取用户基本信息 - 用户同意授权，获取 code
    http://zhanghe.ngrok.cc/weixin/get_code
    http://zhanghe.ngrok.cc/weixin/get_code/snsapi_base
    http://zhanghe.ngrok.cc/weixin/get_code/snsapi_userinfo
    首先设置开发者中心页配置授权回调域名
    snsapi_base 返回结构：
    {'state': '', 'code': ''}
    snsapi_userinfo 返回结构：
    {'state': '', 'code': '', 'nsukey': ''}
    """
    redirect_uri = url_for('.get_openid_access_token', _external=True)
    # 微信会对授权链接做正则强匹配校验，链接的参数顺序固定
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=%s&scope=%s&state=%s#wechat_redirect' % (
        APPID,        # APPID
        quote_plus(redirect_uri),   # REDIRECT_URI
        'code',                     # response_type
        scope,                      # SCOPE (snsapi_base/snsapi_userinfo)
        time.time()                 # STATE
    )
    # return url
    return redirect(url)


@weixin_bp.route('/get_openid_access_token')
def get_openid_access_token():
    """
    获取 openid (获取 code 之后的回调地址, 不能单独调用, 因code只能使用一次，5分钟未被使用自动过期)
    http://zhanghe.ngrok.cc/get_openid_access_token
    正确返回：
    {
        "access_token": "yZ37EaD08h2vG4Qq-GSEFmMTKpDcrdOuZK4mqh4JfUf46ui6sga022bPMhqHNnHQFSn1UGHsVuSZDtSDVen-94KiCmiEoBHwRoGcfizhosQ",
        "expires_in": 7200,
        "openid": "o9XD1weif6-0g_5MvZa7Bx6OkwxA",
        "refresh_token": "TCfFOMfSXbN5uSXbn9aaGzZBu7PsaN7iZZWvZKT2MpDaBl0aBO5itwe-1B7POcRxz_EAX6EuOGYt_aw0Smz9HCx-QDyqAewnhZSp5p2oNG4",
        "scope": "snsapi_base"
    }
    错误返回：
    {"errcode":40029,"errmsg":"invalid code"}
    """
    code = request.args.get('code')
    # 用户拒绝, 调回首页
    if code is None:
        return url_for('.demo', _external=True)
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
        APPID,
        APPSECRET,
        code
    )
    res = get(url)
    return json.dumps(res.json())


@weixin_bp.route('/get_user_info')
def get_user_info():
    """
    基于微信网页授权 获取用户信息(关注公众号之后才有权限)
    http://zhanghe.ngrok.cc/weixin/get_user_info?access_token=ACCESS_TOKEN&openid=OPENID
    正确返回：
    {
        "province": "上海",
        "openid": "o9XD1weif6-0g_5MvZa7Bx6OkwxA",
        "headimgurl": "http://wx.qlogo.cn/mmopen/ALImIJLVKZtPiaaVkcKFR58xpgibiaxabiaStZYcwVNIfz4Tl8VkqzqpV5fKiaibbRGfkY2lDR9SlibQvVm2ClHD6AIhBYQeuy32qaj/0",
        "language": "zh_CN",
        "city": "闸北",
        "privilege": [],
        "country": "中国",
        "nickname": "碎ping子",
        "sex": 1
    }
    错误返回：
    {"errcode":40003,"errmsg":"invalid openid"}
    """
    access_token = request.args.get('access_token')
    openid = request.args.get('openid')
    lang = 'zh_CN'  # 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=%s' % (access_token, openid, lang)
    res = get(url)
    res.encoding = 'utf-8'  # 需要设置, 否则乱码
    return json.dumps(res.json(), ensure_ascii=False)


@weixin_bp.route('/auth_access_token')
def auth_access_token():
    """
    http://zhanghe.ngrok.cc/weixin/auth_access_token?access_token=ACCESS_TOKEN&openid=OPENID
    正确返回：
    {"errcode":0,"errmsg":"ok"}
    错误返回：
    {"errcode":40003,"errmsg":"invalid openid"}
    """
    access_token = request.args.get('access_token')
    openid = request.args.get('openid')
    url = 'https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s' % (access_token, openid)
    res = get(url)
    return json.dumps(res.json())


@weixin_bp.route('/send_tpl_msg/<openid>', methods=['GET', 'POST'])
def send_tpl_msg(openid):
    """
    发送模板消息
    http://zhanghe.ngrok.cc/weixin/send_tpl_msg/o9XD1weif6-0g_5MvZa7Bx6OkwxA
    {
        "msgid": 413348094,
        "errcode": 0,
        "errmsg": "ok"
    }
    """
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
    data = {
        'touser': str(openid),
        'template_id': '-5GfH3t-ofZooFA3CkPin8k-G0vb0_kJBcwcUmxcfEs',
        'url': 'http://weixin.qq.com/download',
        'data': {
            'first': {
                'value': '恭喜你购买成功！',
                'color': '#173177'
            },
            'product': {
                'value': '巧克力',
                'color': '#173177'
            },
            'price': {
                'value': '39.8元',
                'color': '#173177'
            },
            'time': {
                'value': '2014年9月22日',
                'color': '#173177'
            },
            'remark': {
                'value': '欢迎再次购买！',
                'color': '#173177'
            }
        }
    }
    res = post(url, data=json.dumps(data, ensure_ascii=False))
    return json.dumps(res.json())


@weixin_bp.route('/create_qrcode/<int:scene_id>', methods=['GET', 'POST'])
def create_qrcode(scene_id):
    """
    账号管理 - 生成带参数的二维码(临时/永久)
    http://zhanghe.ngrok.cc/weixin/create_qrcode/123
    一、创建二维码 ticket
    正确返回：
    {
        "url": "http://weixin.qq.com/q/LDrqzO-kgnL7ZxnNsRQx",
        "expire_seconds": 604800,
        "ticket": "gQH47joAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL0xEcnF6Ty1rZ25MN1p4bk5zUlF4AAIEak96VwMEgDoJAA=="
    }
    错误返回：
    {"errcode":40013,"errmsg":"invalid appid"}
    二、通过 ticket 换取二维码
    """
    access_token = get_access_token()
    # 创建二维码 ticket
    url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % access_token
    data = {
        'expire_seconds': 604800,
        'action_name': 'QR_SCENE',
        'action_info': {
            'scene': {
                'scene_id': scene_id
            }
        }
    }
    res = post(url, data=json.dumps(data, ensure_ascii=False))
    result = res.json()
    if 'errcode' in result:
        return json.dumps(result)

    # 通过 ticket 换取二维码
    url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s' % result['ticket']
    res = get(url)
    response = make_response(res.content)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@weixin_bp.route('/short_url', methods=['GET', 'POST'])
def short_url():
    """
    长链接转短链接接口
    http://zhanghe.ngrok.cc/weixin/short_url?long_url=LONG_URL
    正确返回：
    {"errcode":0,"errmsg":"ok","short_url":"http:\/\/w.url.cn\/s\/AvCo6Ih"}
    错误返回：
    {"errcode":40013,"errmsg":"invalid appid"}
    """
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/shorturl?access_token=%s' % access_token
    data = {
        'action': 'long2short',
        'long_url': request.args.get('long_url', '')
    }
    res = post(url, data=json.dumps(data, ensure_ascii=False))
    return json.dumps(res.json())


@weixin_bp.route('/order_unified', methods=['GET', 'POST'])
def order_unified():
    """
    微信支付 - 生成预支付交易单
    http://zhanghe.ngrok.cc/weixin/order_unified

    参考: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1

    字段名	    变量名	            必填	类型              描述
    公众账号ID	appid	            是	String(32)
    商户号	    mch_id	            是	String(32)
    设备号	    device_info	        否	String(32)      终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
    随机字符串	nonce_str	        是	String(32)
    签名	        sign	            是	String(32)
    商品描述	    body	            是	String(128)
    商品详情	    detail	            否	String(6000)    商品详细列表，使用Json格式
    附加数据	    attach	            否	String(127)
    商户订单号	out_trade_no	    是	String(32)
    货币类型	    fee_type	        否	String(16)      符合ISO 4217标准的三位字母代码，默认人民币：CNY
    总金额	    total_fee	        是	Int             订单总金额，单位为分
    终端IP	    spbill_create_ip	是	String(16)
    交易起始时间	time_start	        否	String(14)      格式为yyyyMMddHHmmss
    交易结束时间	time_expire	        否	String(14)      格式为yyyyMMddHHmmss
    商品标记	    goods_tag	        否	String(32)
    通知地址	    notify_url	        是	String(256)
    交易类型	    trade_type	        是	String(16)      取值如下：JSAPI，NATIVE，APP
    商品ID	    product_id	        否	String(32)      trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。
    指定支付方式	limit_pay	        否	String(32)      no_credit--指定不能使用信用卡支付
    用户标识	    openid	            否	String(128)     trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。

    detail = {
        'goods_detail': [
            {
                'goods_id': '',         # String 必填 32 商品的编号
                'wxpay_goods_id': '',   # String 可选 32 微信支付定义的统一商品编号
                'goods_name': '',       # String 必填 256 商品名称
                'goods_num': '',        # Int 必填 商品数量
                'price': '',            # Int 必填 商品单价，单位为分
                'goods_category': '',   # String 可选 32 商品类目ID
                'body': ''              # String 可选 1000 商品描述信息
            }
        ]
    }
    """
    if request.method == 'POST':
        dict_data = request.form.to_dict()
        dict_data['spbill_create_ip'] = request.headers.get('X-Forwarded-For', request.remote_addr)
        # 获取预支付交易会话标识
        prepay_id = get_prepay_id(dict_data)
        # 获取jsapi的参数
        js_api_parameters = get_js_api_parameters(prepay_id)
        return json.dumps(js_api_parameters)


@weixin_bp.route('/order_query', methods=['GET', 'POST'])
def order_query():
    """
    查询订单
    http://zhanghe.ngrok.cc/weixin/order_query

    参考: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2
    """
    url = 'https://api.mch.weixin.qq.com/pay/orderquery'
    pass


@weixin_bp.route('/order_close', methods=['GET', 'POST'])
def order_close():
    """
    查询订单(订单生成后不能马上调用关单接口，最短调用时间间隔为5分钟。)
    http://zhanghe.ngrok.cc/weixin/order_close

    参考: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_3
    """
    url = 'https://api.mch.weixin.qq.com/pay/closeorder'
    pass


@weixin_bp.route('/refund', methods=['GET', 'POST'])
def refund():
    """
    申请退款(请求需要双向证书)
    http://zhanghe.ngrok.cc/weixin/refund

    参考: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_4
    """
    url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
    pass


@weixin_bp.route('/refund_query', methods=['GET', 'POST'])
def refund_query():
    """
    申请退款(请求需要双向证书)
    http://zhanghe.ngrok.cc/weixin/refund_query

    参考: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_5
    """
    url = 'https://api.mch.weixin.qq.com/pay/refundquery'
    pass


@weixin_bp.route('/download_bill', methods=['GET', 'POST'])
def download_bill():
    """
    下载对账单
    1、未成功下单的交易不会出现在对账单中。支付成功后撤销的交易会出现在对账单中，跟原支付单订单号一致，bill_type为REVOKED；
    2、微信在次日9点启动生成前一天的对账单，建议商户10点后再获取；
    3、对账单中涉及金额的字段单位为“元”。
    4、对账单接口只能下载三个月以内的账单。

    http://zhanghe.ngrok.cc/weixin/download_bill

    参考: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_6
    """
    url = 'https://api.mch.weixin.qq.com/pay/downloadbill'
    pass


@weixin_bp.route('/pay_notify_callback', methods=['GET', 'POST'])
def pay_notify_callback():
    """
    支付通知回调
    http://zhanghe.ngrok.cc/weixin/pay_notify_callback
    """
    if request.method == 'POST':
        result = {
            'return_code': 'SUCCESS'
        }
        res_dict = xml_to_dict(request.data)
        try:
            # 记录回调通知信息
            log.info(json.dumps(res_dict, ensure_ascii=False))
            if res_dict.get('return_code') == 'FAIL':  # 此字段是通信标识，非交易标识，交易是否成功需要查看result_code来判断
                raise Exception(u'请求服务失败')
            if res_dict.get('result_code') == 'FAIL':  # 业务结果
                raise Exception(res_dict.get('err_code_des') or u'申请支付失败')
            # 验证签名
            res_sign_str = res_dict.pop('sign')
            if create_sign(res_dict) != res_sign_str:
                raise Exception(u'签名失败')
            # 订单支付成功处理
            # todo
        except Exception as e:
            result['return_code'] = 'FAIL'
            result['return_msg'] = e.message
            # 订单支付失败处理
            # todo
        finally:
            return dict_to_xml(result)
