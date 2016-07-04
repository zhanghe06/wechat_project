#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run.py
@time: 16-6-6 上午11:12
"""


from app import app


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
