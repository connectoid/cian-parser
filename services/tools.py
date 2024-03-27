import json
from datetime import datetime


OUT_DATA_FOLDER = 'out_data'


def create_request(city_id, beds_count, rooms_count, date_gte, date_lt, page):
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
                'room': {
                'type': 'terms',
                'value': [
                    rooms_count,
                ],
            },
                'page': {
                'type': 'term',
                'value': page,
            },
            'dates': {
                'type': 'date_range',
                'value': {
                    'gte': f'{date_gte}',
                    'lt': f'{date_lt}',
                },
            },
            'beds_count': {
                'type': 'range',
                'value': {
                    'gte': beds_count,
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
    pretty_datetime = datetime.fromtimestamp(datetime_stamp)
    pretty_datetime = datetime.strftime(pretty_datetime, '%d.%m.%Y %H:%M')
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


def create_offer(id, title, url, added_datetime, description_short,
                 description, address, phone, price, total_area, rooms_count, floor, floor_count):
    offer = {}
    offer['offer_id'] = id
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
    return offer


def save_json(response, file='data-cian.json'):
    with open(f'{OUT_DATA_FOLDER}/{file}', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False)


def load_json(file='data-cian.json'):
    with open(f'{OUT_DATA_FOLDER}/{file}', 'r', encoding='utf-8') as f:
        text = json.load(f)
        return text

