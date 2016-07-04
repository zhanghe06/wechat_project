## 微信接口官方文档

[消息接口使用指南](http://mp.weixin.qq.com/wiki/home/index.html)

[微信JS-SDK说明文档](http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html)

[微信公众平台接口调试工具](http://mp.weixin.qq.com/debug/)

[微信支付文档](https://pay.weixin.qq.com/wiki/doc/api/index.html)

[模板消息接口](http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html)



## 常用接口

获取 token

```
curl https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

示例
```
$ curl https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx1cf9245f9f2cc40e&secret=d4624c36b6795d1d99dcf0547af5443d
{"access_token":"gtmqjG1mHkGhPBwYwd272YHfJtkQn_7k-eS96iPMCd6HM3-CCCdvkVrd7lwNfDJQ1yyIQFPVfpQSpWBR_vHBuuSy9WEvljNazScdZ5bq9ghXwWAp_JKrqsQ5q3u16p4EJPIbAAABHA","expires_in":7200}
```





## todo

一段Html代码给微信分享到朋友圈网页链接前加入小图标
