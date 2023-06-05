'''
model_hospital.py
存储 get_hospitals.py 相关类与方法
'''


class HospitalConstance:
    '''
    存放常数信息
    '''
    # headers 信息
    headers: dict = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
    }
    # 根 url
    base_url: str = 'https://www.haodf.com/hospital/list-3601.html'


class Hospital:
    '''
    Hospital 类
    '''
    name: str
    latitude: str
    longitude: str

    def __init__(
        self,
        name: str,
        latitude: str,
        longitude: str,
    ) -> None:
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
