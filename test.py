from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def job1():
    print('job1:{}'.format(datetime.now()))
def job2():
    print('job2:{}'.format(datetime.now()))
scheduler = BlockingScheduler()
# 每分執行job1
scheduler.add_job(job1, 'interval', minutes=1)
# 每3秒執行job2
scheduler.add_job(job2, 'interval', seconds=3)

scheduler.start()