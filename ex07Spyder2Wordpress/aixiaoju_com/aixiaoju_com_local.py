#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:praictis.py
    @time:2021/04/28
"""
"""
练习使用selenium
爬取指定网站的信息https://www.aixiaoju.com

"""


from selenium import webdriver
from selenium.webdriver import Chrome
import random

# 定位浏览器驱动的指定绝对路径
chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"  # 改成你的chromedriver的完整路径地址
# 要打开的网站的种类首页列表
kinds = ["https://www.aixiaoju.com/thread-1-1","https://www.aixiaoju.com/thread-18-1","https://www.aixiaoju.com/thread-28-1","https://www.aixiaoju.com/tag-index-view?page=1&id=33"]
# 定义selenium爬虫
def spyder_selenium_page_url():
    wd = webdriver.Chrome(chromedriver_path)
    wd.implicitly_wait(random.randint(5,10))
    page_url = []
    for kind_url in kinds:
        wd.get(kind_url)
        element_index_page = wd.find_element_by_xpath('//*[@class="tmode_imgGroup tmode_tagFront mod_box"]')
        element_index_page_a = element_index_page.find_elements_by_tag_name('a')
        for page_href in element_index_page_a:
            page_url.append(page_href.get_attribute('href'))
    return page_url
def spyder_selenium_page_detial(page_url_list):
    for page_url in page_url_list:


if __name__ == '__main__':
    page_url_list = spyder_selenium_page_url()
    # # 定义浏览器对象，调用浏览器驱动打开浏览器
    # wd = webdriver.Chrome(chromedriver_path)
    # # 隐式等待时间，如果请求没有响应，每隔半秒检查一下，直到指定时间之内一直尝试。
    # wd.implicitly_wait(random.randint(5,10))
    # # 给让浏览器对象按指定方式访问网页对象，有get；post两种方式
    # wd.get(url)

    # # 通过id的方式获取指定元素对象
    # element = wd.find_element_by_id('kw')

    # # 向元素对象传递指定值
    # element.send_keys('磁力链接\n')

    # 通过class属性返回多个element元素对象
    # elements = wd.find_elements_by_class_name('title-content-title')
    # for element in elements:
    #     print(element.text)

    # 通过tag标签返回element元素对象
    # elements = wd.find_element_by_tag_name("span")
    # for element in elements:
    #     print(element.text)

    # 通过限制范围查找element元素对象
    # element = wd.find_element_by_id('kw')
    # span = element.find_element_by_tag_name('span')
    # print(span.text)

