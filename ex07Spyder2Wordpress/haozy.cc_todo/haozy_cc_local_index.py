import random
import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPost, NewPost,DeletePost
from wordpress_xmlrpc.methods.users import GetUserInfo
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning



# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='http://www.haozy.cc/'
header = {
    'user - agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.193Safari / 537.36'
}
# 指定大类
start_page_number = int(input('输入要抓取开始页：'))
end_page_number = int(input('输入要抓取结束开页：'))+1

# 获取每一类的前n页url地址
def spyder_magnet():
    # 页码循环
    for page_num in range(start_page_number, end_page_number):
            print('当前是第{}页,共抓取{}页'.format(page_num,end_page_number))
            # 单页面的url地址获取
            page_url='http://www.haozy.cc/?m=vod-index-pg-{}.html'.format(page_num)
            # page_url_str = '-pg-' + str(page_num) + '.html'
            # print(page_url_str)
            # page_url = kind_url.replace('.html',page_url_str)
            print(page_url)
            response = requests.get(url=page_url, headers=header, verify=False)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            div = soup.find_all(name='div', attrs={"class": "xing_vb"})[0].find_all('ul')[1:-1]
            # 详细内容页的<a>链接的地址
            for i in range(0,len(div)):
                url_a = 'http://wwwhaozy.cc' + div[i].find('a').attrs['href']
                print(url_a)
                #防止被封，设置不定时间隔
                # time.sleep(random.randint(1, 4))
                response = requests.get(url=url_a, headers=header)
                # 重新编码
                # response.encoding=response.apparent_encoding
                response.encoding = 'utf-8'
                # 实例化
                soup = BeautifulSoup(response.text, 'lxml')
                # 获取标题
                title = soup.find_all('title')[0].string
                title_replace = title.replace('OK资源采集','magnetkey.xyz')
                # print(title)
                # 获取图片src
                image_src = soup.find_all(name='div', attrs={"class": "vodImg"})[0].find_all('img')[0]
                # print(image_src)
                # 获取影片信息
                vido_info = soup.find_all(name='div', attrs={'class': 'vodInfo'})[0]
                # 获取影片类型
                vido_info_kind = soup.find_all(name='div', attrs={'class': 'vodinfobox'})[0].find_all('li')[3].text
                # 获取影片介绍
                vido_play_info = soup.find_all(name='div', attrs={'class': 'vodplayinfo'})[0]
                # 获取链接地址
                div_magnet = soup.find_all(name='div', attrs={'class': 'ibox playBox'})[1]
                # print(div_magnet)
                # 上传信息到wordpress
                content = '<p>'+title_replace+'\n'+str(image_src)+'\n'+str(vido_info)+'\n'+str(vido_play_info)+'\n'+str(div_magnet)+'\n'+'</p>'
                # print(content)
                # 调用方法上传到wordpress
                wpsend(content,title_replace,vido_info_kind)
                # print(title_replace)


def wpsend(content,title,vido_info_kind):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://192.168.190.145/xmlrpc.php', 'bruce','12345678')
        # print(content)
        post = WordPressPost()
        # 设置标题内容
        post.title = str(title)
        # 文章正文内容
        post.content = " ''' " + content + " ''' "
        # 可见性，publish：全部可见；
        post.post_status = 'publish'
        # 设置标签，分类
        post.terms_names = {
            'post_tag': ['影视'],
            'category': ['影视','链接资源',vido_info_kind]
        }
        # 验证是否有相同标题
        old_post = wp.call(GetPost(post.title))
        # old_post = GetPost(post.title)
        print(old_post)
        if post.title== old_post:
            wp.call(DeletePost(post.title))
            print('已经删除{}'.format(post.title))
        else:
            # 新建文章
            wp.call(NewPost(post))
            localtime = time.localtime(time.time())
            print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')

if __name__ == '__main__':
    # 返回单页信息
    spyder_magnet()
