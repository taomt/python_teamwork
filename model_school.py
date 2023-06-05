'''
model_school.py
存储 get_schools.py 相关类与方法
'''


class SchoolConstance:
    '''
    存放常数信息
    '''
    headers: dict = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    base_url: str = 'https://api.map.baidu.com'


class School:
    '''
    School 类
    '''
    name: str
    longitude: str
    latitude: str

    def __init__(
        self,
        name: str,
        longitude: str,
        latitude: str,
    ) -> None:
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
