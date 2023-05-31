import requests
from lxml import etree
import os
import json


def get_building_area(url1, area1) -> None:
    res_text = requests.get(url1, headers=headers).text

    tree = etree.HTML(res_text)
    li_list = tree.xpath('//div[@id="newhouse_loupan_list"]/ul/li')

    building_path = f"./building_area/{area1}.json"
    buildings: list[dict] = read_json_as_building_area(building_path)
    for li in li_list:
        name: str = li.xpath('.//div[@class="nlcd_name"]/a/text()')[0].strip()
        prices: list = li.xpath('.//div[@class="nhouse_price"]/span/text()')
        if prices and prices[0] != '价格待定':
            price: str = prices[0]
            building = BuildingArea(name, price)
            buildings.append(building.__dict__)

    with open(building_path, "w", encoding="utf-8") as fi:
        fi.write(json.dumps(buildings, indent=2, ensure_ascii=False))
        print(f"写入信息--{area}")

    next_page = tree.xpath('//a[@class="next"]/@href')
    last_page = tree.xpath('//a[@class="last"]/@href')
    if next_page and last_page:
        next1: int = next_page[-1][-3:-1]
        last: int = last_page[-1][-3:-1]
        if last > next1:
            get_building_area(base_url + next_page[-1], area)


def read_json_as_building_area(path) -> list[dict]:
    with open(path, "r+", encoding="utf-8") as f:
        json_buildings = json.loads(f.read())
    return json_buildings


class BuildingArea:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return self.__dict__.__str__()


if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }
    base_url = "https://nc.newhouse.fang.com"
    areas: list[str] = ['honggutan', 'gaoxinkaifaqu', 'qingshanhu', 'xihu', 'nanchangxian', 'donghu', 'jingkaiqu',
                        'qingyunpu', 'wanli', 'xinjian', 'jinxian']
    pages: list[str] = ['b91', 'b92']

    if not os.path.exists("./building_area"):
        os.mkdir("./building_area")
    for area in areas:
        with open(f"./building_area/{area}.json", "w", encoding="utf-8") as f:
            f.write("[]")
        url = base_url + "/house/s/" + area
        get_building_area(url, area)
