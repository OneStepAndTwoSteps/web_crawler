#author py chen

import random
import requests


class BaiduSpider(object):
    def __init__(self):
        self.url = 'http://www.baidu.com/'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.flag = 1

    def get_proxies(self):
        with open('proxies.txt', 'r') as f:
            result = f.readlines()             # 读取所有行并返回列表
        proxy_ip = random.choice(result)[:-1]       # 获取了所有代理IP
        L = proxy_ip.split(':')

        proxy_ip = {
            'http': 'http://{}:{}'.format(L[0], L[1]),
            'https': 'https://{}:{}'.format(L[0], L[1])
        }

        return proxy_ip

    def get_html(self):
        proxies = self.get_proxies()
        # proxies = {'http': 'http://117.88.177.3:3000', 'https': 'https://117.88.177.3:3000'}

        if self.flag <= 10:
            try:
                html = requests.get(url=self.url, proxies=proxies, headers=self.headers, timeout=2).text
                # print(html)
                print(proxies)
            except Exception as e:
                print('{} 已失效 Retry'.format(proxies))

                self.flag += 1
                self.get_html()


if __name__ == '__main__':
    spider = BaiduSpider()
    spider.get_html()
