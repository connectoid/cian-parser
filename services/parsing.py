import requests

from services.tools import (get_datetime, get_title, create_offer, create_request, 
                            save_json, load_json)
from config.config import cookies, headers


def get_city_id(city):
    params = {
        'section_type': '1',
    }

    response = requests.get(f'https://{city}.cian.ru/cian-api/site/v1/adfox/home/', params=params, cookies=cookies, headers=headers)
    return response.json()['data']['params']['puid36']  


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
        offer = create_offer(offer_id, title, url, added_datetime, description_short,
                             description, address, phone, price, total_area, rooms_count, floor, floor_count)
        offers.append(offer)
    return offers


def get_offers(city, beds_count, rooms_count, date_gte, date_lt, pages):
    city_id = get_city_id(city)
    offers_json = []
    flats_count = 1

    for page in range(1, pages + 1):
        print(f'Page {page}')
        json_data = create_request(city_id, beds_count, rooms_count, date_gte, date_lt, page)

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