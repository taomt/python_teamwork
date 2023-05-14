"""
nanchang_windy.py
南昌，妖风。
"""

import os
import re
import json
import datetime
import requests
from retry import retry  # 使用 `retry` 注释自动在错误时重试


class DayWind:
    """
    某一天的风力风向
    """

    date: str  # 日期，格式为 20110101
    day_time: str  # 白天的风力风向
    night_time: str  # 晚上的风力风向

    @retry()
    def __init__(self, date: str, with_save: bool) -> None:
        """
        传入参数 date 如 20110101 获取
        """
        self.date = date

        if with_save:
            print(f'> 正在获取 {date} 的数据')
            res = requests.get(
                url=f'http://tianqihoubao.com/lishi/nanchang/{date}.html',
                timeout=30,
            )
            match: tuple = re.findall(
                r'风力风向</b>[\s\S]*?<td>(.*)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?</tr>',
                res.text,
                re.MULTILINE,
            )[0]
            self.day_time = match[0]
            self.night_time = match[1]
            dates: list[dict] = read_json_as_day_winds_dict()
            with open(JSON_PATH, 'w+', encoding='utf-8') as f:
                dates.append(self.__dict__)
                f.write(json.dumps(dates, indent=2, ensure_ascii=False))
            print(f'> 追加 {self} 完毕')

    @retry()
    def __str__(self) -> str:
        return self.__dict__.__str__()


@retry()
def read_json_as_day_winds_dict() -> list[dict]:
    """
    读取 json 文件的数据并将其转化为 DayWindy 的 dict 列表
    """
    dates: list[dict] = []
    with open(JSON_PATH, 'r+', encoding='utf-8') as f:
        dates = json.loads(f.read())
    return dates


@retry()
def get_day_winds():
    """
    拉取所有天白天、夜晚的风力风向
    """
    os.system('cls')

    if not os.path.exists(JSON_PATH):
        print(f'> {JSON_PATH} 文件不存在，创建空的 json 文件')
        with open(JSON_PATH, 'w+', encoding='utf-8') as f:
            f.write('[]')

    dates: list[dict] = read_json_as_day_winds_dict()

    start: datetime = datetime.datetime.strptime('20110101', '%Y%m%d')
    end: datetime = datetime.datetime.now()
    day_winds: list[DayWind] = []
    start += datetime.timedelta(days=len(dates))
    for date in dates:
        day_wind = DayWind(date=date['date'], with_save=False)
        day_wind.__dict__ = date
        print(f'> 已读取历史记录 {day_wind.__dict__}')
        day_winds.append(day_wind)

    while start < end:
        day_winds.append(DayWind(start.strftime('%Y%m%d'), with_save=True))
        start += datetime.timedelta(days=1)


if __name__ == '__main__':
    JSON_PATH = './day_winds.json'
    get_day_winds()
