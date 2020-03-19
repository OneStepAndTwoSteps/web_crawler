#author py chen

import requests
from fake_useragent import UserAgent
import os

location = os.getcwd() + '/fake_useragent.json'
ua = UserAgent(path=location)   # 创建User-Agent对象
useragent = ua.random
headers = {'User-Agent': useragent}


def ip_test(ip):
    url = 'http://www.baidu.com/'
    ip_port = ip.split(':')
    proxies = {
        'http': 'http://{}:{}'.format(ip_port[0], ip_port[1]),
        'https': 'https://{}:{}'.format(ip_port[0], ip_port[1]),
    }
    res = requests.get(url=url, headers=headers, proxies=proxies, timeout=5)
    if res.status_code == 200:
        return True
    else:
        return False


# 提取代理IP
def get_ip_list():
    # 快代理：https://www.kuaidaili.com/doc/product/dps/
    api_url = 'http://dev.kdlapi.com/api/getproxy/?orderid=946562662041898&num=100&protocol=1&method=2&an_an=1&an_ha=1&sep=2'
    html = requests.get(api_url).content.decode('utf-8', 'ignore')
    ip_port_list = html.split('\n')

    for ip in ip_port_list:
        with open('proxy_ip.txt', 'a') as f:
            if ip_test(ip):
                f.write(ip + '\n')


if __name__ == '__main__':
    get_ip_list()