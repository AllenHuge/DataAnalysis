import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
# 不发出警告
from bokeh.io import output_notebook
output_notebook()
# 导入notebook绘图模块
from bokeh.plotting import figure,show,output_file

datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_set/')
dataname = os.path.join(datapath, 'data_000001_2010-2019.xlsx')
df = pd.read_excel(dataname)
# print(df)

# 画图
p = figure(plot_width=600,
           plot_height=400,
           x_axis_type='datetime',
           tools=['hover,box_select,box_zoom,reset,wheel_zoom,pan,save'],
           x_axis_label = '交易日期',
           y_axis_label = '每日收盘点位',
           title = '000001.SH日K图',
           title_location = 'above'
          )

p.line(df['DateTime'],df['CLOSE']
       ,line_color = 'red'
       ,line_alpha = 1
       # ,line_dash = 'dashed'
      )

output_file('../templates/000001SH.html')
show(p)