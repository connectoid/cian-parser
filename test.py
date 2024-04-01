import datetime

date = '02.03.2025'
date = 5
days_delta = int(date)
now = datetime.datetime.now()
date_lt = now + datetime.timedelta(days=days_delta)
date_lt = date_lt.strftime('%d.%m.%Y')
    
print(now, date_lt)