'''
utils.py
便捷方法
'''

import json
from math import asin, cos, fabs, radians, sin, sqrt


def read_json_file_as_list(path) -> list[dict]:
    '''
    将 json 文件读取为 list
    '''
    lst: list[dict] = []
    with open(path, 'r+', encoding='utf-8') as f:
        lst = json.loads(f.read())
    return lst


def hav(theta):
    '''
    ```markdown
    $$
    sin^2(\\frac{\\theta}{2})
    $$
    ```
    '''
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0: str, lng0: str, lat1: str, lng1: str):
    '''
    用 haversine 公式计算球面两点间的距离
    经纬度转换成弧度
    '''
    lat0 = radians(float(lat0))
    lat1 = radians(float(lat1))
    lng0 = radians(float(lng0))
    lng1 = radians(float(lng1))
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * 6371.137 * asin(sqrt(h))  # km
    return distance
