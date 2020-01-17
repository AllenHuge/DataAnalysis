from WindPy import *

w.start()
import pandas as pd

assetList = ["000001.SH"]
fileds = "pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing"
startDate = "1990-01-01"
endDate = "2019-12-31"
dataImport = w.wsd(assetList, fileds, startDate, endDate, "")
# w.stop()
# type(dataImport) 类型是instance
# wsd是日期序列的wind导入函数，"close"是wind导入的指标名称
# 如果下载其他指标，“”内可以设置相应的参数，比如单位、币种等。
# 通过在wind右下角输入cg，获得wind数据下载代码生成器页面
dates = pd.to_datetime(dataImport.Times)
# time series data, 日期作为后面df的index
# 作为index时，日期格式统一一下
# 错误：df = pd.DataFrame(dataImport.Data, index = dates.strftime("%Y-%m-%d"), columns = assetList)
# 生成一个收盘价格的时间序列表格，行名称是日期，列名称是股票代码
# dataImport.data的表达方式：列是日期，资产是行，所以需要转置。要么在转置之后加上index和column。
# 要么在加上index和column之后再转置，但加的时候跟上面的不一样。

# 方法一：
df = pd.DataFrame(dataImport.Data).T
df.index = dates  # .strftime("%Y-%m-%d")
df.columns = fileds.split(",")
df['trade_date'] = df.index