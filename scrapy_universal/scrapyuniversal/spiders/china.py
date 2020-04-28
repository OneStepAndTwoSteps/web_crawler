# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem
from scrapy.loader import  ItemLoader 
from ..loaders import ChinaLoader

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    # rules 必须是一个可迭代对象，即使 Rule 只有一条，后面也要加上 逗号（,）
    rules = (
        # 在 Rule 中利用 href 中的规则定义正则表达式，找出所有的新闻链接。
        # Rule(LinkExtractor(allow=r'article\/.*\.html',restrict_xpaths="//div[@class='item-con-inner']"), callback='parse_item'),
        Rule(LinkExtractor(allow=r'article\/.*\.html',restrict_xpaths="//div[@class='wntjItem item_defaultView clearfix'][1]/div[@class='item_con']/div[@class='item-con-inner']/h3[@class='tit']/a"), callback='parse_item'),
        
        # 找到下一頁的按钮
        # Rule(LinkExtractor(restrict_xpaths="//div[@class='pages']/ul/a[@class='a1'][3]"))
    )

    def parse_item(self, response):
        
        # item = NewsItem()
        # item['title'] = response.xpath("//h1[@id='chan_newsTitle']/text()").extract_first()
        # item['url'] = response.url
        # # 语法中分隔节点有两种方法/和//，它们之间的差别在于，前者只寻找子节点，后者会寻找子孙所有后代的节点，将所有满足条件的全都找到
        # item['text'] = ''.join(response.xpath("//div[@id='chan_newsDetail']//text()").extract()).strip()
        # item['datetime'] = ''.join(response.xpath("//div[@class='chan_newsInfo_source']/span[@class='time']/text()").extract())
        # item['source'] = response.xpath("//div[@class='chan_newsInfo_source']/span[@class='source']/text()").re_first('来源：(.*)')
        # item['website'] = '中华网'

        '''
        不过我们发现这种提取方式非常不规整。
        下面我们再用Item Loader，通过add_xpath()、add_css()、add_value()等方式实现配置化提取。我们可以改写parse_item()，如下所示：
        '''

        loader = ChinaLoader(item=NewsItem(),response=response)
        loader.add_xpath('title',"//h1[@id='chan_newsTitle']/text()")
        loader.add_value('url',response.url)
        loader.add_xpath('text',"//div[@id='chan_newsDetail']//text()")
        loader.add_xpath('datetime',"//div[@class='chan_newsInfo_source']/span[@class='time']/text()")
        loader.add_xpath('source',"//div[@class='chan_newsInfo_source']/span[@class='source']/text()",re='来源：(.*)')
        loader.add_value('website','中华网')

        yield loader.load_item()
