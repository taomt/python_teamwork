'''
history.py
'''

import json
import requests
from lxml import etree
from get_building_areas import BuildingArea, read_json_file_as_list, BuildingAreaConstance


def get_history_price(building_area: BuildingArea):
    '''
    根据 `BuildingArea.id` 获取历史价格
    ``` python
    print(building_area.id) # 2310200644
    get_history_price(building_area)
    ```
    '''
    # url =

    res = requests.get(
        url=
        f'{BuildingAreaConstance.base_url}/loupan/{building_area.id}/fangjia.htm',
        headers=BuildingAreaConstance.headers,
        timeout=None,
    )

    tree = etree.HTML(res.text)

    lis = tree.xpath("//div[@class='jglist']/ul/li")

    ti_lst = []
    price_lst = []
    for li in lis:

        ti = li.xpath("./span[1]/text()")[0]
        temp = ti.split('-')
        ti = temp[0] + '-' + temp[1]

        price = li.xpath("./span[2]/text()")[0]
        price = price.split("元")[0]
        ti_lst.append(ti)
        price_lst.append(price)

    mon_dic = {}
    for i in range(len(ti_lst)):
        if (ti_lst[i] in mon_dic) and price_lst[i].isalnum():
            mon_dic[ti_lst[i]] = int(
                (int(mon_dic[ti_lst[i]]) + int(price_lst[i])) / 2)
            # print(dic[ti_lst[i]])

        else:
            if price_lst[i].isalnum():
                mon_dic[f'{ti_lst[i]}'] = price_lst[i]

    # print(mon_dic)
    return mon_dic


def main():

    result_lst = []
    dic = {}
    for id in id_lst:
        print(id)
        dic['id'] = id
        mon_dic = get_history_price(id)
        dic['mon_price'] = mon_dic
        # print(id)
        result_lst.append(dic)

        # temp+=1
        # if temp ==20:
        #     break

    print(result_lst)
    with open('mon_price.json', 'w', encoding='utf-8') as f:
        json.dump(result_lst, f, ensure_ascii=False)


class HistoryPrice:
    '''
    历史价格
    '''
    year: str
    month: str
    price: str

    def __init__(
        self,
        year: str,
        month: str,
        price: str,
    ) -> None:
        self.year = year
        self.month = month
        self.price = price


if __name__ == '__main__':
    main()
