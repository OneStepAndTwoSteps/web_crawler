# Selenium Notes

## webdriver 中的 ChromeOptions 

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    chrome_options = ChromeOptions()

常用的参数：

    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])    # 设置成开发者模式
    chrome_options.add_experimental_option('useAutomationExtension', False)             # 取消chrome受自动控制提示

    chrome_options.add_argument("--window-size=1920,1080")              #指定浏览器分辨率
    chrome_options.add_argument('--headless')                           # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chrome_options.add_argument('--no-sandbox')                         #彻底停用沙箱，解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--hide-scrollbars')                    #隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')   #不加载图片, 提升速度
    chrome_options.add_argument('--disable-extensions')                 #禁用拓展。
    chrome_options.add_argument('--disable-gpu')                        #谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.binary_location = r'/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary' #手动指定使用的浏览器位置

其他的参数：

    # 启动就最大化
    --start-maximized 

    # 指定用户文件夹 User Data 路径，可以把书签这样的用户数据保存在系统分区以外的分区
    –-user-data-dir=”[PATH]” 

    # 指定缓存Cache路径
    –-disk-cache-dir=”[PATH]“ 

    # 指定Cache大小，单位Byte
    –-disk-cache-size=100 

    # 隐身模式启动
    –-incognito 

    # 禁用Javascript
    –-disable-javascript 

    # 禁止加载所有插件，可以增加速度
    --disable-plugins 

    # 禁用JavaScript
    --disable-javascript 

    # 禁用弹出拦截
    --disable-popup-blocking 

    # 禁用插件
    --disable-plugins 

    # 禁用图像
    --disable-images 


详细：[`chrome 配置`](https://www.jianshu.com/p/5669fa439c2b)

    序号  参数  说明
    1   --allow-outdated-plugins     不停用过期的插件。
    2   --allow-running-insecure-content     默认情况下，https 页面不允许从 http 链接引用 javascript/css/plug-ins。添加这一参数会放行这些内容。
    3   --allow-scripting-gallery    允许拓展脚本在官方应用中心生效。默认情况下，出于安全因素考虑这些脚本都会被阻止。
    4   --disable-accelerated-video  停用 GPU 加速视频。
    5   --disable-dart   停用 Dart。
    6   --disable-desktop-notifications  禁用桌面通知，在 Windows 中桌面通知默认是启用的。
    7   --disable-extensions     禁用拓展。
    8   --disable-file-system    停用 FileSystem API。
    9   --disable-preconnect     停用 TCP/IP 预连接。
    10  --disable-remote-fonts   关闭远程字体支持。SVG 中字体不受此参数影响。
    11  --disable-speech-input   停用语音输入。
    12  --disable-web-security   不遵守同源策略。
    13  --disk-cache-dir     将缓存设置在给定的路径。
    14  --disk-cache-size    设置缓存大小上限，以字节为单位。
    15  --dns-prefetch-disable   停用DNS预读。
    16  --enable-print-preview   启用打印预览。
    17  --extensions-update-frequency    设定拓展自动更新频率，以秒为单位。
    18  --incognito  让浏览器直接以隐身模式启动。
    19  --keep-alive-for-test    最后一个标签关闭后仍保持浏览器进程。（某种意义上可以提高热启动速度，不过你最好得有充足的内存）
    20  --kiosk  启用kiosk模式。（一种类似于全屏的浏览模式）
    21  --lang   使用指定的语言。
    22  --no-displaying-insecure-content     默认情况下，https 页面允许从 http 链接引用图片/字体/框架。添加这一参数会阻止这些内容。
    23  --no-first-run   跳过 Chromium 首次运行检查。
    24  --no-referrers   不发送 Http-Referer 头。
    25  --no-sandbox     彻底停用沙箱。
    26  --no-startup-window  启动时不建立窗口。
    27  --proxy-pac-url  使用给定 URL 的 pac 代理脚本。（也可以使用本地文件，如 --proxy-pac-url="file:\\\c:\proxy.pac"）
    28  --proxy-server   使用给定的代理服务器，这个参数只对 http 和 https 有效。（例如 --proxy-server=127.0.0.1:8087 ）
    29  --single-process     以单进程模式运行 Chromium。（启动时浏览器会给出不安全警告）
    30  --start-maximized    启动时最大化。
    31  --user-agent     使用给定的 User-Agent 字符串

    参数：--user-data-dir=UserDataDir
    用途：自订使用者帐户资料夹（如：–user-data-dir="D:\temp\Chrome User Data"）
    参数：--process-per-tab
    用途：每个分页使用单独进程
    参数：--process-per-site
    用途：每个站点使用单独进程
    参数：--in-process-plugins
    用途：插件不启用单独进程

    参数：--disable-popup-blocking
    用途：禁用弹出拦截
    参数：--disable-javascript
    用途：禁用JavaScript
    参数：--disable-java
    用途：禁用Java
    参数：--disable-plugins
    用途：禁用插件
    参数：–disable-images
    用途：禁用图像
    参数：--omnibox-popup-count=”num”
    用途：将网址列弹出的提示选单数量改为num个
    参数：--enable-vertical-tabs
    用途：调整chrome游览器标签存放在左边，非顶部


