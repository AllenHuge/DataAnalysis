'''
功能：分析时期内每日股票涨/跌比例区间分布情况
作者：zxhu
日期：2020.02.27
'''

from flask_restful import reqparse, abort, Resource, Api
from logging.handlers import RotatingFileHandler
from common.db_operation import mysql_login
import logging

# 日志配置
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("create_docx.log",
                              encoding="utf-8",
                              maxBytes=10*1024*1024,
                              backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s-%(funcName)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)
logger.addHandler(console)


#获取每日涨跌幅信息
def getUpDownDistr(start_date,end_date):
    sql = '''
    SELECT
				trade_date
				,total_num_day
				,up_num_day
				,up_num_day*100/NULLIF(total_num_day,0) as up_ratio_day
				,FLOOR(up_ratio_day/5)*5 as up_ratio_day_2
				,stay_num_day
				,stay_num_day*100/NULLIF(total_num_day,0) as stay_ratio_day
				,down_num_day
				,down_num_day*100/NULLIF(total_num_day,0) as down_ratio_day
    FROM		(
	SELECT a.trade_date
					,COUNT(a.stock_code) AS total_num_day
					,SUM(CASE WHEN a.pct_chg > 0 THEN 1 ELSE 0 END) AS up_num_day
					,SUM(CASE WHEN a.pct_chg = 0 THEN 1 ELSE 0 END) AS stay_num_day
					,SUM(CASE WHEN a.pct_chg < 0 THEN 1 ELSE 0 END) AS down_num_day
	FROM	ext_data_stock.stock_quotation_info a
	WHERE	a.trade_status = '1' and trade_date = '20200226'
	GROUP BY a.trade_date
) t
    '''


