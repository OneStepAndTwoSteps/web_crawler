#author py chen
import os
import threading
from multiprocessing import Pool,cpu_count
from bs4 import BeautifulSoup
import requests
import re
import logging

HEADERS={
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'http://www.mzitu.com'
}

SAVE_DIR='D:\MEIZITU'


def log():
    logger = logging.getLogger("mylogger")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


class get_picture():
    def __init__(self,urls=None):
        self.urls=urls
        # self.write_log = self.log()

        # self.write_log = self.log()

        # super(get_picture,self).__init__()

    def get_picture_urls(self):

        page_urls=['http://www.mzitu.com/page/{number}/'.format(number=i) for i in range(1,2)]
        image_urls=[]
        print("The program starts running...")
        for page_url in page_urls:
            html = requests.get(page_url, headers=HEADERS, timeout=10).text
            try:

                '''找出所有的存放图片的父标签'''
                bsobj = BeautifulSoup(html, 'lxml').find('ul', id='pins')

                '''取出除href开头的字符 
                即 <a href= 被去除 后面\S+ 匹配任何不是空格字符的字符 到空格处停止匹配 最后得出['"http://www.mzitu.com/150774"']
                <a href="http://www.mzitu.com/150774" target="_blank">欲女王雨纯情趣调教 她火热紧致让你性趣满满</a>
                str(bsobj)为要匹配的文本
                '''
                result=re.findall(r'(?<=href=)\S+',str(bsobj))

                '''列表表达式，将列表中的元素中的""全部去除  '''
                img_urls=[url.replace('"',"") for url in result]

                image_urls.extend(img_urls)

                # print(bsobj)
                # print(type(img_urls))


            except Exception as e:
                print("error %s" % e)

        return set(image_urls)


    def mkdir(self):
        if os.path.isdir(SAVE_DIR):
            pass
        else:
            write_log.info("开始创建主目录 %s.."%SAVE_DIR)
            os.mkdir(SAVE_DIR)

    def save_images(self,url,title,count):
        '''请求到真正的图片的url 然后保存到本地 img.content 保存图片'''
        if os.path.isdir(os.path.join(SAVE_DIR, title)):
            pass
        else:
            print("开始创建文件夹%s.." % title)

            os.mkdir(os.path.join(SAVE_DIR, title))


        img=requests.get(url,headers=HEADERS)

        image_name = "img{page}.jpg".format(page=count)

        with open(os.path.join(SAVE_DIR, title, image_name), 'ab') as f:
            print("开始下载%s.." % image_name)
            f.write(img.content)

    def download_pic(self,url):
        '''注意 在request之后后面要加.text 否则BeautifulSoup调用不了html
           会报错 TypeError: object of type 'Response' has no len()
        '''

        html=requests.get(url,headers=HEADERS,timeout=3).text
        # title=BeautifulSoup(html,'lxml').find("div",{"class":"main-image"}).find("img")["alt"]
        title=BeautifulSoup(html,'lxml').find("h2",{"class":"main-title"}).get_text()
        '''创建相应的目录'''

        '''计算出每个组图的数量'''
        max_page=BeautifulSoup(html,'lxml').find("div",{"class":"pagenavi"}).find_all("span")[-2].get_text()

        # with lock:
        img_url_list = []

        # img_url_list.clear()
        ''' 一组图片里面的个个图片的 url '''
        image_urls = [url + '/{page}'.format(page=i) for i in range(1, int(max_page))]
        # print(len(image_url))
        # print(image_url)
        for index,image_url in enumerate(image_urls,1):
            image_html=requests.get(image_url,headers=HEADERS,timeout=3).text
            img_url=BeautifulSoup(image_html,'lxml').find("div",{"class":"main-image"}).find("img")['src']
            # print(img_url)
            print("获取第%s个图片的url.." % index)
            '''append函数直接将object整体当作一个元素追加到列表中，而extend函数则是将可迭代对象中的元素逐个追加到列表中。'''
            img_url_list.append(img_url)
            '''可以看出 每个线程都启动了一个列表来存放url，各个线程分开互不干扰'''
            # print(img_url_list,threading.current_thread())
        # print("img_url_list: %s ,title: %s,max_page: %s"%(img_url_list,title,max_page))
        for patn_index, image_path in enumerate(img_url_list):
            print(image_path)
            self.save_images(image_path, title, patn_index)




if __name__ == '__main__':
    start_button=get_picture()
    urls=start_button.get_picture_urls()
    # print(urls)
    write_log = log()
    start_button.mkdir()

    # lock=threading.Lock()

    pool = Pool(processes=cpu_count())
    '''pool.map会将urls拆分成多个块，即将urls分割一个一个传入 '''
    pool.map(start_button.download_pic,urls)
    # start_button.download_pic(urls)
    # print(123)





