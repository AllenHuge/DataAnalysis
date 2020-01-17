from apscheduler.schedulers.blocking import BlockingScheduler
from common.commfunc import job
from common.create_docx import output_docx

# BlockingScheduler
sched = BlockingScheduler()
# Schedule job_function to be called every two hours,starts on 2010-10-10 at 9:30 and stops on 2014-06-15 at 11:00
# sched.add_job(job_function, 'interval', hours=0,seconds = 5, start_date='2010-10-10 09:30:00', end_date='2020-01-09 11:00:00')

sched.add_job(output_docx, 'cron' ,day_of_week='1-5', hour=17, minute=0, second=0)
# '''
# year (int|str) – 4-digit year
# month (int|str) – month (1-12)
# day (int|str) – day of the (1-31)
# week (int|str) – ISO week (1-53)
# day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
# hour (int|str) – hour (0-23)
# minute (int|str) – minute (0-59)
# econd (int|str) – second (0-59)
#
# start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
# end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
# timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
#
# *    any    Fire on every value
# */a    any    Fire every a values, starting from the minimum
# a-b    any    Fire on any value within the a-b range (a must be smaller than b)
# a-b/c    any    Fire every c values within the a-b range
# xth y    day    Fire on the x -th occurrence of weekday y within the month
# last x    day    Fire on the last occurrence of weekday x within the month
# last    day    Fire on the last day within the month
# x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
# '''
sched.start()

