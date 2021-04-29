#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:spyder02-baiduTranslate.py
    @time:2021/04/01
"""
# 获取百度翻译数据

import requests
import json

# url = "https://fanyi.baidu.com/sug"
url = "https://movie.douban.com/j/chart/top_list"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
params = {
    'type': '24',
    'interval_id': '100:90',
    'action': '',
    'start': '0',
    'limit': '40',
}


def response_baidu():
    response = requests.get(url=url, headers=header, params=params)
    movie_list = response.json()
    fp = open('./douban.json',mode='w',encoding='utf-8')
    json.dump(movie_list,fp=fp,ensure_ascii=False)


if __name__ == '__main__':
    response_baidu()
