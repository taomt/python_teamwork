'''
render.py
'''

from pyecharts import charts, options
from get_building_areas import Constance, read_json_file_as_list

if __name__ == '__main__':

    geo = charts.Geo().add_schema(maptype='南昌')
    geo.set_global_opts(
        title_opts=options.TitleOpts(title="地理位置展示"),
        visualmap_opts=options.VisualMapOpts(max_=200),
    )

    for area in Constance.areas:
        data = read_json_file_as_list(f'./building_area/{area}.json')
        for item in data:
            name = item['name']
            latitude = float(item['latitude'])
            longitude = float(item['longitude'])
            tooltip_content = f"名称: {name}<br/>价格: {item['price']}<br/>电话: {', '.join(item['phone'])}"
            geo.add_coordinate(name, longitude, latitude)
    geo.render()
