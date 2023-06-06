'''
utils.py
便捷方法
'''

import json


def read_json_file_as_list(path) -> list[dict]:
    '''
  将 json 文件读取为 list
  '''
    lst: list[dict] = []
    with open(path, 'r+', encoding='utf-8') as f:
        lst = json.loads(f.read())
    return lst
