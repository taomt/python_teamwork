'''
render_schools.py
'''

import math
from pyecharts import charts, options as opts
from model_building_area import BuildingArea, BuildingAreaConstance, read_as_building_areas
from model_school import School
from utils import get_distance_hav, read_json_file_as_list


def get_value_of(building_area: BuildingArea, schools: list[School]) -> float:
    '''
    传入 building_area 和 schools 得到一个反映学校对该 building_area 价格影响程度的权值
    '''
    value: float = 0
    for school in schools:
        distance: float = get_distance_hav(
            building_area.latitude,
            building_area.longitude,
            school.latitude,
            school.longitude,
        )
        # 假定影响程度与距离符合正态分布
        v = math.exp(-distance**2 / 10)
        value += v
    print(f'{building_area.name}的价格为 {building_area.price} 权值为 {value:.2f}')
    return value


if __name__ == '__main__':
    data: list[list[float]] = []
    for area in BuildingAreaConstance.areas:
        for building_area in read_as_building_areas(
                f'./data/building_area/{area}.json'):
            data.append([
                building_area.price,
                get_value_of(
                    building_area,
                    [
                        School.from_json(dct) for dct in
                        read_json_file_as_list('./data/schools.json')
                    ],
                ),
            ])

    data.sort(key=lambda x: x[0])
    x_data = [d[0] for d in data]
    y_data = [d[1] for d in data]

    (charts.Scatter().add_xaxis(xaxis_data=x_data).add_yaxis(
        series_name="",
        y_axis=y_data,
        symbol_size=20,
        label_opts=opts.LabelOpts(is_show=False),
    ).set_series_opts().set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
    ).render("./output/basic_scatter_chart.html"))
