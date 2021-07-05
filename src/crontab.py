# CRON TAB EXECUTABLE 
# WILL IMPLEMENT IN BASH

from crontab import CronTab

with CronTab(user='root') as cron:
    job = cron.new(command='python3 parser.py')
    job.minute.every(60)

print('cron.write() was just executed')
