'''
render.py
'''

from pyecharts import charts, options
from get_building_areas import Constance, read_json_file_as_list

if __name__ == '__main__':

    geo = charts.Geo(init_opts=options.InitOpts(
        page_title='南昌楼市数据',
        is_horizontal_center=True,
        width='100%',
        height='958px',
        theme='halloween',
    ))
    geo.set_global_opts(title_opts=options.TitleOpts(
        title='南昌楼市数据',
        pos_left='50%',
        pos_top='20px',
        text_align='center',
        title_textstyle_opts=options.TextStyleOpts(font_size='32px'),
    ))
    geo.add_schema(maptype='南昌')

    for area in Constance.areas:
        data = read_json_file_as_list(f'./building_area/{area}.json')
        for item in data:
            name = item['name']
            latitude = float(item['latitude'])
            longitude = float(item['longitude'])
            geo.add_coordinate(name, longitude, latitude)
    geo.render()
