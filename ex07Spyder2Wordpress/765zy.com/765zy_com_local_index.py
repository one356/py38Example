import random
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading

# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='http://www.765zy.com/'
header = {
    'user-agent':'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.193Safari/537.36'
}
# 指定大类
start_page_number = int(input('输入要抓取开始页：'))
end_page_number = int(input('输入要抓取结束开页：'))
url_list = [f'http://www.765zy.com/?m=vod-index-pg-{page_num}.html' for page_num in
            range(start_page_number, end_page_number)]


# 获取每一类的前n页url地址
def spyder_magnet(page_url):
    # 页码循环
    print('当前采集的页面是----------------》》》》》', page_url)
    response = requests.get(url=page_url, headers=header, verify=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    div = soup.find_all(name='div', attrs={"class": "xing_vb"})[0].find_all('ul')[1:-1]
    # 详细内容页的<a>链接的地址
    for i in range(0, len(div)):
        url_a = 'http://www.765zy.com' + div[i].find('a').attrs['href']
        print(page_url)
        print(i)
        # 防止被封，设置不定时间隔
        time.sleep(random.randint(1, 10))
        response = requests.get(url=url_a, headers=header)
        # 重新编码
        # response.encoding=response.apparent_encoding
        response.encoding = 'utf-8'
        # 实例化
        soup = BeautifulSoup(response.text, 'lxml')
        # 获取标题
        title = soup.find_all('title')[0].string
        title_replace = title.replace('605资源网', 'magnetkey.xyz')
        # print(title)
        # 获取图片src
        image_src = str(soup.find_all(name='div', attrs={"class": "vodImg"})[0].find_all('img')[0])
        # print(image_src)
        image_src_replace = image_src.replace('/.', 'http://www.765zy.com')
        # print(image_src_replace)
        # 获取影片信息
        vido_info = soup.find_all(name='div', attrs={'class': 'vodInfo'})[0]
        # 获取影片类型
        vido_info_kind = soup.find_all(name='div', attrs={'class': 'vodinfobox'})[0].find_all('li')[4].text
        # 获取影片介绍
        vido_play_info = soup.find_all(name='div', attrs={'class': 'vodplayinfo'})[0]
        # 获取链接地址
        div_magnet = soup.find_all(name='div', attrs={'class': 'ibox playBox'})[1]
        # print(div_magnet)
        # 上传信息到wordpress
        content = '<p>' + str(image_src_replace) + '\n' + str(vido_info) + '\n' + str(
            vido_play_info) + '\n' + str(div_magnet) + '\n' + '</p>'
        # print(content)
        # 调用方法上传到wordpress
        wpsend(content, title_replace, vido_info_kind)
        # print(title_replace)


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
            'post_tag': ['影视'],
            'category': ['影视', '链接资源', vido_info_kind]
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
        time.sleep(random.randint(60, 140))
        thread.start()
    for thread in threads_list:
        thread.join()


if __name__ == '__main__':
    # 多线程启动
    # multi_thread()

    # 单线程采集
    for url in url_list:
        try:
            spyder_magnet(url)
        except:
            print('没有采集到的页面链接：',url)
