## 微信接口官方文档

[消息接口使用指南](http://mp.weixin.qq.com/wiki/home/index.html)

[微信JS-SDK说明文档](http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html)

[微信公众平台接口调试工具](http://mp.weixin.qq.com/debug/)

[微信支付文档](https://pay.weixin.qq.com/wiki/doc/api/index.html)

[模板消息接口](http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html)



## 常用接口

### 获取 token

接口地址
```
https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

示例
```
$ curl https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx1cf9245f9f2cc40e&secret=d4624c36b6795d1d99dcf0547af5443d
{"access_token":"gtmqjG1mHkGhPBwYwd272YHfJtkQn_7k-eS96iPMCd6HM3-CCCdvkVrd7lwNfDJQ1yyIQFPVfpQSpWBR_vHBuuSy9WEvljNazScdZ5bq9ghXwWAp_JKrqsQ5q3u16p4EJPIbAAABHA","expires_in":7200}
```


### 模板消息

接口地址
```
https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
```

POST 数据
```
{
    'touser': 'OPENID',
    'template_id': 'ngqIpbwh8bUfcSsECmogfXcV14J0tQlEpBO27izEYtY',
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
```


标题：购买成功通知
```
{{first.DATA}}

商品名称：{{product.DATA}}
商品价格：{{price.DATA}}
购买时间：{{time.DATA}}
{{remark.DATA}}
```


### 账号管理 - 生成带参数的二维码


## 上传图片

1、wx.chooseImage 接口选择图片
2、wx.uploadImage 接口上传图片有效期3天
3、下载多媒体文件到服务器


## 微信支付

支付申请
- 1、资料审核
- 2、账户验证
- 3、协议签署

开发配置

1、公众号支付

支付授权目录: http://zhanghe.ngrok.cc/weixin/demo/01/order/

2、扫码支付

支付回调URL: http://zhanghe.ngrok.cc/weixin/pay_notify_callback

注意:　申请支付, 必须是备案通过的

页面流程：
- 确认订单
    order_info
- 点击支付
    order_pay
- 处理结果
    pay_callback

## todo

一段Html代码给微信分享到朋友圈网页链接前加入小图标
