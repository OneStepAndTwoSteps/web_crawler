# run 用于启动程序
import sys
from scrapy.utils.project import get_project_settings
from scrapyuniversal.spiders.universal import UniversalSpider
from scrapyuniversal.utils import get_config
from scrapy.crawler import CrawlerProcess

def run():
    name = sys.argv[1]
    
    # 获取定义的 json 文件数据
    custom_settings = get_config(name)

    # 获取爬取使用的 spider 名称
    spider = custom_settings.get('spider','universal')  # 如果不存在默认使用 universal
    print("spider_name: ",spider)
    project_settings = get_project_settings()           # 读取settings设置文件
    settings = dict(project_settings.copy())

    # 合并配置
    settings.update(custom_settings.get('settings'))    # 将 settings 中的配置和 自定义 的配置合并
    process = CrawlerProcess(settings)                  # 使用 CrawlerProcess 来实例化 爬虫程序

    # 启动爬虫
    process.crawl(spider,**{'name':name})               # 传入名称 开始爬取 相当于 scrapy crawl spider_name
    process.start()

if __name__ == "__main__":
    run()