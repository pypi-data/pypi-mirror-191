#!/usr/bin/env python3
# coding=utf-8
"""
the url structure of website
"""

from handlers.index import IndexHandler    #假设已经有了

url = [
    (r'/', IndexHandler),
]