# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import  getLogger
import time

class SeleniumMiddleware():
    def __init__(self,timeout=None):

        self.logger = getLogger(__name__)
        self.timeout = timeout
        print('self.timeout: ',timeout)
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver,timeout)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
        })

    def __del__(self):
        
        self.driver.close()

    # def login(self):
    #     user_input = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="fm-login-id"]')))
    #     pass_input = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="fm-login-password"]')))

    #     user_input.clear()
    #     pass_input.clear()
        
    #     user_input.send_keys('')
    #     pass_input.send_keys('')

    #     submit = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="login-form"]/div[4]/button')))
    #     submit.click()

        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager li.item.active.span')))


    def process_request(self,request,spider):
        print(222222222222222222222222222222222222222222)
        self.logger.debug('selenium is starting')
        page = request.meta.get('page',1)
        try:
            self.driver.get(request.url)
            # if self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="fm-login-id"]'))):
                # self.login()

            if page >1 :
                page_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
                submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form> span.btn.J_Submit'))) 
                page_input.clear()
                page_input.send_keys(page)
                submit.click()

            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active> span'),str(page)))
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
            print(22222222222223333333333333333333333333333)

            return HtmlResponse(url=request.url,body=self.driver.page_source,request=request,encoding='utf-8',status=200)
        except:
            return HtmlResponse(url=request.url,status=500,request=request)
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))





