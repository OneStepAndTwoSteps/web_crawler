# 用于处理 json 文件中的 静态 start_urls 和 动态 start_urls

def china(start,end):

    for page in range(start,end+1):
        yield "http://tech.china.com/articles/index_" + str(page) + '.html'

