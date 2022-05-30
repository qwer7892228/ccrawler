import re
import os
import pandas as pd

pair_pattern = re.compile(r'\'([^\']+)\' => \'([^\']+)\'',re.M)
hans_pattern = re.compile(r'public static \$zh2Hans = \[([^]]*)]',re.M)
pardir = os.path.abspath(__file__)
pardir = os.path.dirname(pardir)


def make_dict(data, pattern,shopee_data_t2s):
    for p in pattern.findall(data):
        for list in pair_pattern.findall(p):
            shopee_data_t2s['name'] = shopee_data_t2s['name'].str.replace(list[0],list[1])

def abspath(path):
    global pardir
    return os.path.join(pardir, path)

def conv():
    with open(abspath('shopee_data.csv'),'r',encoding='utf-8') as shopee_data:
        shopee_data_t2s = pd.read_csv(shopee_data)

    with open(abspath('ZhConversion.php'), 'r', encoding='utf-8') as fin:
        php_data = fin.read()

    make_dict(php_data, hans_pattern,shopee_data_t2s)

    shopee_data_t2s.to_csv('shopee_data_t2s.csv',encoding='utf-8-sig', index =False)