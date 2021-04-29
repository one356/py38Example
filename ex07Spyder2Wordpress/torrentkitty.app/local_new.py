#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:local.py
    @time:2021/04/27
"""
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from time import sleep
import random
import datetime


# 定义一个taobao类
class taobao_infos:

    # 对象初始化
    def __init__(self):
        # day = datetime.date.today()
        # url= "https://cn.torrentkitty.app/archive/" + str(day) + '/1'
        url = "https://cn.torrentkitty.app"
        self.url = url

        options = webdriver.ChromeOptions()
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    # 登录淘宝
    def login(self):
        # 打开网页
        self.browser.implicitly_wait(30)  # 智能等待，直到网页加载完毕，最长等待时间为30s
        self.browser.get(self.url)
        text = self.browser.page_source(self.url)
        print(text)
        self.browser.find_element_by_xpath()
        # 自适应等待，点击密码登录选项
        # self.browser.implicitly_wait(30)  # 智能等待，直到网页加载完毕，最长等待时间为30s
        # day = datetime.date.today()
        # page_url = "https://cn.torrentkitty.app/archive/" + str(day) + '/1'
        # self.browser.get(page_url)


    # 模拟向下滑动浏览
    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            # 根据i的值，模拟上下滑动
            if (i % 2 == 0):
                js = "var q=document.documentElement.scrollTop=" + str(300 + 400 * i)
            else:
                js = "var q=document.documentElement.scrollTop=" + str(200 * i)
            self.browser.execute_script(js)
            sleep(0.1)

        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.1)

    # 爬取淘宝 我已买到的宝贝商品数据
    def crawl_good_buy_data(self):
        # 对我已买到的宝贝商品数据进行爬虫
        day = datetime.date.today()
        url= "https://cn.torrentkitty.app/archive/" + str(day) + '/1'
        self.browser.get(url)
        self.browser.implicitly_wait(30)  # 智能等待，直到网页加载完毕，最长等待时间为30s
        # 遍历所有页数
        # 获取本页面源代码
        html = self.browser.page_source
        # pq模块解析网页源代码
        doc = pq(html)
        # # 存储该页已经买到的宝贝数据
        good_items = doc('#tp-bought-root .js-order-container').items()
        # 遍历该页的所有宝贝
        for item in good_items:
            good_time_and_id = item.find('.bought-wrapper-mod__head-info-cell___29cDO').text().replace('\n',"").replace('\r', "")
            good_merchant = item.find('.seller-mod__container___1w0Cx').text().replace('\n', "").replace('\r', "")
            good_name = item.find('.sol-mod__no-br___1PwLO').text().replace('\n', "").replace('\r', "")
            # 只列出商品购买时间、订单号、商家名称、商品名称
            # 其余的请自己实践获取
            print(good_time_and_id, good_merchant, good_name)
        print('\n\n')

        # 大部分人被检测为机器人就是因为进一步模拟人工操作
        # 模拟人工向下浏览商品，即进行模拟下滑操作，防止被识别出是机器人
        # 随机滑动延时时间
        swipe_time = random.randint(1, 3)
        self.swipe_down(swipe_time)
        # 等待下一页按钮 出现
        good_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pagination-next')))
        # 点击下一页按钮
        good_total.click()
        sleep(2)
if __name__ == "__main__":
    chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"  # 改成你的chromedriver的完整路径地址
    a = taobao_infos()
    a.login()  # 登录
    # a.crawl_good_buy_data()  # 爬取淘宝 我已买到的宝贝商品数据



