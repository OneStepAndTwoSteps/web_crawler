# docker 镜像 selenium/standalone-chrome

`项目地址：` [selenium/standalone-chrome](https://github.com/SeleniumHQ/docker-selenium) 

`docker hub 地址：` [selenium/standalone-chrome](https://hub.docker.com/search?q=selenium%2Fstandalone-chrome&type=image) 



*   重点介绍一下：`selenium/standalone-chrome:` 安装有 Chrome 的 Selenium Node 节点镜像

`docker-selenium` 项目（ 镜像仓库 , 代码仓库 ）是将 selenium、webdriver、VNC server、chrome（或者firefox）集成在一个docker镜像里的项目。提供如下的功能：

*   代替原有的 remote webdriver
*   单个容器就能提供全套 selenium+webdriver+headless 浏览器的功能
*   几个容器配合就能完全代替 selenium grid（目前仅限chrome和firefox）
*   包含 VNC server（远程桌面），方便远程调试 headless 浏览器
*   全部在 linux 环境下执行，无需设置 windows 节点机，方便自动化
*   方便自定义 Dockerfile ，用户可以自己制作镜像

### 详细参考：

[当 selenium 遇上 docker ](https://www.lfhacks.com/tech/selenium-docker)


