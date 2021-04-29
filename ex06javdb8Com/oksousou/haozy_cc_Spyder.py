# import random
# import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
# from wordpress_xmlrpc.methods.users import GetUserInfo
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymongo import mongo_client
import random

# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='https://javdb8.com'
header = {
    'user - agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.193Safari / 537.36'
}
# 指定有码，无码，欧美大类
kinds = ['/', '/uncensored/', '/western/']
start_page_number = int(input('输入要抓取开始页：'))
end_page_number = int(input('输入要抓取结束开页：'))+1

# 获取每一类的前六页url地址
def page_url():
    page_url_list = []
    for kind in kinds:
        kind_url = 'https://javdb8.com{}'.format(kind)
        for page_num in range(start_page_number, end_page_number):
            page_url = kind_url + '?page=' + str(page_num)
            page_url_list.append(page_url)
    # print(page_url_list)
    return page_url_list
    # 设置抓取起止位置


# 抓取每页中详细页的<a>标签的url链接
def index_a(page_url_list):
    index_a_list = []
    try:
        for url in page_url_list:
            response = requests.get(url=url, headers=header, verify=False)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            div = soup.find_all(name='div', attrs={"class": "grid columns"})[0].find_all('a')
            # 将<a>链接的地址写入列表
            for a in div:
                index_a_list.append('https://javdb8.com' + a.attrs['href'])
        # print(index_a_list)
        return index_a_list
    except :
        print('no抓取每页中详细页的<a>标签的url链接')



# 抓取详细页
def spyder_magnet(index_a_list):
    contents_list = []
    try:
        for url_detailed in index_a_list:
            # 设置随机时间，防止被封ip
            # time.sleep(random.randint(1, 4))
            response = requests.get(url=url_detailed, headers=header)
            # 重新编码
            # response.encoding=response.apparent_encoding
            response.encoding = 'utf-8'
            # 实例化
            soup = BeautifulSoup(response.text, 'lxml')
            # 获取标题
            title = soup.find_all('title')[0].string
            title_replace = title.replace('JavDB','magnetkey.xyz')
            # print(title)
            # 获取图片src
            image = soup.find_all(name='div', attrs={"class": "column column-video-cover"})[0].find_all('a')
            # print(image)
            image_src = image[0]
            # print(image_src)
            # 获取magnet
            div_magnet = soup.find_all(name='div', attrs={'id': 'magnets-content'})[0]
            # div = soup.find_all(name='div', attrs={'id': 'magnets-content'})[0].find_all('a')
            # magnets = []
            # for magnet in div:  # 找到id="magnets-content"的div里面的所有<magnet>标签
            #     magnets.append(magnet.attrs['href'])  # 获取magnet标签的href属性，即magnet网址
            # content = '<p>'+title_replace+'\n'+str(image_src)+'\n'+'\n'.join(magnets)+'\n'+'</p>'
            # contents_list.append(content)
            # 上传信息到wordpress
            content = '<p>'+title_replace+'\n'+str(image_src)+'\n'+str(div_magnet)+'\n'+'</p>'
            wpsend(content,title_replace)
            print(title_replace)
        # return contents_list
    except :
        print('no详细页')


def wpsend(content,title):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://192.168.190.145/xmlrpc.php', 'bruce','12345678')
        # print(content)
        post = WordPressPost()
        post.title = str(title)
        post.content = " ''' " + content + " ''' "
        post.post_status = 'publish'
        post.terms_names = {
            'post_tag': ['福利'],
            'category': ['福利','magnet']
        }
        wp.call(NewPost(post))
        localtime = time.localtime(time.time())
        print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')

if __name__ == '__main__':
    # 返回单页信息
    spyder_magnet(index_a(page_url()))
