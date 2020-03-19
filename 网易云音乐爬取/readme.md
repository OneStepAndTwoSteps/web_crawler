# 爬取网易云音乐    注意这里不包含哪些收费的音乐(下次再研究)  
## download_music_list 下载的是列表音乐
  这里粗略的讲解一下歌曲的url是如何获取的
   ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling-wangyiyun-music/master/img/token.png)
   由上图可见 是通过该地址http://music.163.com/weapi/song/enhance/player/url?csrf_token=请求的mp3地址的
   ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling-wangyiyun-music/master/img/post.png)
   这里可以看到我们获取的 mp3 url 的url是通过post参数(传过去的params和encSecKet)获取而来的
   如何造出params和encSecKey  可以参考  https://www.zhanghuanglong.com/detail/csharp-version-of-netease-cloud-music-api-analysis-(with-source-code)
   
   在coding中遇到了一些坑  我也在代码中备注了 可以参考一下   
   
   其中在获取song?id的获取中我使用postman 获取链接之后不会发生跳转 html标签获取起来也更加方便
   ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling-wangyiyun-music/master/img/获取song_id.png)
   
###    可以做成exe格式，之后输入所要下载的歌单的URL即可  我这里就使用固定的url测试了
    
![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling-wangyiyun-music/master/img/使用1.png)
   
###    效果图：
 ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling-wangyiyun-music/master/img/%E4%B8%8B%E8%BD%BD%E6%95%88%E6%9E%9C%E5%9B%BE.png)
 ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling-wangyiyun-music/master/img/%E4%B8%8B%E8%BD%BD%E6%95%88%E6%9E%9C%E5%9B%BE2.png)

## download_music_Single 下载单曲音乐

###    输入所要下载的歌单的URL即可
