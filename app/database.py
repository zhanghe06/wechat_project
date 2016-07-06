#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: database.py
@time: 16-7-6 下午15:10
"""


from flask.ext.sqlalchemy import SQLAlchemy
from app import app
db = SQLAlchemy(app)
