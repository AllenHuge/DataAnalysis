import os
import numpy as np
import pandas as pd

from common.db_operation import mysql_login, df2mysql

datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_set/')
dataname = os.path.join(datapath, 'data_000001_2010-2019.xlsx')

df = pd.read_excel(dataname)
df['DateTime'] = pd.to_datetime(df['DateTime'],format="%Y-%m-%d")
# print(df['DateTime'])

#数据插入mysql数据库
df2mysql(df=df
         ,schema_name='ext_data_stock'
         ,table_name='stock_quotation_his'
         ,if_exists='replace'
         )