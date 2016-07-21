#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 16-6-6 上午11:09
"""


from flask import Flask, render_template
from .views.weixin import weixin_bp
from .views.demo import demo_bp


app = Flask(__name__)
app.config.from_object('config')


app.register_blueprint(weixin_bp)
app.register_blueprint(demo_bp)


@app.route('/')
@app.route('/index')
def index():
    """
    网站首页
    """
    return render_template('layout.html')
