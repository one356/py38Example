#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    @author:Administrator
    @file:ex01threading.py
    @time:2021/04/21
"""
# 多线程，多进程，多协程练习
import threading
import random
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning



# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='http://www.88zyw.xyz/'
header = {
    'user - agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.193Safari / 537.36'
}
start_page_number = int(input('输入要抓取开始页：'))
end_page_number = int(input('输入要抓取结束开页：'))+1
url_list = [f'https://yj1.pc20x12.com/pw/thread.php?fid=3&page={page_num}' for page_num in range(start_page_number, end_page_number,-1)]
# 获取指定格式当前时间
localtime = time.localtime(time.time())
daytime = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
# 获取每一类的前2页url地址
def spyder_magnet(page_url):
    # 页码循环
    print('当前采集的页面是----------------》》》》》',page_url)
    response = requests.get(url=page_url, headers=header, verify=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    div = soup.find_all(name='tbody', attrs={"style": "table-layout:fixed;"})[0].find_all('tr')[7:-1]
    # 详细内容页的<a>链接的地址
    for i in range(len(div)):
        print(page_url)
        print(i)
        url_a = 'https://yj1.pc20x12.com/pw/' + div[i].find('a').attrs['href']
        try:
            #防止被封，设置不定时间隔
            time.sleep(random.randint(10, 15))
            response = requests.get(url=url_a, headers=header)
            # 重新编码
            response.encoding = 'utf-8'
            # 实例化
            soup = BeautifulSoup(response.text, 'lxml')
            # 获取标题
            title = soup.find_all('title')[0].string
            title_replace = title.replace('BT伙计', 'magnetkey.xyz')
            # 获取合集正文中a链接地址
            a_list = soup.find_all(name='div', attrs={"class": "tpc_content"})[0].find_all('a')
            magnetkeys = []
            for a in a_list:
                magnetkeys.append(a.text.split('/')[-1] + '\n')
            magnetkey_upcode ='magnet:?xt=urn:btih:'.join(magnetkeys)
            # 上传信息到wordpress
            content = '<p>'+title_replace+'\n'+magnetkey_upcode+'\n'+'</p>'
            # 调用方法上传到wordpress
            wpsend(content,title_replace)
            print(title_replace)
        except:
            print('未找到指定的页面-----',url_a)



def wpsend(content,title):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://magnetkey.xyz/xmlrpc.php',  'bruce','flzx3qc@ysyhl9t')
        # print(content)
        post = WordPressPost()
        post.title = str(title)
        post.content = " ''' " + content + " ''' "
        post.post_status = 'publish'
        post.terms_names = {
            'post_tag': ['magnet'],
            'category': ['福利','magnet']
        }
        wp.call(NewPost(post))
        print('文档已上传 {}'.format(daytime))
    except:
        print('没有上传成功')

def multi_thread():
    print('multi_thread begin')
    threads_list = []
    for url in url_list:
        threads_list.append(
            threading.Thread(target=spyder_magnet,args=(url,))
        )
    for thread in threads_list:
        # 设置上传速度，否则会无法上传
        time.sleep(random.randint(70, 140))
        thread.start()
    for thread in threads_list:
        thread.join()


if __name__ == '__main__':
    # 返回单页信息
    # spyder_magnet()
    multi_thread()

