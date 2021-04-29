#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:spyder02-baiduTranslate.py
    @time:2021/04/01
"""
# 获取百度翻译数据

import requests

# url = "https://fanyi.baidu.com/sug"
url ="https://fanyi.baidu.com/v2transapi?from=en&to=zh"
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
kw = input("输入要翻译的内容")
data = {
    'query':'kw'
}
def response_baidu():
    response = requests.post(url=url,headers=header,data=data)
    print(response.json())

if __name__ == '__main__':
    response_baidu()