#author py chen
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions  as EC
import time
import csv

driver=webdriver.Chrome()
url_path="https://movie.douban.com/subject_search?search_text={director}&start={start}"

director="宁浩"
# director="周星驰"

# director_list=["成龙","Jackie Chan"]
director_list=["宁浩"]
# director_list=["周星驰"]

# 創建CSV文件

file_path='导演'+ director +'.csv'
# 用于区分换行符(只对文本模式有效，可以取的值有None,'\n','\r','','\r\n')
# csv标准库中的writerow在写入文件时会加入'\r\n'作为换行符，if newline is ''，换行符不会被转化而是直接输出就是'\r\n'
out=open(file_path,'a',newline='',encoding='utf-8')
csv_writer=csv.writer(out,dialect='excel')

# 用于标记已经写入文件的电影，防止重复
flag=[]

def download(page_url):
    driver.get(page_url)
    time.sleep(1)

    wait = WebDriverWait(driver,timeout=20)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='meta abstract_2']")))
    except:
        pass

    actor_name_lists = driver.find_elements_by_xpath("/html/body/div[@id='wrapper']/div[@id='root']/div[1]//div[@class='item-root']/div[@class='detail']/div[@class='meta abstract_2']")
    movie_name_lists = driver.find_elements_by_xpath("/html/body/div[@id='wrapper']/div[@id='root']//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']")

    print(actor_name_lists)
    print(movie_name_lists)



    if len(movie_name_lists)>=16:   #第一页会有16条数据
        # 默认第一个不是，所以需要去掉
        movie_name_lists=movie_name_lists[1:]
        actor_name_lists=actor_name_lists[1:]

    print("actor_name_list: ",actor_name_lists)
    print("movie_name_list: ",movie_name_lists)

    for movie_name,actor_name in zip(movie_name_lists,actor_name_lists):

        movie_name = movie_name.text
        actor_name = actor_name.text
        # 将名字分开
        names=actor_name.split('/')
        print("movie_name: ",movie_name)
        print("actor_name: ",actor_name)

        # names[0]是导演名称
        print("导演名称： ",names[0])
        if names[0].strip() in  director_list and movie_name not in flag:
            # 如果第一个字段是导演，那么设置第一个字段为电影名称，并写入csv文件
            names[0]=movie_name
            flag.append(movie_name)
            print("开始写csv文件..........")

            csv_writer.writerow(names)

    # 如果没有电影显示了就退出
    if len(movie_name_lists) < 1:
        return False
    else:
        return True


if __name__ == '__main__':
    for i in range(0,3):
        # 以 15 划分一页
        page_url=url_path.format(director=director,start=i*15)
        print(page_url)

        return_code=download(page_url)

        if return_code:
            pass
        else:
            break

    out.close()
