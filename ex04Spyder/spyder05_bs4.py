#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:spyder05_bs4.py
    @time:2021/04/02
"""
# 使用bs4标签定位
# 只有在python中有此方式
import requests
from bs4 import BeautifulSoup

url = "https://www.qiushibaike.com/imgrank/"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}


def qiutu():
    response = requests.get(url=url,headers=header).text
    soup = BeautifulSoup(response,'lxml')
    # soup = BeautifulSoup(response,'html.parser')

    # 如果html不全，自动补全代码
    # print(soup.prettify())
    print(soup.title.string)
    print(soup.p)

if __name__ == '__main__':
    qiutu()

