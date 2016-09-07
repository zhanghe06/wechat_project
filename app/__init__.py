#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 16-6-6 上午11:09
"""


from flask import Flask, render_template
from app.lib.qiniu_store import QiNiuClient
from logging.config import dictConfig
from .views.weixin import weixin_bp
from .views.demo import demo_bp
from .views.demo_01 import demo_01_bp


app = Flask(__name__)
app.config.from_object('config')

# 配置日志
dictConfig(app.config['LOG_CONFIG'])

# 七牛云存储
qi_niu_client = QiNiuClient(app)

app.register_blueprint(weixin_bp)
app.register_blueprint(demo_bp)
app.register_blueprint(demo_01_bp)


@app.route('/')
@app.route('/index')
def index():
    """
    网站首页
    """
    return render_template('layout.html')
