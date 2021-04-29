#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:spyder04-qiuImage.py
    @time:2021/04/01
"""
# 爬取图片
# 使用正则表达式获取内容
import requests
import re
import os

url = "https://www.qiushibaike.com/imgrank/page/%d"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

def qiu_image():
    for url_number in range(1,pag_num):
        new_url = format(url%url_number)
        response = requests.get(url=new_url,headers=header).text
        # 正则表达式中()括号中的内容是提取出来的，用.*?表示任意的字符
        ex = '<div class="thumb">.*?<img src="(.*?)" alt.*?</div>'
        # 取得正则表达式中匹配规则的列表，re.S表示单行匹配
        image_src_list = re.findall(ex,response,re.S)
        if not os.path.exists('./qiutu'):
            os.mkdir('./qiutu')
        for image_src in image_src_list:
            impage_url = 'https:'+image_src
            impage_response = requests.get(url=impage_url,headers=header).content
            image_name = image_src.split('/')[-1]
            save_path = './qiutu/'+image_name
            with open(save_path,'wb') as fp:
                fp.write(impage_response)
            print(image_name)
if __name__ == '__main__':
    pag_num = int(input('要爬取多少页：'))
    qiu_image()