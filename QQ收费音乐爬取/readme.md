#  ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling_qq_music/master/img/logo.png)这次提供了一个QQ音乐的下载code
    
## 实现过程我就不进行细说了，我这里大概讲一下思路

     1.首先我们打开抓包工具 我们可以直接定位到音乐文件所在的路径 如果不想code的话也可以打开f12直接找到链接然后下载
     2.多次添加歌曲，并且找到歌曲的文件之后对url进行分析，我们可以分析出有些参数是不变的 变的参数就是{}.m4a?和vkey
![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling_qq_music/master/img/vkey不同1.png)
![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling_qq_music/master/img/vkey不同1.png)
     3.这样我们只要找到对应的vkey和响应的mid号，就可以得到最终歌曲所在的url
     4.即采用逆向推理法，从如何获取vkey一层层向上推进

## 实现效果
    我这里把他打包成了exe格式执行
   ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling_qq_music/master/img/效果图1.png)
   ![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling_qq_music/master/img/效果图1.png)

## 好了那动手试试把
 
![Image text](https://raw.githubusercontent.com/OneStepAndTwoSteps/crawling_qq_music/master/img/2.jpg)
