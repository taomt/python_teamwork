'''
market.py
'''

import requests
from  lxml import etree
import pandas as pd
if __name__ == "__main__":
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
    }
    #爬取网页源码数据
    url='https://www.maigoo.com/top/430869.html'
    page_text=requests.get(url=url,headers=headers).text
    #数据解析
    tree=etree.HTML(page_text)

    li_list=tree.xpath('//ul[@class="citiaobtnlist"]/li')

    fp=open('market/market.json', 'w', encoding='utf_8')
    for li in li_list:
        #局部解析
        title=li.xpath('.//text()')[0]
        print(title)
        fp.write(title+'\n')
