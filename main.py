"""
Nanchang real estate
"""

import os
import json
import requests
from lxml import etree


def get_building_areas() -> None:
    """
    获取所有地区的房市信息并保存为 json 文件
    """
    # 保证文件夹存在
    if not os.path.exists('./building_area'):
        os.mkdir('./building_area')
    # 遍历各地区
    for area in Constance.areas:
        # 先写空文件
        json_path: str = f'./building_area/{area}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write('[]')
        get_building_area(f'{Constance.base_url}/house/s/{area}', area)


def get_building_area(url: str, area: str) -> None:
    """
    通过 url 和 area 获取房市信息
    注意一个 area 可以对应多个 url
    """

    # 发送请求
    res_text = requests.get(
        url=url,
        headers=Constance.headers,
        timeout=None,
    ).text

    # 获取 node 树，并通过 xpath 获取楼盘列表
    tree = etree.HTML(res_text)
    li_list: list = tree.xpath('//div[@id="newhouse_loupan_list"]/ul/li')

    # 读取原先的 json 文件
    json_path: str = f'./building_area/{area}.json'
    buildings: list[dict] = read_json_file_as_list(json_path)

    # 遍历列表
    for li in li_list:
        # 通过 xpath 获取楼盘名称与价位
        name: str = li.xpath('.//div[@class="nlcd_name"]/a/text()')[0].strip()
        prices: list = li.xpath('.//div[@class="nhouse_price"]/span/text()')
        img_url: str = "https:" + li.xpath('.//div[@class="nlc_img"]//img[1]/@src')[0]
        map_url: str = li.xpath('.//div[@class="address"]/a/@href')[0]
        phone: list = li.xpath('.//div[@class="tel"]/p/text()')
        # 数据合理则添加至列表
        if prices and prices[0] != '价格待定':
            price: str = prices[0]
            building = BuildingArea(name, price, img_url, map_url, phone)
            buildings.append(building.__dict__)

    # 写入文件
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(buildings, indent=2, ensure_ascii=False))

    print(f'> 已将 {url} 的数据写入 {json_path}')

    # 最后检查是否是最后页，不是则获取下一页
    next_page = tree.xpath('//a[@class="next"]/@href')
    last_page = tree.xpath('//a[@class="last"]/@href')
    if next_page and last_page:
        next1: int = next_page[-1][-3:-1]
        last: int = last_page[-1][-3:-1]
        if last > next1:
            get_building_area(Constance.base_url + next_page[-1], area)


def read_json_file_as_list(path) -> list[dict]:
    """
    将 json 文件读取为 list
    """
    lst: list[dict] = []
    with open(path, 'r+', encoding='utf-8') as f:
        lst = json.loads(f.read())
    return lst


class Constance:
    """
    存放常数信息
    """
    # headers 信息
    headers: dict = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
    }
    # 根 url
    base_url: str = 'https://nc.newhouse.fang.com'
    # 各地区
    areas: list[str] = [
        'honggutan', 'gaoxinkaifaqu', 'qingshanhu', 'xihu', 'nanchangxian',
        'donghu', 'jingkaiqu', 'qingyunpu', 'wanli', 'xinjian', 'jinxian'
    ]


class BuildingArea:
    """
    BuildingArea 类
    """
    name: str
    price: str

    def __init__(self, name: str, price: str, img_url: str, map_url: str, phone: list) -> None:
        self.name = name
        self.price = price
        self.img_url = img_url
        self.map_url = map_url
        self.phone = phone

    def __str__(self) -> str:
        return self.__dict__.__str__()


if __name__ == '__main__':
    get_building_areas()