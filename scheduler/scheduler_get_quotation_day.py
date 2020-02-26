from apscheduler.schedulers.blocking import BlockingScheduler
from stock_sh.get_quotation import main as getQuotMain

def getQuotJob():
    sched = BlockingScheduler()
    sched.add_job(getQuotMain, 'cron' ,day_of_week='1-5', hour=18, minute=0, second=0)
    sched.start()