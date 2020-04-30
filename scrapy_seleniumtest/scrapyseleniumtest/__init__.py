item= {'deal': '395人付款',
 'image': '//g-search3.alicdn.com/img/bao/uploaded/i4/i3/3261336459/O1CN0168tnnP1xaGmmNvHOF_!!0-item_pic.jpg',
 'location': '广东 广州',
 'price': '¥1299.00',
 'shop': '荣耀港讯专卖店',
 'title': '【现货当天发】荣耀平板5 10英寸12大屏智能安卓超薄新款pad全网通全新二合一平板电脑华为手机ipad10.1m5m6'}

data = dict(item)
keys = ', '.join(data.keys())
values = ', '.join(['% s'] * len(data))
# values = ', '.join(data.values())
sql = 'insert into % s (% s) values (% s)'%('table1', keys, values)
print(keys)
print(values)
print(sql)

# insert into table1 (deal, image, location, price, shop, title) values ('395人付款', '//g-search3.alicdn.com/img/bao/uploaded/i4/i3/3261336459/O1CN0168tnnP1xaGmmNvHOF_!!0-item_pic.jpg', '广东 广州', '¥1299.00', '荣耀港讯专卖店', '【现货当天发】荣耀平板5 10英寸12大屏智能安卓超薄新款pad全网通全新二合一平板电脑华为手机ipad10.1m5m6')


