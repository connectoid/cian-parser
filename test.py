import datetime

def validate(date_text):
        try:
            datetime.date.fromisoformat(date_text)
            return True
        except ValueError:
            return False
        

def check_date_gte(date):
    try:
        year = date.split('.')[-1]
        mounth = date.split('.')[1]
        day = date.split('.')[0]
        new_date = f'{year}-{mounth}-{day}'
        print(new_date)
        if validate(new_date):
            now = datetime.datetime.now()
            date = datetime.datetime.strptime(date, '%d.%m.%Y')
            print(now.date(), date.date())
            if date < now:
                 print('Дата из прошлого')
                 return False
            else:
                 print('Дата указана правильно')
                 return True
            return True
        else:
             print('Формат дата указан правильно, но эта дата не существует')
             return False
    except:
         print('Неправильный формат даты')
         return False
    

date = '31.03.2024'
check_date_gte(date)