from scrapy.loader import ItemLoader

# Join：        方法相当于字符串的join()方法，可以把列表拼合成字符串，字符串默认使用空格分隔
# TakeFirst：   返回列表的第一个非空值，类似extract_first()的功能，常用作Output Processor
# Compose：     是用给定的多个函数的组合而构造的Processor，每个输入值被传递到第一个函数，其输出再传递到第二个函数，依次类推，直到最后一个函数返回整个处理器的输出
from scrapy.loader.processors import TakeFirst,Join,Compose

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

# ChinaLoader继承了NewsLoader类，其内定义了一个通用的Out Processor为TakeFirst，这相当于之前所定义的extract_first()方法的功能。
class ChinaLoader(NewsLoader):
    # 做两次对数据的标准化
    text_out = Compose(Join(),lambda s: s.strip())
    source_out = Compose(Join(),lambda s: s.strip())
