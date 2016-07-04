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
$ pip freeze > requirements.txt
```

服务部署安装方式
```
$ pip install -r requirements.txt
```

