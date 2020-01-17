from pyecharts.charts import Line,Bar, Page,Kline,Grid
from pyecharts import options as opts
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot
from typing import List,Union
import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
# 不发出警告


# n日均线
def calculate_ma(day_count: int, d):
    result: List[Union[float, str]] = []
    for i in range(len(d)):
        if i < day_count:
            result.append("-")
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(d[i - j][1])
        result.append(abs(float("%.3f" % (sum_total / day_count))))
    return result


def kline_profession(data_period: pd.DataFrame) -> Grid:
    data_x = [x for x in data_period['DateTime'].apply(lambda x: x.strftime("%Y/%m/%d"))]
    data_v = [list(x) for x in data_period[['OPEN','CLOSE','LOW','HIGH']].values]
    data_volume = [x for x in data_period['VOLUME']]

    kline = (
        Kline()
        .add_xaxis(xaxis_data=data_x)
        .add_yaxis(
            series_name="上证综指日K",
            y_axis=data_v,
            itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="大盘走势图 ",
                subtitle="均线MA-n(n以2, 4, 6, 8为例)",
            ),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True,
                    areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            legend_opts=opts.LegendOpts(
                is_show=True,
                pos_top="top",
                pos_left="center"
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    xaxis_index=[0, 1],
                    range_start=0,
                    range_end=100,
                ),
                opts.DataZoomOpts(
                    is_show=True,
                    xaxis_index=[0, 1],
                    type_="slider",
                    pos_top="90%",
                    range_start=0,
                    range_end=100,
                ),
            ],
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color="rgba(245, 245, 245, 0.8)",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000"),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": "#ec0000"},
                    {"value": -1, "color": "#00da3c"},
                ],
            ),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777"),
            ),
            brush_opts=opts.BrushOpts(
                tool_box=["rect", "polygon", "keep", "clear"],
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX",
            ),
        )
    )

    line = (
        Line()
        .add_xaxis(xaxis_data=data_x)
        .add_yaxis(
            series_name="MA2",
            y_axis=calculate_ma(day_count=2, d=data_v),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA4",
            y_axis=calculate_ma(day_count=4, d=data_v),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA6",
            y_axis=calculate_ma(day_count=6, d=data_v),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA8",
            y_axis=calculate_ma(day_count=8, d=data_v),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"),)
    )

    bar = (
        Bar()
        .add_xaxis(xaxis_data=data_x)
        .add_yaxis(
            series_name="Volume",
            yaxis_data=[
                # [i, data_volume[i]]
                [i, data_volume[i], 1 if data_v[i][0] < data_v[i][1] else -1]
                for i in range(len(data_v))
            ],
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            # itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c0"),
        )
        .set_global_opts(
            # title_opts=opts.TitleOpts(
            #     title='成交量/万股'
            # ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                grid_index=1,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                # name='成交量/万股',
                # name_location = 'end',
                grid_index=1,
                is_scale=True,
                split_number=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    # Kline And Line
    overlap_kline_line = kline.overlap(line)

    # Grid Overlap + Bar
    grid_chart = Grid()
    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
    )
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="70%", height="16%"
        ),
    )
    return grid_chart


if __name__ == "__main__":
    datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_set/')
    dataname = os.path.join(datapath, 'data_000001_2010-2019.xlsx')
    df = pd.read_excel(dataname)
    df = df[df['DateTime'] > '20190601']
    res = kline_profession(df)
    res.render('../result_set/kline_test.html')