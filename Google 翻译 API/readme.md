# 一个封装Google的小软件

## 制作方法：
   1.当我们想要翻译一个单词或者其他文字的时候 我们在翻译框中输入 可以看到url会发生变化 url直接发生变化 一般都是get请求提交
   2.进入Google 翻译的网页 打开f12 输入我们要翻译的内容  按f5刷新 找到发请求的url  即为
   	https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=1&tk=182860.282026&q=%E6%88%91%E6%93%8D
   3.在该url中有两项是会发生变化的 一项是tk 他会随着翻译内容的不同而发生变化 而q则是我们要翻译的内容
   4.tk的获取是靠js获取 如何获取 已经在代码中贴出

   
