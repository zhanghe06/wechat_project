#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: demo.py
@time: 16-7-20 上午9:47
"""


from flask import Blueprint, request, make_response, render_template, redirect, url_for


demo_bp = Blueprint('demo', __name__, url_prefix='/demo')


@demo_bp.route('/01/')
def index_01():
    return render_template('demo_01/index.html')


@demo_bp.route('/02/')
def index_02():
    return render_template('demo_02/index.html')


@demo_bp.route('/03/')
def index_03():
    return render_template('demo_03/index.html')
