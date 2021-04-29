# import random
# import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
# from wordpress_xmlrpc.methods.users import GetUserInfo
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='https://javdb8.com'
header = {
    'user - agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.193Safari / 537.36'
}
# 指定有码，无码，欧美大类
kinds = ['/', '/uncensored/', '/western/']
page_number = int(input('输入要抓取多少页：'))+1

# 获取每一类的前六页url地址
def url():
    page_url_list = []
    for kind in kinds:
        kind_url = 'https://javdb8.com{}'.format(kind)
        for page_num in range(1, page_number):
            page_url = kind_url + '?page=' + str(page_num)
            page_url_list.append(page_url)
    # print(page_url_list)
    return page_url_list
    # 设置抓取起止位置


# 抓取每页中详细页的<a>标签的url链接
def spyder_index_a(page_url_list):
    a_list = []
    try:
        for url in page_url_list:
            response = requests.get(url=url, headers=header, verify=False)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            div = soup.find_all(name='div', attrs={"class": "grid columns"})[0].find_all('a')
            # 将<a>链接的地址写入列表
            for a in div:
                a_list.append('https://javdb8.com' + a.attrs['href'])
        # print(a_list)
        return a_list
    except :
        print('no抓取每页中详细页的<a>标签的url链接')



# 抓取详细页
def spyder_magnet(a_list):
    contents_list = []
    # try:
    for url_detailed in a_list:
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
        image = soup.find_all(name='div', attrs={"class": "message-body"})[0].find_all('img')
        # print(image)
        image_src = image[0].attrs['src']
        # print(image_src)
        # 获取magnet
        # div = soup.find_all(name='div', attrs={'id': 'magnets-content'})[0]

        div = soup.find_all(name='div', attrs={'id': 'magnets-content'})[0].find_all('a')

        magnets = []
        for magnet in div:  # 找到id="magnets-content"的div里面的所有<magnet>标签
            magnets.append(magnet.attrs['href'])  # 获取magnet标签的href属性，即magnet网址
            # print(magnet.attrs['href'])
        # print(title,image_src,magnets)

        content = title_replace+'\n'+image_src+'\n'+'\n'.join(magnets)
        contents_list.append(content)
        print(title_replace)
        # content = title + '\n' + image_src + '\n' + div
    return contents_list
    # except :
    #     print('no详细页')


def wpsend(content):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://192.168.190.145/xmlrpc.php', 'bruce','12345678')
        print(content)
        post = WordPressPost()
        post.title = '实例演示'
        post.content = " ''' " + content + " ''' "
        post.post_status = 'publish'
        post.terms_names = {
            'post_tag': ['test'],
            'category': ['Tests']
        }
        wp.call(NewPost(post))
        localtime = time.localtime(time.time())
        print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')

if __name__ == '__main__':
    # 返回单页信息
    content_list = spyder_magnet(spyder_index_a(url()))
    print(content_list)
    for i in content_list:
        wpsend(i)