#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:hupu_com_local.py
    @time:2021/05/09
"""
# 抓取虎扑网新闻
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import time
import requests
import threading
import json

# url_list = []
# for i in range(1, 10):
#     url_hupu = "https://www.hupu.com/home/v1/news?pageNo={}&pageSize=20".format(i)
    # url_list.append(url_hupu)
url_hupu = "https://www.hupu.com/home/v1/news?pageNo=1&pageSize=50"
header = {
    "user-agent": "Mozilla/5.0(Windows NT 10.0; WOW64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/90.0.4430.72 Safari/537.36"}


def spyder_news(url):
    response = requests.get(url=url, headers=header)
    data_list = json.loads(response.text)['data']
    content_list = []
    for data in data_list:
        # 标题
        title = data['title']
        # print( title)
        # 文章内容
        content = data['content']
        # print(content)
        # 详细页链接
        tid = data['tid']
        tid_url = "https://bbs.hupu.com/{}.html".format(tid)
        tid_a = "<a href = '{}'".format(tid_url) + ">虎扑引用链接</a>"
        # print(tid_url)
        # 上传信息到wordpress
        content = '<p>' + str(title) + str(content) + str(tid_a) + '</p>'
        print(content)
        content_list.append(content)
        # 调用方法上传到wordpress
    title = '虎扑信息合集{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    wpsend(str(content_list).replace('\n', ''), title)


def wpsend(content, title):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://magnetkey.xyz/xmlrpc.php', 'bruce', 'flzx3qc@ysyhl9t')
        post = WordPressPost()
        # 设置标题内容
        post.title = str(title)
        # 文章正文内容
        post.content = " ''' " + content + " ''' "
        # 可见性，publish：全部可见；'private':私有
        post.post_status = 'publish'
        # 设置标签，分类
        post.terms_names = {
            'post_tag': ['短资讯'],
            'category': ['短资讯', '虎扑']
        }
        # # 新建文章
        wp.call(NewPost(post))
        localtime = time.localtime(time.time())
        print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')


# def mut_thread():
#     threadings = []
#     for url in url_list:
#         threadings.append(threading.Thread(target=spyder_news, args=(url,)))
#     time.sleep(30)
#     for thread in threadings:
#         thread.start()
#     for thread in threadings:
#         thread.join()


if __name__ == '__main__':
    # mut_thread()
    spyder_news(url_hupu)
