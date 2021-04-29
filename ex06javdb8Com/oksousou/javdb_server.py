import random
import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
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
# start_page_number = int(input('输入要抓取开始页：'))
# end_page_number = int(input('输入要抓取结束开页：'))+1
start_page_number = 1
end_page_number = 3


# 获取每一类的前六页url地址
def spyder_magnet():
    # 三大类循环
    for kind in kinds:
        kind_url = 'https://javdb8.com{}'.format(kind)
        # 页码循环
        for page_num in range(start_page_number, end_page_number):
            # print('当前是第{}页,共抓取{}页'.format(page_num,end_page_number))
            page_url = kind_url + '?page=' + str(page_num)
            response = requests.get(url=page_url, headers=header, verify=False)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            div = soup.find_all(name='div', attrs={"class": "grid columns"})[0].find_all('a')
            # 详细内容页的<a>链接的地址
            for url_a in div:
                url_a = 'https://javdb8.com' + url_a.attrs['href']
                #防止被封，设置不定时间隔
                # time.sleep(random.randint(1, 3))
                response = requests.get(url=url_a, headers=header)
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
                # 调用方法上传到wordpress
                wpsend(content,title_replace)
                # print(title_replace)


def wpsend(content,title):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://127.0.0.1/xmlrpc.php', 'bruce','12345678')
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
    spyder_magnet()
