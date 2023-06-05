'''
school.py
'''

import re
import json
import requests

from model_school import SchoolConstance


def get_page_num():
    '''
    获取总页数
    '''
    params: dict = {
        'qt': 's',
        'c': '163',
        'wd': '南昌高中',
        'rn': '10',
        'pn': '7',
        'ie': 'utf-8',
        'oue': '1',
        'fromproduct': 'jsapi',
        'v': '2.1',
        'res': 'api',
    }

    res = requests.get(
        url=SchoolConstance.base_url,
        headers=SchoolConstance.headers,
        params=params,
        timeout=None,
    )
    # 转换为中文
    res_text = res.text.encode('utf-8').decode('unicode_escape')

    print(res_text)

    total = re.findall("'total':(.*?),", res_text)[0]
    # print(total)
    page_num = int(total) // 10
    if int(total) % 10 != 0:
        page_num += 1
    # print(page_num)
    return page_num


def save_data():
    '''
    保存数据
    '''
    page_num = get_page_num()
    name_lst = []
    for page in range(page_num):

        params = {
            'qt': 's',
            'c': '163',
            'wd': '南昌高中',
            'rn': '10',
            'pn': f'{page}',
            'ie': 'utf-8',
            'oue': '1',
            'fromproduct': 'jsapi',
            'v': '2.1',
            'res': 'api',
        }

        res = requests.get(
            url=SchoolConstance.base_url,
            headers=SchoolConstance.headers,
            params=params,
            timeout=None,
        )

        for i in res.content:
            try:
                name = i['ext']['detail_info']['name']
            except Exception as e:
                print(e)
                name = i['name']
            name_lst.append(name)

    with open('name.txt', 'w', encoding='utf-8') as f:
        for i in name_lst:
            f.write(i)
            f.write('\n')


def rename():
    '''
    去重
    '''
    with open('name.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
    # print(data)
    temp_lst = []
    for i in data:
        # print(repr(i.replace('\n', '')))
        print(i.replace('\n', ''))
        if not i.replace('\n', '') in temp_lst:
            temp_lst.append(i.replace('\n', ''))

    with open('rname.text', 'w', encoding='utf-8') as f:
        for i in temp_lst:
            f.write(i)
            f.write('\n')


def baiAI():
    with open('rname.text', 'r', encoding='utf-8') as f:
        names = f.readlines()
    json_lst = []
    dic = {}
    name_lst = []
    longitude = []
    latitude = []

    for i in names:
        name = i.replace('\n', '')

        # 接口地址
        url = 'https://api.map.baidu.com/geocoding/v3'

        # 此处填写你在控制台-应用管理-创建应用后获取的AK
        ak = 'NWqi2iGuW9mpd5CsOBA0hV3dsDq0f6GC'

        params = {
            'address': f'{name}',
            'output': 'json',
            'ak': ak,
        }

        res = requests.get(url=url, params=params, timeout=None)
        if res:
            print(res.json())

            name_lst.append(name)
            longitude.append(res.json()['result']['location']['lng'])
            latitude.append(res.json()['result']['location']['lat'])

    for i in range(len(name_lst)):
        dic['学校'] = name_lst[i]
        dic['经度'] = longitude[i]
        dic['维度'] = latitude[i]
        json_lst.append(dic)

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(json_lst, f, ensure_ascii=False)
    print(json_lst)


if __name__ == '__main__':
    baiAI()
