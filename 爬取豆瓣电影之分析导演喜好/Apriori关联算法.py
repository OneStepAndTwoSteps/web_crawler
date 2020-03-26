#author py chen
from efficient_apriori import apriori
import csv

director="宁浩"
data=open('导演'+ director +'.csv','r',encoding='utf-8')
lists=csv.reader(data)
# print(data.read())

data_lists=[]
for names in lists:
    # print(names)
    actor_list=[]
    for name in names:
        # 去掉数据中的空格
        new_name=name.strip()
        actor_list.append(new_name)
    # 取出名字
    data_lists.append(actor_list[1:])
print(data_lists)

data.close()

# min_support 最小支持度，min_confidence 最小置信度
itemsets,rules = apriori(data_lists,min_support=0.3,min_confidence=1)
print(itemsets)
print(rules)


