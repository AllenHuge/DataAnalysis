import pandas as pd
import baostock as bstk
import sqlalchemy
import datetime
from common.db_operation import mysql_login, df2mysql

def getStockCode(stockCode = None):
    # mysql登录
    conn = mysql_login()

    # sql脚本
    if stockCode == None:
        sql = '''
        select stock_code, stock_name from ext_data_stock.stock_base_info;
        '''
    else:
        sql = '''
        select stock_code, stock_name from ext_data_stock.stock_base_info where stock_code ='{}' ;
        '''.format(stockCode)

    # pandas查询
    df = pd.read_sql(sql=sql, con=conn)
    conn.close()
    return df

def getStockQuot(start_date, end_date, stockCode,):
    stock_list = getStockCode(stockCode)

    #### 登陆系统 ####
    lg = bstk.login()
    # 显示登陆返回信息
    print('login respond  error_msg:' + lg.error_msg)
    #### 获取沪深A股历史K线数据 ####
    data_list = []
    for stock_code in stock_list['stock_code']:
        rs = bstk.query_history_k_data_plus(stock_code,
                                      "date,code,open,high,low,close,preclose,volume,amount,pctChg,adjustflag,turn,tradestatus,isST",
                                      start_date=start_date,
                                      end_date=end_date,
                                      frequency="d",
                                            )

        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.columns = [
        'trade_date',
        'stock_code',
        'open_price',
        'high_price',
        'low_price',
        'close_price',
        'pre_close_price',
        'trade_vol',
        'trade_amt',
        'pct_chg',
        'adjust_flag',
        'turn',
        'trade_status',
        'is_st',
    ]
    df = pd.merge(result, stock_list, on='stock_code', how='left')
    df_stock_name = df.pop('stock_name')
    df.insert(2, 'stock_name', df_stock_name)

    dtype = {
        'trade_date':sqlalchemy.types.DateTime(),
        'stock_code':sqlalchemy.types.NVARCHAR(length=20),
        'stock_name':sqlalchemy.types.NVARCHAR(length=20),
        'open_price':sqlalchemy.types.Numeric(20,2),
        'high_price':sqlalchemy.types.Numeric(20,2),
        'low_price':sqlalchemy.types.Numeric(20,2),
        'close_price':sqlalchemy.types.Numeric(20,2),
        'pre_close_price':sqlalchemy.types.Numeric(20,2),
        'trade_vol':sqlalchemy.types.Numeric(20,0),
        'trade_amt':sqlalchemy.types.Numeric(20,0),
        'pct_chg':sqlalchemy.types.NVARCHAR(length=20),
        'adjust_flag':sqlalchemy.types.NVARCHAR(length=10),
        'turn':sqlalchemy.types.NVARCHAR(length=20),
        'trade_status':sqlalchemy.types.NVARCHAR(length=10),
        'is_st':sqlalchemy.types.NVARCHAR(length=10),
    }

    ## 结果集插入mysql ####
    df2mysql(df=df
             , schema_name='ext_data_stock'
             , table_name='stock_quotation_info'
             , if_exists='append'
             , chunksize=5000
             , dtype=dtype
             , index=False
             )

    #### 登出系统 ####
    bstk.logout()
    return len(df)


def getIndexQuot(start_date, end_date, index_dict = {},):
    #### 登陆系统 ####
    lg = bstk.login()
    # 显示登陆返回信息
    print('login respond  error_msg:' + lg.error_msg)
    #### 获取沪深A股历史K线数据 ####
    data_list = []
    for stock_code in index_dict.keys():
        rs = bstk.query_history_k_data_plus(stock_code,
                                            "date,code,open,high,low,close,preclose,volume,amount,pctChg",
                                            start_date=start_date,
                                            end_date=end_date,
                                            frequency="d",
                                            adjustflag="3"
                                            )

        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.columns = [
        'trade_date',
        'index_code',
        'open_price',
        'high_price',
        'low_price',
        'close_price',
        'pre_close_price',
        'trade_vol',
        'trade_amt',
        'pct_chg',
    ]

    index_df = pd.DataFrame({'index_code': list(index_dict.keys()),
                             'index_name': list(index_dict.values())})
    df = pd.merge(result, index_df, left_on='index_code', right_on='index_code', how='left')
    df_stock_name = df.pop('index_name')
    df.insert(2, 'index_name', df_stock_name)

    dtype = {
        'trade_date': sqlalchemy.types.DateTime(),
        'index_code': sqlalchemy.types.NVARCHAR(length=20),
        'index_name': sqlalchemy.types.NVARCHAR(length=20),
        'open_price': sqlalchemy.types.Numeric(20, 3),
        'high_price': sqlalchemy.types.Numeric(20, 3),
        'low_price': sqlalchemy.types.Numeric(20, 3),
        'close_price': sqlalchemy.types.Numeric(20, 3),
        'pre_close_price': sqlalchemy.types.Numeric(20, 3),
        'trade_vol': sqlalchemy.types.Numeric(20, 0),
        'trade_amt': sqlalchemy.types.Numeric(20, 4),
        'pct_chg': sqlalchemy.types.NVARCHAR(length=20),
    }

    ## 结果集插入mysql ####
    df2mysql(df=df
             , schema_name='ext_data_stock'
             , table_name='index_quotation_info'
             , if_exists='append'
             , chunksize=5000
             , dtype=dtype
             , index=False
             )

    #### 登出系统 ####
    bstk.logout()
    return len(df)



if __name__ == "__main__":
    ## 获取个股日K数据
    # res = getStockQuot('2006-01-01', '2020-12-31', None)
    # # res = getStockQuot('2019-01-01','2020-12-31',None)
    # # res.to_csv('../result_set/quotation.csv',encoding='gbk')
    # print(res)

    ##获取指数日K数据
    # index_dict = {
    #                 'sh.000001':'上证综指',
    #                 'sh.000016':'上证50',
    #                 'sh.000300':'沪深300',
    #                 'sh.000905':'中证500',
    #                 }
    # res = getIndexQuot('2006-01-01', '2020-12-31', index_dict=index_dict)
    # print(res)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    print(current_date)

