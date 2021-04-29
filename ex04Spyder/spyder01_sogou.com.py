import requests

#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
url = "https://www.sogou.com/web"
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
kw = input("输入要搜索的内容")
param = {
    'query':kw
}
def request_url():
    res = requests.get(url=url,headers=header,params=param)
    page_text = res.text
    fileName = kw +'.html'
    with open(fileName,'w',encoding='utf-8') as f:
        f.write(page_text)
    print(fileName,'保存成功！！！')


if __name__ == '__main__':
    request_url()

