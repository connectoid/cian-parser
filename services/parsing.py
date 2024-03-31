import requests

from services.tools import (get_datetime, get_title, create_offer, create_request, 
                            save_json, load_json)
from config.config import cookies, headers
from database.orm import add_flat

def get_json(json_data):
    response = requests.post(
        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response.json()


def get_offers_list(json):
    offers = []
    flats = json['data']['offersSerialized']
    for flat in flats:
        offer = {}
        offer_id = flat['id']
        try:
            title = flat['title']
        except:
            title = None
        url = flat['fullUrl']
        added_timestamp = flat['addedTimestamp']
        added_datetime = get_datetime(added_timestamp)
        address = flat['geo']['userInput']
        description = flat['description'].replace('\n', ' ').replace('\r', '')
        description_short = description[:75] + '..'
        price = flat['bargainTerms']['price']
        phone = flat['phones'][0]['number']
        floor = flat['floorNumber']
        floor_count = flat['building']['floorsCount']
        try:
            rooms_count = flat['roomsCount']
        except:
            rooms_count = None
        total_area = flat['totalArea']
        title = get_title(title, rooms_count, total_area, floor, floor_count)
        photos_list = flat['photos']
        photos_list = [photo['fullUrl'] for photo in photos_list]
        photos = ', '.join(photos_list)
        photo_mini = flat['photos'][0]['thumbnail2Url']
        offer = create_offer(offer_id, title, url, added_datetime, description_short,
                             description, address, phone, price, total_area, rooms_count,
                             floor, floor_count, photo_mini, photos)
        offers.append(offer)
    return offers


def get_offers(prefs):
    offers_json = []
    flats_count = 1

    json_data = create_request(prefs)

    offers_json_data = get_json(json_data)
    save_json(offers_json_data)
        
    offers_json_data = load_json()
    offers = get_offers_list(offers_json_data)

    for offer in offers:
        offers_json.append(offer)
        flats_count += 1

    save_json(offers_json, file='parsed_data.json')
    # pandas.read_json("parsed_data.json").to_excel("parsed_data.xlsx")
    return flats_count, offers_json


def parse(tg_id, prefs):
    count = 1
    new_offers = []
    flats_count, offers_json = get_offers(prefs)
    print(f'По запросу найдено {flats_count} квартир')

    for item in offers_json:
        if add_flat(tg_id, item):
            if item['price'] <= prefs['min_price']:
                new_offers.append(item)
                count += 1
                if count >= 5:
                    break
    
    return new_offers