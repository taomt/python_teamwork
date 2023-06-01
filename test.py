'''
测试用
'''

import re
import requests
from lxml import etree

if __name__ == '__main__':
    map_url: str = 'https://nc.newhouse.fang.com/loupan/2310201034.htm#detail_map'
    res: str = requests.get(map_url, timeout=None).text
    iframe: etree._Element = etree.HTML(res).xpath('//*[@id="iframe_map"]')[0]
    iframe_url: str = iframe.attrib['src']
    res: str = requests.get(f'https:{iframe_url}', timeout=None).text
    script: etree._Element = etree.HTML(res).xpath('/html/body/script[4]')[0]
    reg = re.compile(r'_vars.cityx = "(.*)";[\s\S]*_vars.cityy = "(.*)"')
    latitude, longitude = reg.findall(script.text)[0]
    print(latitude, longitude)
