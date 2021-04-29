#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:torrentkitty_app_local.py
    @time:2021/04/27
"""
# 注释
# url =
# 抓取规则如下
import threading
import random
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime
import cfscrape
# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Spyder():
    # 获取页面url列表
    def page_magnet(day):
        header = {
            'user-agent':'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.193Safari/537.36'}
        url= "https://cn.torrentkitty.app/archive/" + str(day) + '/1'
        # page_response = requests.get(url=url,headers =header)
        print('url====================',url)
        time.sleep(random.randint(6, 10))

        # 实例化一个create_scraper对象
        scraper = cfscrape.create_scraper()
        # 请求报错，可以加上时延
        # scraper = cfscrape.create_scraper(delay = 10)
        # 获取网页源代码
        web_data = scraper.get("https://www.torrentkitty.io/archive/2021-04-26/1").text
        print(web_data)
        soup = BeautifulSoup(web_data, 'lxml')
        # page_response = requests.get(url="https://cn.torrentkitty.app/archive/" + str(day) + '/1', headers=header)
        # page_response.encoding='utf-8'

        # soup = BeautifulSoup(page_response.text,'lxml')
        try:
            magnet_a = soup.find_all(name='table',attrs={"id":"archiveResult"})[0]
            print(magnet_a)
        except:
            print('没有获取首页')
    # 获取日期列表
    def daytime(self):
        # date_input1 = input("请输入日期(格式YYYY-MM-DD)：")
        # date_input2 = input("请输入日期(格式YYYY-MM-DD)：")
        date_input1 = str('2015-01-01')
        date_input2 = str('2021-04-26')
        timelist1 = date_input1.split("-")
        timelist1 = [int(x) for x in timelist1]
        year1 = timelist1[0]
        month1 = timelist1[1]
        day1 = timelist1[2]
        begin = datetime.date(year1, month1, day1)
        timelist2 = date_input2.split("-")
        timelist2 = [int(x) for x in timelist2]
        year2 = timelist2[0]
        month2 = timelist2[1]
        day2 = timelist2[2]
        end = datetime.date(year2, month2, day2)
        day_list = []
        for i in range((end - begin).days + 1):
            day = begin + datetime.timedelta(days=i)
            day_list.append(str(day))
        return day_list

    # print('当前年月日:', datetime.date.today())
def thread():
    spyder = Spyder()
    threads = []
    for day in spyder.daytime():
        threads.append(
            threading.Thread(target=spyder.page_magnet(),args=(day,))
        )
    for thread in threads:
        time.sleep(random.randint(35, 140))
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    thread()

