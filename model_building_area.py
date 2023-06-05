'''
model_building_area.py
存储 get_building_areas.py 相关类与方法
'''

from kit import read_json_file_as_list


class BuildingArea:
    '''
    BuildingArea 类
    '''
    id: str
    name: str
    price: str
    img_url: str
    map_url: str
    phone: list
    latitude: str
    longitude: str

    def __init__(
        self,
        id: str,
        name: str,
        price: str,
        img_url: str,
        map_url: str,
        phone: list,
        latitude: str,
        longitude: str,
    ) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.img_url = img_url
        self.map_url = map_url
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_json(dct: dict):
        '''
        静态函数，将 `dct` 的 `json` 数据类型转为 BuildingAre
        '''
        return BuildingArea(
            dct['id'],
            dct['name'],
            dct['price'],
            dct['img_url'],
            dct['map_url'],
            dct['phone'],
            dct['latitude'],
            dct['longitude'],
        )

    def __str__(self) -> str:
        return self.__dict__.__str__()


class BuildingAreaConstance:
    '''
    存放常数信息
    '''
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


def read_as_building_areas(path: str) -> list[BuildingArea]:
    '''
    将 json 文件读取为 list[BuildingArea]
    '''
    buildings: list[dict] = read_json_file_as_list(path)
    building_areas: list[BuildingArea] = [
        BuildingArea.from_json(building) for building in buildings
    ]
    return building_areas
