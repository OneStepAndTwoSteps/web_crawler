# 自定义的 rules 
# 每个Rule对爬取网站的动作都做了定义，CrawlSpider会读取rules的每一个Rule并进行解析

from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Rule


rules = {
    'china':(
        Rule(LinkExtractor(allow='article\/.*\.html',
        restrict_xpaths="//div[@class='wntjItem item_defaultView clearfix'][1]/div[@class='item_con']/div[@class='item-con-inner']/h3[@class='tit']/a"
        ),callback='parse_item'),
        
        # Rule(LinkExtractor(restrict_xpaths="//div[@class='pages']/ul/a[@class='a1'][3]"))
    )
}




