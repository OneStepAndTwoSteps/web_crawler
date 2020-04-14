# 反爬虫措施

反爬虫措施合集

## 防止selenium被认出

做了反爬虫的服务端，使用一行`Javascript`代码，就能轻轻松松识别你是否使用了`Selenium + Chromedriver`模拟浏览器。

*   `自动化控制的chrome` 在 `console` 中输入：`window.navigator.webdriver` 返回的值为 `True` 

*   `真实打开的chrome` 在 `console` 中输入：`window.navigator.webdriver` 返回的值为 `undefined` 

### 解决方案1（适合新版chrome）：

可以在`selenium`中调用`CDP`命令,使用 `selenium` 中的 `execute_cdp_cmd` 。

通过这个命令，我们可以给定一段 `JavaScript` 代码，让 `Chrome` 刚刚打开每一个页面，还没有运行网站自带的 `JavaScript` 代码时，就先执行我们给定的这段代码。

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

只需要执行一次，之后只要你不关闭这个 `driver` 开启的窗口，无论你打开多少个网址，他都会自动提前在网站自带的所有 `js` 之前执行这个语句，隐藏 `window.navigator.webdriver`。


### 解决方案2（适合老版chrome）：

注意：`chrome` 更新后该方法已失效

    from selenium.webdriver import Chrome
    from selenium.webdriver import ChromeOptions

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)

你可以通过在自动化控制 `chrome` 中再使用 `window.navigator.webdriver` 查看返回值，返回值仍为 `True`。