#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:updateWordpress.py
    @time:2021/04/13
"""
# https://blog.csdn.net/qq_37195257/article/details/103643238
# 爬虫用的 bs4+requests
# 上传用的  wordpress_xmlrpc

# coding=utf-8
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import time
import requests
from bs4 import BeautifulSoup

url = 'https://futures.hexun.com/2019-12-17/199706366.html'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.XXXX.XXX Safari/537.36'}


def getcontent():
    try:
        html = requests.get(url=url, headers=header)
        html.encoding = 'gbk'
        Soup = BeautifulSoup(html.text, "lxml")
        con = Soup.select('div.art_contextBox p')
        cont = ''
        for y in con:
            # print (type(str(y)))
            cont = cont + str(y)
        return (cont)
    except:
        pass


def wpsend(content):
    # 链接地址，登录用户名，密码
    wp = Client('http://192.168.190.145/xmlrpc.php', 'bruce','12345678')
    print(content)
    post = WordPressPost()
    post.title = '实例演示'
    post.content = " ''' " + content + " ''' "
    post.post_status = 'publish'
    post.terms_names = {
        'post_tag': ['test'],
        'category': ['Tests']
    }
    wp.call(NewPost(post))
    localtime = time.localtime(time.time())
    print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))


wpsend(getcontent())
