#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:ygdy8_net_local_index.py
    @time:2021/04/18
"""
import random
import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='https://www.ygdy8.net/html/gndy/dyzz/index.html'
header = {
    'user-agent': 'Mozilla/5.0(Windows NT 10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.193Safari/537.36'
}


# 获取每一类的前n页url地址
def spyder_magnet():
    # 只抓取首页中更新的电影
    try:
        # 首页的url
        main_url = 'https://dydytt.net/index.htm'
        response = requests.get(url=main_url, headers=header, verify=False)
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find_all('a')
        # 详细内容页的<a>链接的地址
        for i in range(len(div)):
            url_a = 'https://dydytt.net' + div[i]['href']
            # 防止被封，设置不定时间隔
            # time.sleep(random.randint(1, 4))
            try:
                response = requests.get(url=url_a, headers=header)
                # 重新编码
                # response.encoding=response.apparent_encoding
                response.encoding = 'gbk'
                # 实例化
                soup = BeautifulSoup(response.text, 'lxml')
                # 获取标题
                title = soup.find_all('title')[0].string
                title_replace = title.replace('电影天堂', 'magnetkey.xyz')
                print(title_replace)
                # 获取影片信息
                div_info = soup.find_all(name='div', attrs={'id': 'Zoom'})[0]
                # 获取链接地址
                div_magnet = soup.find_all(name='div', attrs={'id': 'Zoom'})[0].find('a',href = True).attrs['href']
                div_magnet_a = '<a href="'+div_magnet+'">下载点击此磁力链接</a>'
                # 上传信息到wordpress
                content = '<p>' + title_replace + '\n' + str(div_info) + '\n' + str(div_magnet_a) + '\n' + '</p>'
                print('上传信息',content)
                # 调用方法上传到wordpress
                wpsend(content,title_replace)
                # print(title_replace)
            except:
                print('没有找到详细页：{}'.format(url_a))
    except:
        print('没有访问到：{}'.format(main_url))


def wpsend(content, title):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://wh-nb6ulvw9jakg3k41rni.my3w.com/xmlrpc.php', 'bruce', 'flzx3qc@ysyhl9t')
        # print(content)
        post = WordPressPost()
        # 设置标题内容
        post.title = str(title)
        # 文章正文内容
        post.content = " ''' " + content + " ''' "
        # 可见性，publish：全部可见；'private':私有
        post.post_status = 'publish'
        # 设置标签，分类
        post.terms_names = {
            'post_tag': ['影视', '迅雷下载'],
            'category': ['影视', '链接资源', '迅雷下载']
        }
        # # 新建文章
        wp.call(NewPost(post))
        localtime = time.localtime(time.time())
        print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')


if __name__ == '__main__':
    # 返回单页信息
    spyder_magnet()
