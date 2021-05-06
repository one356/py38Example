'''
三大种类共最多20页每个种类中的分类不一定。


'''




import random
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import  NewPost
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading



# 避免警告信息
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# url ='https://javdb8.com'
header = {
    'user - agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.193Safari / 537.36'
}
# 指定有码，无码，欧美大类
kinds = ['https://javdb8.com/series/', 'https://javdb8.com/series/uncensored/', 'https://javdb8.com/series/western/']
# 最大20页
start_page_number = int(input('输入要抓取开始页：'))
end_page_number = int(input('输入要抓取结束开页：'))+1
url_list = []
for kind in kinds:
    for page_num in range(start_page_number, end_page_number):
        url_list.append(kind + f'?page={page_num}')
series_url_list = []
def series_url(url_list):
    for page_url in url_list:
        print('当前采集的页面是----------------》》》》》', page_url)
        response = requests.get(url=page_url, headers=header, verify=False)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        series_div_list = soup.find_all(name='div', attrs={"id": "series"})[0].find_all('a')
        for series_div in series_div_list:
            for series_page in range(1, 20):
                series_div_url = 'https://javdb8.com' + series_div.attrs['href'] + f'?page={series_page}'
                series_url_list.append(series_div_url)
                # print('series_div_url:', series_div_url)
    return series_url_list
# 获取每一类的前六页url地址
def spyder_magnet(page_url):
    try:
        response = requests.get(url=page_url, headers=header, verify=False)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find_all(name='div', attrs={"class": "grid columns"})[0].find_all('a')
        vido_info = soup.find_all('title')[0].string
        vido_info_kind = vido_info.replace(' | JavDB 成人影片資料庫及磁鏈分享 ','')
    # 详细内容页的<a>链接的地址
        for url in div:
            url_a = 'https://javdb8.com' + url.attrs['href']
            print('分类',vido_info_kind)
            print('详细页链接地址',url_a)
            #防止被封，设置不定时间隔
            time.sleep(random.randint(5, 10))
            response = requests.get(url=url_a, headers=header)
            # 重新编码
            # response.encoding=response.apparent_encoding
            response.encoding = 'utf-8'
            # 实例化
            soup = BeautifulSoup(response.text, 'lxml')
            # 获取标题
            title = soup.find_all('title')[0].string
            title_replace = title.replace('JavDB','magnetkey.xyz')
            # 获取图片src
            image = soup.find_all(name='div', attrs={"class": "column column-video-cover"})[0].find_all('img')[0]
            image_src = '<a href="'+image.attrs['src']+'" target="_blank">点击预览图片</a>'
            # 获取magnet
            video_info_list = soup.find_all(name='nav',attrs={'class':"panel video-panel-info"})[0].find_all('div')[0:8]
            video_info = ''.join('%s' %id for id in video_info_list)
            # 获取magnet
            div_magnet = soup.find_all(name='div', attrs={'id': 'magnets-content'})[0]
            # 上传信息到wordpress
            content = '<p>'+str(image_src)+'\n'+video_info+'\n'+str(div_magnet)+'\n'+'</p>'
            # 调用方法上传到wordpress
            wpsend(content,title_replace,vido_info_kind)
            # print(content)
    except:
        print('不存在的页面----------------》》》》》', page_url)

def wpsend(content,title,vido_info_kind):
    try:
        # 链接地址，登录用户名，密码
        wp = Client('http://magnetkey.xyz/xmlrpc.php', 'bruce', 'flzx3qc@ysyhl9t')
        # wp = Client('http://192.168.190.145/xmlrpc.php', 'bruce','12345678')
        post = WordPressPost()
        post.title = str(title)
        post.content = " ''' " + content + " ''' "
        post.post_status = 'publish'
        post.terms_names = {
            'post_tag': ['magnet',vido_info_kind],
            'category': ['福利','magnet',vido_info_kind]
        }
        wp.call(NewPost(post))
        localtime = time.localtime(time.time())
        print('文档已上传 {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", localtime)))
    except:
        print('没有上传成功')
def mutli_thread():
    print('Mutlithread begin')
    threads_list = []
    for url in series_url(url_list):
        threads_list.append(
            threading.Thread(target=spyder_magnet,args=(url,))
        )
    for thread in threads_list:
        # 设置上传速度，否则会无法上传
        time.sleep(random.randint(60, 140))
        thread.start()
    for thread in threads_list:
        thread.join()


if __name__ == '__main__':
    # 返回单页信息
    mutli_thread()
    # spyder_magnet(url_list)