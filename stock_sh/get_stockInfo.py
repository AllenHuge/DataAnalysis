import baostock as bstk
import pandas as pd
import numpy as np
from common.db_operation import df2mysql, mysql_login
import requests #python的http客户端
import re
import sqlalchemy
import datetime


def getHtml(page):
    start = (page - 1)*25
    end = page*25
    url = '''
    http://yunhq.sse.com.cn:32041//v1/sh1/list/exchange/equity?callback=jQuery1124023881100803018573_1582514431484&select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate%2Ccpxxsubtype%2Ccpxxprodusta&order=&begin='''\
          +str(start)\
          +'''&end='''\
          +str(end)+'''&_=1582514431493
    '''
    r = requests.get(url)
    pat = '''"list":\[(.*?)\]}'''
    data = re.compile(pat,re.S).findall(r.text)
    return data


def getOnePageStock(page):
    html = getHtml(page)
    pat = '''\[(.*?)\]'''
    data = re.compile(pat, re.S).findall(html[0])
    return [x.replace('''"''', "").split(',')[0] for x in data]


def getCode():
    page = 1
    stocks = getOnePageStock(page)
    # 自动爬取多页，并在结束时停止
    while True:
        page += 1
        if getHtml(page) != getHtml(page - 1):
            stocks.extend(getOnePageStock(page))
        else:
            break
    return stocks


def getStockInfo():
    # 登陆系统
    lg = bstk.login()
    # 显示登陆返回信息
    print('login respond  error_msg:'+lg.error_msg)
    # 获取证券基本资料
    data_list = []
    stock_list = getCode()
    for stock in stock_list:
        stock_code = stock
        rs = bstk.query_stock_basic(code="sh.{}".format(stock_code))
        # rs = bs.query_stock_basic(code_name="浦发银行")  # 支持模糊查询

        # 打印结果集
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 登出系统
    bstk.logout()
    df = result
    df.columns = ['stock_code','stock_name','ipo_date','out_date','stock_type','stock_status']
    df['out_date'] = result['out_date'].apply(lambda x: np.NaN if x=='' else x)

    return df

def insertCode():
    conn = mysql_login()
    sql = '''
    select * from ext_data_stock.stock_base_info;
    '''
    code_yest = pd.read_sql(sql=sql,con = conn)
    conn.close()
    codenum_yest = len(code_yest)

    code_curr = getStockInfo()
    codenum_curr = len(code_curr)

    # 股票基本信息插入mysql数据库
    dtype_dict ={
        "stock_code": sqlalchemy.types.NVARCHAR(length=10),
        "stock_name": sqlalchemy.types.NVARCHAR(length=10),
        "ipo_date": sqlalchemy.types.DateTime(),
        "out_date": sqlalchemy.types.DateTime(),
        "stock_type": sqlalchemy.types.NVARCHAR(length=5),
        "stock_status": sqlalchemy.types.NVARCHAR(length=5),
    }
    df2mysql(df=code_curr
             , schema_name='ext_data_stock'
             , table_name='stock_base_info'
             , if_exists='replace'
             , dtype=dtype_dict
             , index=True
             , chunksize=5000
             )
    return codenum_curr,codenum_yest

def main():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    codenum_curr, codenum_yest = insertCode()
    print("{0}，今日共{1}只上市股票,前一交易日共{2}只上市股票。".format(current_date,str(codenum_curr),str(codenum_yest)))



if __name__ == '__main__':
    main()