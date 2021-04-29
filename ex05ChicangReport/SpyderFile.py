#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:SpyderFile.py
    @time:2021/04/06
"""
# 获取交易所分析文档，
import requests
import pandas as pd
import time
import os


# 转换日期时间获取当天指定格式日期
timeArray = time.localtime(time.time())
year_time = time.strftime("%Y",timeArray)
day_time = time.strftime("%Y%m%d", timeArray)
url = " http://www.czce.com.cn/cn/DFSStaticFiles/Future/{}/{}/FutureDataHolding.xls".format(year_time,day_time)
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
def zhengzhou():
    response = requests.get(url=url,headers=header).content
    with open('./FutureDataHolding{}.xls'.format(day_time),'wb') as fp:
        fp.write(response)

    # data = pd.read_excel('./FutureDataHolding.xls',sheet_name=0,index_col=0,header=[1],usecols=[0,4,5,6,7,8,9])
    # data.to_csv('FutureDataHolding.csv',encoding='utf-8')

if __name__ == '__main__':
    zhengzhou()


