# coding:utf-8

import re
import requests
import random


class NeiHanDuanZi_Spidre():
    """
            内涵段子爬虫类
    """

    # 初始化
    def __init__(self):
        self.url = "http://www.neihanpa.com/article/list_5_"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36"
        }
        self.proxy_lise = [{'http': 'http://116.199.115.78:80'},
                           {'http': 'http://116.199.115.79:83'},
                           {'http': 'http://116.199.115.79:82'},
                           {'http': 'http://116.199.115.78:81'},
                           {'http': 'http://124.163.209.110:80'},
                           {'http': 'http://121.8.98.198:80'}]

        # 3. 第一层解析  注意: "''" == '""'字符串; 但是正则里不是
        # 一般代码里都是"" 所以一般用'""'写正则  具体看目标网站的代码决定用那个
        # 获取目标文本 通过类名的方式找到目标位置 这里的类名是  f18 mb20
        self.first_pattern = re.compile(r'<div class="f18 mb20">(.*?)</div>', re.S)

        # 4. 第二层解析
        # 标签 <(.*?)>
        # 字符实体 &(.*?);
        # 空白处  \s
        # 全角空格 　　
        self.second_pattern = re.compile(r'<(.*?)>|&(.*?);|\s|　　', re.S)

    # 1.请求方法
    def get_page(self, url):
        proxy = random.choice(self.proxy_lise)
        print proxy
        responst = requests.get(url, headers=self.headers,  proxies=proxy)
        data = responst.content
        return data

    # 2.数据解析方法
    def analysis_data(self,data):
        # 第一层解析
        result = self.first_pattern.findall(data)
        return result

    # 3.文件保存方法
    def write_file(self, data, page):
        filename = '第'+str(page)+'页正在下载。。。'
        print filename
        with open('neihan3.txt', 'a') as f:
            fliename = '-----------------第'+str(page)+'页-----------------\n'
            f.write(fliename)
            for context in data:
                # 第二层解析 替换掉不需要的 所以这里用 sub  不是用findall
                second_context = self.second_pattern.sub("", context)
                f.write(second_context)
                f.write("\n\n")

    # 执行方法
    def start_work(self):
        # 遍历要爬去的页数
        for page in range(1, 507):
            # 拼接URL
            full_url = self.url+str(page)+'.html'
            # 发送请求
            data = self.get_page(full_url)
            # 遇到乱码问题 所以改编码
            data = data.decode('gbk').encode('utf-8')
            # 解析数据 调用第一层解析
            analysis_data_list = self.analysis_data(data)
            # 保存到本地
            self.write_file(analysis_data_list, page)


if __name__ == '__main__':
    tool = NeiHanDuanZi_Spidre()
    tool.start_work()


