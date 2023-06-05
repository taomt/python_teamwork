'''
get_building_areas.py
'''

import os
import json
import re
import requests
from lxml import etree
from retry import retry

from kit import read_json_file_as_list
from model_building_area import BuildingArea, BuildingAreaConstance


def get_building_areas() -> None:
    '''
    获取所有地区的房市信息并保存为 json 文件
    '''
    # 保证文件夹存在
    if not os.path.exists('./building_area'):
        os.mkdir('./building_area')
    # 遍历各地区
    for area in BuildingAreaConstance.areas:
        # 先写空文件
        json_path: str = f'./building_area/{area}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write('[]')
        get_building_area(
            f'{BuildingAreaConstance.base_url}/house/s/{area}',
            area,
        )


def get_building_area(url: str, area: str) -> None:
    '''
    通过 url 和 area 获取房市信息
    注意一个 area 可以对应多个 url
    '''

    # 发送请求
    res_text = requests.get(
        url=url,
        headers=BuildingAreaConstance.headers,
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
        id_url: str = li.xpath('.//div[@class="nlcd_name"]/a/@href')[0]
        reg = re.compile(r'loupan/(.*)\.htm')
        id = reg.findall(id_url)[0]
        name: str = li.xpath('.//div[@class="nlcd_name"]/a/text()')[0].strip()
        prices: list = li.xpath('.//div[@class="nhouse_price"]/span/text()')
        img_url: str = 'https:' + li.xpath(
            './/div[@class="nlc_img"]//img[1]/@src')[0]
        map_url: str = li.xpath('.//div[@class="address"]/a/@href')[0]
        phone: list = li.xpath('.//div[@class="tel"]/p/text()')
        lat, lon = get_position_by(map_url)
        # 数据合理则添加至列表
        if prices and prices[0] != '价格待定':
            price: str = prices[0]
            building = BuildingArea(
                id,
                name,
                price,
                img_url,
                map_url,
                phone,
                lat,
                lon,
            )
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
            get_building_area(BuildingAreaConstance.base_url + next_page[-1],
                              area)


@retry()
def get_position_by(map_url: str) -> tuple[str, str]:
    '''
    根据 `map_url` 获取经纬度，例：
    ``` python
    lat, lon = get_position_by('https://nc.newhouse.fang.com/loupan/2310201034.htm#detail_map')
    print(lat, lon) # 28.6836542 115.8583358
    ```
    '''
    print(f'> 正在获取 {map_url}')
    res: str = requests.get(map_url, timeout=None).text
    iframe = etree.HTML(res).xpath('//*[@id="iframe_map"]')
    if not iframe:
        return 'None', 'None'
    iframe_url: str = iframe[0].attrib['src']
    res: str = requests.get(f'https:{iframe_url}', timeout=None).text
    script: etree._Element = etree.HTML(res).xpath('/html/body/script[4]')[0]
    reg = re.compile(r'_vars.cityx = "(.*)";[\s\S]*_vars.cityy = "(.*)"')
    longitude, latitude = reg.findall(script.text)[0]
    return latitude, longitude


if __name__ == '__main__':
    get_building_areas()
