#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:praictis.py
    @time:2021/04/28
"""
"""
练习使用selenium


"""
import  selenium
from selenium import webdriver
from selenium.webdriver import Chrome
# 定位浏览器驱动的指定绝对路径
chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"  # 改成你的chromedriver的完整路径地址
# 要打开的网站的url
# url = "https://cn.torrentkitty.app"
url = "https://www.baidu.com"



if __name__ == '__main__':
    # 定义浏览器对象，调用浏览器驱动打开浏览器
    wd = webdriver.Chrome(chromedriver_path)
    # 隐式等待时间，如果请求没有响应，每隔半秒检查一下，直到指定时间之内一直尝试。
    wd.implicitly_wait(10)
    # 给让浏览器对象按指定方式访问网页对象，有get；post两种方式
    wd.get(url)

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
    element = wd.find_element_by_id('kw')
    span = element.find_element_by_tag_name('span')
    print(span.text)





'''
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.get(url)
    '''
