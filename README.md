## 环境安装

创建并进入虚拟环境
```
$ virtualenv wechat.env
$ source wechat.env/bin/activate
```

初始模块及扩展安装
```
$ pip install Flask
$ pip install Flask-Login
$ pip install Flask-Mail
$ pip install Flask-SQLAlchemy
$ pip install Flask-WTF
$ pip install Flask-OAuthlib
$ pip install 'requests[security]'
$ pip install sqlacodegen
$ pip install gunicorn
$ pip install supervisor
$ pip install schedule
$ pip install MySQL-python
$ pip install Pillow
$ pip freeze > requirements.txt
```

服务部署安装方式
```
$ pip install -r requirements.txt
```


## 测试账号接口调试

### 准备工作

- 通过 ngrok 实现端口转发

官网链接: [http://www.ngrok.cc](http://www.ngrok.cc); 免费的二级域名, 同时实现外网转发至内网本机

配置参数：tools/ngrok/linux_amd64/ngrok.cfg
```
server_addr: "server.ngrok.cc:4443"
auth_token: "a74ab29e0299e1eef89f7de6eb01c168" #授权token，在www.ngrok.cc平台注册账号获取
tunnels:
  wechat:
   subdomain: "zhanghe" #定义服务器分配域名前缀，跟平台上的要一样
   proto:
    http: 5000 #映射端口，不加ip默认本机
    https: 5000
```

- 微信公众平台接口测试帐号申请及配置

进入[微信测试账号申请入口/管理后台](http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)参考如下配置:

微信号： gh_feb29e69bcbb

测试号信息

配置项 | 参数
----|------
appID | wx1cf9245f9f2cc40e
appsecret | d4624c36b6795d1d99dcf0547af5443d


接口配置信息

配置项 | 参数
----|------
URL | http://zhanghe.ngrok.cc/weixin/callback
Token | wechat_token


JS接口安全域名

配置项 | 参数
----|------
域名 | zhanghe.ngrok.cc


### 开启 web 服务
```
$ python run.py
```

### 开启外网访问内网
```
$ cd tools/ngrok/linux_amd64
$ ./wechat clientid 68bd4946c5d53528
```

```
隧 道 状 态                           在 线
版 本                             2.0/2.0
转 发                             http://zhanghe.ngrok.cc -> 127.0.0.1:5000
Web界 面                          127.0.0.1:4040
# Conn                        0
Avg Conn Time                 0.00ms
```

### 手动更新 access_token 和 jsapi_ticket
```
更新微信开放平台 access_token
$ python task.py update_access_token

更新微信开放平台 jsapi_ticket
$ python task.py update_jsapi_ticket
```


[官方demo](http://203.195.235.76/jssdk/)

[官方调试工具](http://blog.qqbrowser.cc/)

[公众平台正式登录入口](https://mp.weixin.qq.com)


## Slideout.js 侧滑插件

[https://github.com/mango/slideout](https://github.com/mango/slideout)

安装
```
$ npm install slideout
```


## QRCode 二维码生成模块

```
$ pip install qrcode
```

[https://pypi.python.org/pypi/qrcode](https://pypi.python.org/pypi/qrcode)


## 字体图标

[http://www.h-ui.net/Hui-3.7-Hui-iconfont.shtml](http://www.h-ui.net/Hui-3.7-Hui-iconfont.shtml)

[http://www.gengyi.com/font/](http://www.gengyi.com/font/)

第一步：使用font-face声明字体
```
@font-face {font-family: 'iconfont';
    src: url('iconfont.eot'); /* IE9*/
    src: url('iconfont.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
    url('iconfont.woff') format('woff'), /* chrome、firefox */
    url('iconfont.ttf') format('truetype'), /* chrome、firefox、opera、Safari, Android, iOS 4.2+*/
    url('iconfont.svg#iconfont') format('svg'); /* iOS 4.1- */
}
```
第二步：定义使用iconfont的样式
```
.iconfont{
    font-family:"iconfont" !important;
    font-size:16px;font-style:normal;
    -webkit-font-smoothing: antialiased;
    -webkit-text-stroke-width: 0.2px;
    -moz-osx-font-smoothing: grayscale;
}
```
第三步：挑选相应图标并获取字体编码，应用于页面
```
<i class="iconfont">&#x33;</i>
```
