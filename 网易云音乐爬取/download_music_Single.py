#author py chen
import os,json,requests
from scrapy.selector import Selector
from  binascii import hexlify
from Crypto.Cipher import AES
import base64
import re

url='http://music.163.com/weapi/song/enhance/player/url?csrf_token='
HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'http://music.163.com/'}



class Encrypyed():
    '''加密算法'''
    def __init__(self):
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        # self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'

    def create_secret_key(self, size):
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    def aes_encrypt(self,text, key):
        iv = '0102030405060708'
        '''以下两行code是为了保证text的length是16的整数倍'''
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)

        encryptor = AES.new(key, AES.MODE_CBC, iv)
        result = encryptor.encrypt(text)
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    def rsa_encrpt(self,text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(hexlify(text.encode('utf-8')), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def work(self,text):
        '''将字典转成字符串,加密的数据不能为字典'''
        text = json.dumps(text)
        # print('text',text)
        '''生成16位的随机数'''
        i=self.create_secret_key(16)
        # print("i",i)
        '''开始aes加密'''
        encText =self.aes_encrypt(text, self.nonce)
        # print("encText1",encText)
        '''开始第二次aes加密'''
        encText=self.aes_encrypt(encText,i)
        # print("encText2",encText)
        '''加密获取到encSecKey'''
        encSecKey=self.rsa_encrpt(i,self.pub_key,self.modulus)
        # print("encSecKey",encSecKey)
        data = {'params': encText, 'encSecKey': encSecKey}
        # print(data)
        return data

class core():
    def __init__(self,id):
        self.headers=HEADERS
        self.id=id
        self.session=requests.Session()
        self.session.headers = self.headers
        self.main_url='http://music.163.com/'
        self.url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='

        self.download_path = 'D:/a py Place of storage/crawling/download_music/music'

    # def get_music_list(self):
    #     '''在这里同学们要注意了如果直接返回网页http会转成https url也会发生变化 html标签也会发生变化
    #        如输入http://music.163.com/playlist?id=2440489579  会自动转成 https://music.163.com/#/playlist?id=2440489579
    #        并且/song?id 要么被隐藏 要么就是变成了变量 获取不到相应的id的值 所以很难定位到真正的id
    #        我这里使用postman请求url返回的信息 url不会发生跳转 可以找到相应的xpath 对应到 /song?id
    #     '''
    #     URL='http://music.163.com/playlist?id={id}'.format(id=self.id)
    #     re = self.session.get(URL)
    #     sel = Selector(text=re.text)
    #     urls=sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
    #     #返回的song?id
    #     #['/song?id=534542079', '/song?id=34923303', '/song?id=34003562', '/song?id=493316158', '/song?id=1217558',
    #     #  '/song?id=472117541', '/song?id=26260757', '/song?id=2068708', '/song?id=27162707', '/song?id=406346674',
    #     #  '/song?id=22846478', '/song?id=28954188', '/song?id=426850742']
    #     return urls

    def download_music(self,song_name,song_singer,url):
        with open(os.path.join(self.download_path,song_name+"-"+song_singer+'.mp3'),'wb') as f:
            music=requests.get(url)
            # print(music.content)
            f.write(music.content)

    def work(self):
        if os.path.isdir(self.download_path):
            pass
        else:
            os.mkdir(self.download_path)

        # urls_list=self.get_music_list()
        # 获取id的值
        # id=[id.replace("/song?id=",'') for id in urls_list]
        d=Encrypyed()
        # for id in id_lists:
        id=int(self.id)
        text = {"ids": [id], "br": 128000, "csrf_token": ""}
        data = d.work(text)
        song_url=self.get_music_url(data)
        song_name,song_singer=self.get_music_info(id)
        print("song_name",song_name)
        print("song_singer",song_singer)
        print("song_url",song_url)
        # exit()
        self.download_music(song_name,song_singer,song_url)

    def get_music_info(self,id):
        URL='http://music.163.com/song?id={id}'.format(id=id)
        re = self.session.get(URL)
        sel = Selector(text=re.text)
        # extract 为了提取真实的原文数据，你需要调用 .extract() extract返回列表
        song_name=sel.xpath('//em[@class="f-ff2"]/text()').extract_first()
        song_singer=sel.xpath('//a[@class="s-fc7"]/text()').extract_first()
        # print(song_name,song_singer)
        # exit()
        return song_name,song_singer
    def get_music_url(self,data):
        while True:
            try:
                resp=self.session.post(self.url,data=data)
                # print(resp.text)
                data=json.loads(resp.text)
                print('data',data)
                url=data['data'][0]['url']
                return url

            except Exception as e:
                print("error %s"%e)
                continue

        # print(resp.text)



if __name__ == '__main__':

    # music_list_url=input("请输入你要下载的网易云音乐列表所在的链接")
    run=core(list_id)
    run.work()




# do=Encrypyed()
# data=do.work({"ids": [534542079], "br": 128000, "csrf_token": ""})


# session = requests.Session()
# session.headers=headers
# re=session.post(url,data=data)
# print(re.text)
