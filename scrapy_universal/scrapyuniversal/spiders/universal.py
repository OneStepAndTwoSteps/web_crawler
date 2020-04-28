# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import get_config
from ..rules import rules
from ..loaders import ChinaLoader
from ..items import NewsItem
from scrapyuniversal import urls

class UniversalSpider(CrawlSpider):
    name = 'universal'

    def __init__(self,name,*args,**kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        start_urls = config.get('start_urls')

        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                # 'urls.'+start_urls.get('method') 用于获取 urls.py 中相应的处理函数，如 urls.china
                # (*start_urls.get('args',[])) 用于传递参数
                # 最后会将返回结果依次存储在 list 中，赋值给 self.start_urls
                self.start_urls = list(eval('urls.'+start_urls.get('method'))(*start_urls.get('args',[])))

        self.allowed_domains = config.get('allowed_domains')
        super(UniversalSpider,self).__init__(*args,**kwargs)    # 初始化父类的 __init__ 必须加上

    def parse_item(self, response):
        item = self.config.get('item')
        # print('item: ',item)
        if item:

            # 相当于 loader = itemloader(item = loader,response = response)
            cls = eval(item.get('class'))()                             # 使用 eval 函数来实例化类  eval(item.get('class')) 相当于cls的内存地址，后面加上()，实例化。
            loader = eval(item.get('loader'))(cls,response=response)    # 实例化函数，cls,response 是参数
            
            # 动态获取属性配置 针对 loader 中的配置
            for key,value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key,*extractor.get('args'),**{'re':extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key,*extractor.get('args'),**{'re':extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key,*extractor.get('args'),**{'re':extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key,getattr(response,*extractor.get('args')))

            yield loader.load_item()            


