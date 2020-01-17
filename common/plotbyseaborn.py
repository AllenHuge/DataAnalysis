import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)

import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
# 不发出警告

# 获取股票数据
stock_name = '000001.SH'

datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_set/')
dataname = os.path.join(datapath, 'data_000001_2010-2019.xlsx')
df = pd.read_excel(dataname)
# df = df[df['DateTime'] > '20091201']

# ##线性图
# f, ax= plt.subplots(figsize = (7, 5))
# sns.lineplot(x="DateTime", y="CLOSE", data=df, ci=None, ax=ax)
#
# # 设置X轴标签的字体大小和字体颜色
# ax.set_xlabel('日期',fontsize=15,color='r', fontproperties=font_set)
#
# # 设置Y轴标签的字体大小和字体颜色
# ax.set_ylabel('close_price',fontsize=15, color='r')
#
# # # 设置Axes的标题
# ax.set_title(stock_name,fontsize=25, color='b')
#
# # 显示
# plt.show()

data = df[['OPEN','CLOSE','VOLUME','PCT_CHG','SWING']]
# ##热力图
# f, ax = plt.subplots(figsize = (7, 5))
# sns.heatmap(data.corr(),ax = ax)
# plt.show()

##相关性图
# f, ax = plt.subplots(figsize = (7, 5))
sns.clustermap(data.corr())
plt.show()