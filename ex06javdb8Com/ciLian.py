#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:ciLian.py
    @time:2021/04/07
"""
# 注释
'''
magnet：此链接采用的协议名称；xt：Exact Topic的缩写，包含文件Hash值的统一资源名称；
btih：BitTorrent Info Hash的缩写，这里表示采用了Hash方法名，这里还可以使用ED2K，AICH，SHA1和MD5等。
这个值是文件的唯一标识符，是不可缺少的。
上面列举的这三项是一条Magnet URL中，必不可少的组成部分。
此外，在一些Magnet URL中还会出现dn、tr、ws等等缩写，它们均为选填字段，这里就不多做介绍。
磁力链实例：
magnet:?xt=urn:btih:808430ac61e9fb87b5dff6641adcb711ec9a50aa&dn=[javdb.com]LZDM-038.mp4
magnet:?xt=urn:btih:2095cb2b491220eb7fc22e31e6f2f7423cf85f54&dn=[javdb.com]lzdm00038
magnet:?xt=urn:btih:2b5d6d760a2b52924edf9bd7025e6e0688600cf4&dn=[javdb.com]LZDM-038.HD
'''

import random
import string
import pymongo
from urllib import request
from hashlib import sha1

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['ciliandb']
mycol = mydb['key']

def keyWord():
    # 指定随机数长度
    r_num = 40
    # 生成数字 + 字母（字符串序列）
    token = string.digits + string.ascii_lowercase + string.digits
    # 随机选择 指定长度 随机码（字符串列表）
    token = random.sample(token,r_num)
    # 生成 数字 + 字母 随机数
    token = "".join(token)
    # 加强版（一行代码）
    # token = ''.join(random.sample(string.digits + string.ascii_letters,r_num))
    return token

if __name__ == '__main__':
    a = keyWord()
    # for i in range(1,10000000000000):
    #     a = keyWord()
    #     print(i)
    #     mydict = {"key": i}
    #     # open('key.txt','a+').write("{}\n".format(a))
    #     x = mycol.insert_one(mydict)

    # 对a切片
    print(a[:20])
    print(a[20:])