# utils 用于获取 json 数据

from os.path import realpath,dirname
import json

def get_config(name):
    path = dirname(realpath(__file__))+'/configs/'+name+'.json'
    with open(path,'r',encoding='utf-8') as f:
        return json.loads(f.read()) 


# data = get_config('china')
# print(data)