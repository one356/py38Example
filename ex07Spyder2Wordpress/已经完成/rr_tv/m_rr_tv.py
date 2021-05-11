#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:m_rr_tv.py
    @time:2021/05/11
"""
# 抓取人人视频手机端电影分发下载地址信息
# 整体思路：通过获取json数据解析详细地址和信息，解析出视频的cdn地址，统计收集
#详情页面获取剧集的ul列表最后的li标签值，并循环请求剧集，获取cdn地址收集到列表中整理
import random

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import time
import requests
import threading
import json
from bs4 import BeautifulSoup
from selenium import webdriver

'''
页面详解：
url = “https://content.json.rr.tv/morpheus/filter/all/all/all/all/all/latest/1?5-11-7”
循环遍历访问上面url会获取近18个不分类的影片的json数据，更改数字1就可以循环访问
'''
# url = "https://content.json.rr.tv/morpheus/filter/all/all/all/all/all/latest/1?5-11-7"
header = {
    "user-agent": "Mozilla/5.0(Windows NT 10.0; WOW64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/90.0.4430.72 Safari/537.36"}
# 定位浏览器驱动的指定绝对路径
chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"  # 改成你的chromedriver的完整路径地址

def spyder(url):
    response = requests.get(url=url,headers=header)
    #获取json并解析
    data_list = json.loads(response.text)['result']['content']
    # 循环遍历获取每个剧集对应的信息
    for data in data_list:
        # 图片地址
        img = '<img src="{}">'.format(data['cover'])
        # 详细访问页url
        id = data['id']
        # 剧集评分
        score = data['score']
        # 标题
        title = data['title']
        # 类型
        type = data['type']
        #获取详细页
        url_id = 'http://m.rr.tv/detail/{}?snum=1'.format(id)
        response_id = requests.get(url=url_id,headers=header)
        # 重新编码
        # response.encoding=response.apparent_encoding
        response_id.encoding = 'utf-8'
        soup = BeautifulSoup(response_id.text,'lxml')
        # 获取可播放剧集数
        id_number = soup.find_all(name='ul',attrs={"class":"episode-list"})[0].find_all('li')[-1].string
        # print(id_number)
        # 循环获取剧集cdn地址
        videojs_list=[]
        for number in range(1,int(id_number)):
            url_number = url_id.replace('snum=1','snum={}'.format(number))
            # 定义浏览器对象，调用浏览器驱动打开浏览器
            wd = webdriver.Chrome(chromedriver_path)
            # 给让浏览器对象按指定方式访问网页对象，有get；post两种方式
            wd.get(url_number)
            # 隐式等待时间，如果请求没有响应，每隔半秒检查一下，直到指定时间之内一直尝试。
            # wd.implicitly_wait(5)
            time.sleep(random.randint(3,5))
            # 获取元素
            cdn = wd.find_element_by_xpath("//*[@id='__layout']/div/main/div[2]/video").get_attribute("src")
            # print(cdn)
            videojs = f'<a href="{cdn}" target="_blank">在线播放第{number}集</a><br>'
            # print(videojs)
            videojs_list.append(videojs)
            wd.close()
        # print(videojs_list)
        # 上传信息到wordpress
        content = '<p>' +str(title)+ '\n'+ str(img) + '\n' + '评分：'+str(score) + '\n' + str(videojs_list) + '\n' + '</p>'
        # print(content)
        # 调用方法上传到wordpress
        wpsend(content, title, type)
        # print(title)

def wpsend(content, title, vido_info_kind):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://magnetkey.xyz/xmlrpc.php', 'bruce', 'flzx3qc@ysyhl9t')
        # wp = Client('http://192.168.190.145/xmlrpc.php', 'bruce', '12345678')
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
            'post_tag': ['影视'],
            'category': ['影视','迅雷下载','人人视频', vido_info_kind]
        }
        # # 新建文章
        wp.call(NewPost(post))
        localtime = time.localtime(time.time())
        print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')


if __name__ == '__main__':
    for i in range(1, 0, -1):
        url = "https://content.json.rr.tv/morpheus/filter/all/all/all/all/all/latest/{}?5-11-7".format(i)
        spyder(url)
