#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test.py
@time: 16-3-10 下午5:10
"""
import json
ss = {"province": "上海", "openid": "o9XD1weif6-0g_5MvZa7Bx6OkwxA", "headimgurl": "http://wx.qlogo.cn/mmopen/ALImIJLVKZtPiaaVkcKFR58xpgibiaxabiaStZYcwVNIfz4Tl8VkqzqpV5fKiaibbRGfkY2lDR9SlibQvVm2ClHD6AIhBYQeuy32qaj/0", "language": "zh_CN", "city": "闸北", "country": "中国", "sex": 1, "privilege": [], "nickname": "碎ping子"}


print json.dumps(ss, indent=4, ensure_ascii=False)
