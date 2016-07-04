#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 16-6-6 上午11:09
"""


from flask import Flask
app = Flask(__name__)
app.config.from_object('config')


from app import views
