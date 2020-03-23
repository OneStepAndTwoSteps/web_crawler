# 反爬虫措施

反爬虫措施合集

## 防止selenium被认出

做了反爬虫的服务端，使用一行Javascript代码，就能轻轻松松识别你是否使用了Selenium + Chromedriver模拟浏览器。

### 解决方案：

    from selenium.webdriver import Chrome
    from selenium.webdriver import ChromeOptions

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)


