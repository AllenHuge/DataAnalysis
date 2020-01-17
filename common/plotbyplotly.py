import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
# 不发出警告
import random
import plotly.offline as po
import plotly.graph_objs as go
from pandas import datetime

# 获取股票数据
stock_name = '000001.SH'

datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_set/')
dataname = os.path.join(datapath, 'data_000001_2010-2019.xlsx')
df = pd.read_excel(dataname)
# df = df[df['DateTime'] > '20190101']
# print(df.dtypes)

trace = go.Candlestick(x=df['DateTime']
                       ,open=df['OPEN']
                       ,high=df['HIGH']
                       ,low=df['LOW']
                       ,close=df['CLOSE']
                       )
data = [trace]
layout = {
    'title': stock_name}
fig = dict(data=data, layout=layout)
po.plot(fig, filename='../templates/000001SH.html')
