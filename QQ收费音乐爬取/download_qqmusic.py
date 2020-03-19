#author py chen

import requests
import os,json,re


class music_download():

    def __init__(self):
        self.HEADERS={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
        '''輸入搜索的歌曲之後，会返回一个json的包，里面有各个歌曲的id等信息 为了给获取到key做服务 '''
        self.soso_url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.top&searchid=34725291680541638&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={song_name}&g_tk=5381&jsonpCallback=MusicJsonCallback703296236531272&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        '''每个歌曲vkey 即使是同一首歌(song的ID相同) 他的返回的vkey也会不同'''
        self.get_vkey_url='https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback9239412173137234&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback9239412173137234&uin=0&songmid={song_mid}&filename={media_mid}.m4a&guid=8208467632'
        ''' 歌曲文件所在的URL  经过分析我们可以发现他有的信息是固定的 只有mid和vkey是变化的 所以我们只要获取到这两个变量将其放入到url即可  '''
        self.song_url='http://dl.stream.qqmusic.qq.com/{media_mid}.m4a?vkey={vkey}&guid=8208467632&uin=0&fromtag=66'

    def work(self,song_name,song_num):
        media_mid_list, song_mid_list, song_singer_list=self.song_list(song_name)
        media_mid=media_mid_list[song_num-1]
        song_mid=song_mid_list[song_num-1]
        song_singer=song_singer_list[song_num-1]
        vkey=self.get_vkey(media_mid,song_mid)
        self.download_music(vkey,media_mid,song_name,song_singer)

    def song_list(self,song_name):

        resp=requests.get(self.soso_url.format(song_name=song_name),headers=self.HEADERS).text

        # print(self.soso_url)

        '''获取medie_mid'''
        media_mid_list_temp=re.findall(r'"media_mid":"(.*?)"',resp)
        media_mid_list=['C400'+media_mid.replace('"',"") for media_mid in media_mid_list_temp]

        song_mid_list=re.findall(r'"lyric_hilight":".*?","mid":"(.*?)","mv"',resp)

        '''获取singer'''
        singer=[]
        song_singer = re.findall(r'"singer":\[.*?\]', resp)
        for s in song_singer:
            '''这里要获取singer'''
            singer.append(re.findall('"name":"(.*?)"', s)[0])

        songname = re.findall('},"name":"(.*?)","newStatus"', resp)

        # print('media_mid_list:%s len:%s'%(media_mid_list,len(media_mid_list)))
        # print("song_mid_temp%s len:%s"%(song_mid_list,len(song_mid_list)))
        # print("song_singer%s len:%s"%(song_singer,len(song_singer)))
        # print("song_singer%s len:%s"%(singer,len(singer)))

        # return mid_list,media_mid_list
        return media_mid_list,song_mid_list,singer

    def get_vkey(self,media_mid,song_mid):
        # print(self.get_vkey_url.format(media_mid=media_mid,song_mid=song_mid))
        resp=requests.get(self.get_vkey_url.format(song_mid=song_mid,media_mid=media_mid),headers=self.HEADERS).text
        # print(resp)
        vkey=re.findall(r'"vkey":"(.*?)"',resp)
        # print(vkey)
        return vkey[0]


    def download_music(self,vkey,media_mid,song_name,song_singer):
        if os.path.isdir("./MP3"):
            pass
        else:
            os.mkdir("./MP3")
        response=requests.get(self.song_url.format(media_mid=media_mid,vkey=vkey),headers=self.HEADERS)
        # print(os.path.join('./MP3',song_name+"_"+song_singer+".mp3"))
        with open(os.path.join('./MP3',song_name+"_"+song_singer+".mp3"),'wb') as f:
            f.write(response.content)


if __name__ == '__main__':

    song_name=input("请输入你要下载的歌曲的名称：")
    song_num=input("请输入你要下载的歌曲在列表上的排序是第几位：")
    run=music_download()
    run.work(song_name,int(song_num))
