from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading
import random
# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='https://www.177521.com/nvshen/index_2.html'
header = {
    'user-agent': 'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.193Safari/537.36'
}
start_page_number = int(input('输入要抓取开始页：'))
end_page_number = int(input('输入要抓取结束开页：'))+1
kinds = ['oumei','nvshen','meinv','cosplay']
url_list = []
for kind in kinds:
    kind_url = "https://www.177521.com/"+str(kind)
    for page_num in range(start_page_number, end_page_number):
        url_list.append(kind_url + "/index_{}.html".format(page_num))
print(url_list)
# 页面应该有400页以上，从第二页开始抓取
# 获取每一类的前n页url地址
def spyder_magnet(page_url):
    # 页码循环
    try:
        print('当前采集的页面是----------------》》》》》', page_url)
        response = requests.get(url=page_url, headers=header, verify=False)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find_all(name='ul', attrs={'class': "update_area_lists cl"})[0].find_all('li')
        # 详细内容页的<a>链接的地址
        for i in range(len(div)):
            url_a = 'https://www.177521.com' + div[i].find('a').attrs['href']
            print(page_url)
            print(i)
            # 防止被封，设置不定时间隔
            # time.sleep(random.randint(1, 4))
            response = requests.get(url=url_a, headers=header)
            # 重新编码
            # response.encoding=response.apparent_encoding
            response.encoding = 'utf-8'
            # 实例化
            soup = BeautifulSoup(response.text, 'lxml')
            # 获取标题
            title = soup.find_all('title')[0].string
            title_replace = title.replace('177521女神资料网', 'magnetkey.xyz磁力链接分享')
            # 获取wordpress类型
            vido_info_kind = soup.find_all(name='div', attrs={'class': "post_au"})[0].find('a').text
            # print(vido_info_kind)
            # 女神介绍
            nvshen_info_list = soup.find_all(name='div', attrs={'class': 'content_left'})[0].find_all('p')
            nvshen_info = '\n'.join('%s' % i for i in nvshen_info_list)
            # print(nvshen_info)
            # 上传信息到wordpress
            content = '<p>' + title_replace + '+\n' + str(nvshen_info) + '\n' + '</p>'
            # print(content)
            # 调用方法上传到wordpress
            wpsend(content, title_replace, vido_info_kind)
    except:
        print('不存在的页面----------------》》》》》', page_url)


def wpsend(content, title, vido_info_kind):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://magnetkey.xyz/xmlrpc.php', 'bruce', 'flzx3qc@ysyhl9t')
        # print(content)
        post = WordPressPost()
        # 设置标题内容
        post.title = str(title)
        # 文章正文内容
        post.content = " ''' " + content + " ''' "
        # 可见性，publish：全部可见；'private':私有
        post.post_status = 'publish'
        # 设置标签，分类
        post.terms_names = {
            'post_tag': ['女神'],
            'category': ['图片', '演员', vido_info_kind]
        }
        # # 新建文章
        wp.call(NewPost(post))
        localtime = time.localtime(time.time())
        print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')

def multi_thread():
    print('multi_thread begin')
    threads_list = []
    for url in url_list:
        threads_list.append(
            threading.Thread(target=spyder_magnet, args=(url,))
        )
    for thread in threads_list:
        # 设置上传速度，否则会无法上传
        time.sleep(random.randint(20, 50))
        thread.start()
    for thread in threads_list:
        thread.join()


if __name__ == '__main__':
    # 返回单页信息
    multi_thread()
