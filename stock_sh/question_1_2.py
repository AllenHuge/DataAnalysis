import dbutils
import pandas as pd
from contextlib import closing

#sql脚本取行情数据（交易日期、开盘价、收盘价、最高价、最低价、成交金额）
sql = '''
    SELECT  trade_date
            ,open_price
            ,curr_price
            ,high_price
            ,low_price
            ,trade_amt
    FROM    pd_data.sec_quotation_his
    WHERE   trade_date BETWEEN '20190830' AND '20190930'
    AND     sec_code = '600000'
    ;
'''

#pandas读取行情数据
with closing(dbutils.getConn("pg_test")) as conn:
    df_pufa = pd.read_sql(sql = sql, con = conn)

#从df_pufa中取交易日期、开盘价、收盘价、最高价和最低价画出日K线


#从df_pufa中取交易日期、成交金额画出成交金额折线图


