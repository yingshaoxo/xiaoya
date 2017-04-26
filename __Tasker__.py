##import schedule
##import time
##
##def job():
##    print('ok')
##
##schedule.every(1).seconds.do(job)
##while True:
##    schedule.run_continuously()
##    time.sleep(3)
##    print('no')

from Plugins.Library import schedule
import datetime
import time

import telebot
from __Xiaoya__ import xiaoya

user_id = 'telegram'
directory = 'GaoKao'
TGx = xiaoya('xiaoya', 17, user_id, directory)

GROUP = -1001082405980
#GROUP = -178341019
TOKEN = '121899714:AAF3xShKMc52iV5yN93fiIjOH98ZXP1zcOc'
tb = telebot.TeleBot(TOKEN)


start_time = datetime.datetime(2017, 4, 26, 17)
work_days = 40 # all the day you got

work_time = datetime.timedelta(hours=work_days*24) 
end_time = start_time + work_time #deadline
print(end_time)

all_interval = work_time.total_seconds()

def job_interval_time():
    diff = end_time - datetime.datetime.now()
    now_interval = diff.total_seconds()

    left_num = TGx.left_num()
    left_day = int(now_interval / (60 * 60 * 24)) - 1
    
    today_left_seconds = ((end_time - datetime.timedelta(hours=left_day*24)) - datetime.datetime.now()).total_seconds()

    interval_t = ((left_day * (8 * 60 * 60))+today_left_seconds) // left_num
    
    #progress = str((1 - (now_interval/all_interval)) * 100)[:7] + '%'
    if interval_t < 0:
        tb.send_message(GROUP, 'Your schedule times up!')
        exit()
        
    return left_num, interval_t

def job():
    result = TGx.reply('fuck')
    if result != '':
        tb.send_message(GROUP, result)
    return ''

left_num, interval_t = job_interval_time()
tb.send_message(131513300, 'You still got {} pieces to read.'.format(left_num))
tb.send_message(131513300, 'Every {} seconds one piece.'.format(str(int(interval_t))))
schedule.every(interval_t).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)