'''
功能：分析时期内每日股票涨/跌比例区间分布情况
作者：zxhu
日期：2020.02.27
'''

from flask_restful import reqparse, abort, Resource, Api
from flask import Flask,jsonify,request
from logging.handlers import RotatingFileHandler
from common.db_operation import mysql_login
import pandas as pd
import math
import logging
from pyecharts import options as opts
from pyecharts.charts import Bar
import time
import uuid

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
def getUpDownDistr(start_date,end_date,flag='up'):
    sql = '''
    SELECT
				trade_date
				,total_num_day
				,up_num_day
				,up_num_day*100/NULLIF(total_num_day,0) as up_ratio_day
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
	    WHERE	a.trade_status = '1' 
	    and     a.trade_date >= '{0}'
	    and     a.trade_date <= '{1}'
	    GROUP BY a.trade_date
    ) t
    '''.format(start_date, end_date)

    conn = mysql_login()
    upDownNumDay = pd.read_sql(
                                sql = sql,
                                con = conn
                            )
    conn.close()

    upDownNumDay['up_ratio_day_int'] = upDownNumDay['up_ratio_day'].apply(lambda x:(math.floor(x/5)+1)*5)
    up_res = pd.DataFrame(upDownNumDay.groupby(by=['up_ratio_day_int']).size(),columns=['num'])

    upDownNumDay['down_ratio_day_int'] = upDownNumDay['down_ratio_day'].apply(lambda x:(math.floor(x/5)+1)*5)
    down_res = pd.DataFrame(upDownNumDay.groupby(by=['down_ratio_day_int']).size(),columns=['num'])

    if flag == 'up':
        res = up_res
    else:
        res = down_res

    return res

def getDistrPic(df):
    data_x = list(df.index)
    data_y = list(df['num'])

    c = (
        Bar()
        .add_xaxis(data_x)
        .add_yaxis("up-distribution", data_y)
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

class Analy_up_down(Resource):
    def post(self):
        start_time = time.time()
        flowid = str(uuid.uuid1())  #查询唯一uid
        result = {
                    'success':True,
                    'code':0,
                    'message':None,
                    'flowId':flowid,
                    'time':0,
                    'value':{'flowId':str(flowid),'ch_colnames':[],'rows':[]}
                  }
        getDicts_raw = request.get_json()
        start_date = getDicts_raw.get('start_date')
        end_date = getDicts_raw.get('end_date')
        upDown_flag = getDicts_raw.get('upDown_flag')
        data = getUpDownDistr(start_date, end_date, upDown_flag)
        ch_colnames = ['占比','天数']
        data.insert(0,'ratio',data.index)
        data2=data.to_dict(orient='split')
        rows = data2['data']
        pic = getDistrPic(data)
        pic.render('D:\\PyProjects\\DataAnalysis\\result_set\\down-distribution.html')
        end_time = time.time()
        result.update({
            'success': True,
            'code': 200,
            'message': '查询绘图成功',
            'flowId': flowid,
            'time': (end_time - start_time)*1000,
            'value': {'flowId': str(flowid), 'ch_colnames': ch_colnames, 'rows': rows}
        })
        return jsonify(result)





if __name__ == '__main__':
    df = getUpDownDistr('2006-01-01','2020-02-27','up')
    # print(res[['up_ratio_day_int','trade_date']])
    # print(getDistrPic(df))
    pic = getDistrPic(df)
    pic.render('../result_set/down-distribution.html')



