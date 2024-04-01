import json
import requests
import datetime
from transliterate import translit, get_available_language_codes

from config.config import cookies, headers, logger

OUT_DATA_FOLDER = 'out_data'

def get_city_id(city):
    print(city)
    city = translit(city, 'ru', reversed=True)
    print(city)
    params = {
        'section_type': '1',
    }
    try:
        response = requests.get(f'https://{city}.cian.ru/cian-api/site/v1/adfox/home/', params=params, cookies=cookies, headers=headers)
        city_id = response.json()['data']['params']['puid36']  
        return city_id
    except Exception as e:
        logger.error(f'Ошибка запроса города: {e}')
        return 1



def create_request(prefs):

    city_id = get_city_id(prefs['city'])
    print(city_id)


    """
    'show_hotels': {
            'type': 'term',
            'value': True,
        },
    """
    json_data = {
        'jsonQuery': {
            '_type': 'flatrent',
            'engine_version': {
                'type': 'term',
                'value': 2,
            },
            'region': {
                'type': 'terms',
                'value': [
                    f'{city_id}',
                ],
            },
            'for_day': {
                'type': 'term',
                'value': '1',
            },
                'show_hotels': {
                'type': 'term',
                'value': prefs['is_hotel'],
            },
                'room': {
                'type': 'terms',
                'value': [
                    prefs['rooms_count'],
                ],
            },
                'page': {
                'type': 'term',
                'value': 1,
            },
            'dates': {
                'type': 'date_range',
                'value': {
                    'gte': prefs['date_gte'],
                    'lt': prefs['date_lt'],
                },
            },
            'beds_count': {
                'type': 'range',
                'value': {
                    'gte': prefs['beds_count'],
                },
            },
            'sort': {
                'type': 'term',
                'value': 'creation_date_desc',
        },
        },
    }

    return json_data


def get_datetime(datetime_stamp):
    pretty_datetime = datetime.datetime.fromtimestamp(datetime_stamp)
    pretty_datetime = datetime.datetime.strftime(pretty_datetime, '%d.%m.%Y %H:%M')
    return pretty_datetime


def get_title(title, rooms_count, total_area, floor, floor_count):
    if rooms_count:
        sub_title = f'{rooms_count}-комн. квартира, {total_area} кв. м, {floor}/{floor_count} этаж'
    else:
        sub_title = f'Студия, {total_area} кв. м, {floor}/{floor_count} этаж'
    if not title:
        title = sub_title
    else:
        title = f'{title}, {sub_title}'
    return title


def create_offer(offer_id, title, url, added_datetime, description_short,
                 description, address, phone, price, total_area, rooms_count, 
                 floor, floor_count, photo_mini, photos):
    offer = {}
    offer['offer_id'] = offer_id
    offer['title'] = title
    offer['url'] = url
    offer['added_datetime'] = added_datetime
    offer['description'] = description
    # offer['description'] = ''
    offer['description_short'] = description_short
    offer['address'] = address
    offer['phone'] = phone
    offer['price'] = price
    offer['area'] = total_area
    offer['rooms_count'] = rooms_count
    offer['floor'] = floor
    offer['floor_count'] = floor_count
    offer['photo_mini'] = photo_mini
    offer['photos'] = photos
    return offer


def save_json(response, file='data-cian.json'):
    with open(f'{OUT_DATA_FOLDER}/{file}', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False)


def load_json(file='data-cian.json'):
    with open(f'{OUT_DATA_FOLDER}/{file}', 'r', encoding='utf-8') as f:
        text = json.load(f)
        return text


def check_city(city):
    if isinstance(city, str):
        city = city.lower()
        if (get_city_id(city) == 1 and city != 'moskva'):
            return False
    return True


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
        if validate(new_date):
            now = datetime.datetime.now()
            date = datetime.datetime.strptime(date, '%d.%m.%Y')
            if date < now:
                 logger.warning('Дата из прошлого')
                 return False
            else:
                 logger.info('Дата указана правильно')
                 return True
            return True
        else:
             logger.warning('Формат дата указан правильно, но эта дата не существует')
             return False
    except:
         logger.warning('Неправильный формат даты')
         return False


def check_date_lt(date, date_gte):
    try:
        days_delta = int(date)
        date_gte = datetime.datetime.strptime(date_gte, '%d.%m.%Y')
        date_lt = date_gte + datetime.timedelta(days=days_delta)
        date_lt = date_lt.strftime('%d.%m.%Y')
        logger.info(f'Даты выезда посчитана как {date_lt}')
        return date_lt
    except:
        logger.info('Дата выезда введена не числом дней')
        if check_date_gte(date):
            date_lt = datetime.datetime.strptime(date, '%d.%m.%Y')
            date_gte = datetime.datetime.strptime(date_gte, '%d.%m.%Y')
            if date_lt > date_gte:
                return date
            else:
                return False
        else:
            return False



def check_is_hotel_answer(answer):
    try:
        num = int(answer)
        if 0 <= num < 2:
            return True
        return False
    except:
        return False
    

def check_int_answer(answer):
    try:
        num = int(answer)
        return True
    except:
        return False
