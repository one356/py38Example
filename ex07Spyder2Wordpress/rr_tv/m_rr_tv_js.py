#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:m_rr_tv_js.py.py
    @time:2021/05/13
"""
import requests
# 注释
url = 'https://web-api.rr.tv/watch/morpheus/v1/cdn/parser?5-13-18'
def spyder():
    response = requests.post(url=url)
    print(response.text)

if __name__ == '__main__':
    spyder()