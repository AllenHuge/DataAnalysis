from apscheduler.schedulers.blocking import BlockingScheduler
from stock_sh.get_quotation import main as getQuotMain
from stock_sh.get_stockInfo import main as getStockMain

def getQuotJob():
    sched = BlockingScheduler()
    sched.add_job(getStockMain, 'cron' ,day_of_week='1-5', hour=16, minute=30, second=0, coalesce=True, misfire_grace_time=3600,)
    sched.add_job(getQuotMain, 'cron' ,day_of_week='1-5', hour=18, minute=20, second=0, coalesce=True, misfire_grace_time=3600,)
    sched.start()