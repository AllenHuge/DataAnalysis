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
dataname = os.path.join(datapath, 'data_lt_star.xlsx')
df = pd.read_excel(dataname)

data = df[['拉抬打压幅度','主动成交占比', '成交占比','T-1日持有流通股']]
data['次数'] = df['次数']
sns.heatmap(data.corr())
plt.show()