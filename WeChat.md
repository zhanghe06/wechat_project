## 微信公众平台接口测试帐号申请

[http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login](http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)


## 外网访问内网

[www.ngrok.cc](www.ngrok.cc)

```
$ cd tools/ngrok/linux_amd64
$ ./ngrok -config ngrok.cfg start wechat
```
```
Tunnel Status                 online
Version                       1.7/1.7
Forwarding                    https://zhanghe.ngrok.cc -> 127.0.0.1:5000
Forwarding                    http://zhanghe.ngrok.cc -> 127.0.0.1:5000
Web Interface                 127.0.0.1:4040
# Conn                        3
Avg Conn Time                 388.67ms
```


## 本实例中的配置信息

微信号： gh_feb29e69bcbb

### 测试号信息
appID
wx1cf9245f9f2cc40e
appsecret
d4624c36b6795d1d99dcf0547af5443d

### 接口配置信息
URL
http://zhanghe.ngrok.cc/weixin
Token
wechat_token

### JS接口安全域名
域名
zhanghe.ngrok.cc


[官方demo](http://203.195.235.76/jssdk/)


## 获取 token

```
curl https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

```
$ curl https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx1cf9245f9f2cc40e&secret=d4624c36b6795d1d99dcf0547af5443d
{"access_token":"gtmqjG1mHkGhPBwYwd272YHfJtkQn_7k-eS96iPMCd6HM3-CCCdvkVrd7lwNfDJQ1yyIQFPVfpQSpWBR_vHBuuSy9WEvljNazScdZ5bq9ghXwWAp_JKrqsQ5q3u16p4EJPIbAAABHA","expires_in":7200}
```
