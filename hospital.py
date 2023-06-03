'''
hospital.py
'''

import json
import os
import re
import requests
from lxml import etree


def get_hospitals() -> None:
    '''
    获取南昌市所有医院的信息并保存为 json 文件
    '''
    # 保证文件夹存在
    if not os.path.exists('./hospital'):
        os.mkdir('./hospital')
    json_path: str = './hospital/hospital.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write('[]')

    # 发送请求
    res_text = requests.get(
        url=Constance.base_url,
        headers=Constance.headers,
        timeout=None,
    ).text

    # 获取 node 树，并通过 xpath 获取医院列表
    tree = etree.HTML(res_text)
    li_list: list = tree.xpath(
        '//*[@id="el_result_content"]/div/div[2]/div[2]/div[2]/ul/li')

    hospitals: list[dict] = []

    for li in li_list:
        position = get_position_by(li.xpath('a/@href')[0])
        if position is not None:
            name = li.xpath('a/text()')[0]
            hospital = Hospital(name, position[0], position[1])
            hospitals.append(hospital.__dict__)

    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(hospitals, ensure_ascii=False, indent=2))


def get_position_by(url: str) -> tuple[str, str] | None:
    '''
    根据 `url` 获取经纬度
    '''
    url = url.replace('.html', '/jieshao.html')
    print(f'> 正在获取 {url}')
    res: str = requests.get(url, headers=Constance.headers, timeout=None).text
    tree = etree.HTML(res)
    try:
        map_url = tree.xpath(
            '//*[@id="app"]/div[3]/div[1]/div[1]/div[1]/div/p/span/a/@href')[0]
    except IndexError:
        return None
    reg = re.compile(r'location=(.*),(.*?)&')
    return reg.findall(map_url)[0]


class Constance:
    '''
    存放常数信息
    '''
    # headers 信息
    headers: dict = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
    }
    # 根 url
    base_url: str = 'https://www.haodf.com/hospital/list-3601.html'


class Hospital:
    name: str
    latitude: str
    longitude: str

    def __init__(
        self,
        name: str,
        latitude: str,
        longitude: str,
    ) -> None:
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


if __name__ == '__main__':
    get_hospitals()
