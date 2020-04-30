# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from ..items import ProductItem

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url  = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1,self.settings.get('MAX_PAGE')+1):

                # quote 用于对字符串进行url编码，按照标准， URL 只允许一部分 ASCII 字符（数字字母和部分符号），其他的字符（如汉字）是不符合 URL 标准的。
                # 所以 URL 中使用其他字符就需要进行 URL 编码。
                url = self.base_url + quote(keyword)             
                #    meta 参数用于指定参数，在取参数的时候可以使用 response.meta['page']
                print(11111111111111111111111111111111111111111111)
                yield scrapy.Request(url=url,callback=self.parse,meta={'page':page},dont_filter=True)

    def parse(self, response):
        print(33333333333333333333333333333333333333333333333)
        products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class,"item")]')
        print('products: ',products)        # 注意 这里输出的数据显示是不完整的

        for product in products:
            item = ProductItem()
            print('product: ',product)
            item['price'] = ''.join(product.xpath('.//div[contains(@class,"price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class,"title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class,"shop")]//text()').extract()).strip()
            item['image'] = ''.join(product.xpath('.//div[contains(@class,"pic")]//@data-src').extract()).strip()
            
            item['deal'] = ''.join(product.xpath('.//div[contains(@class,"deal-cnt")]//text()').extract()).strip() 
            item['location'] = product.xpath('.//div[contains(@class,"location")]//text()').extract_first()
       
            # print('item:',item)
            yield item


