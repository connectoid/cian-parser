import requests
from pprint import pprint
import json

import pandas

import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?page=1&sort=popular&xsubject=3274&fbrand=28928%3B27445',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


OUT_DATA_FOLDER = 'wb_out'

def save_json(response, file='data-cian.json'):
    with open(f'{OUT_DATA_FOLDER}/{file}', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False)


def load_json(file='data-cian.json'):
    with open(f'{OUT_DATA_FOLDER}/{file}', 'r', encoding='utf-8') as f:
        text = json.load(f)
        return text

pages = 10
items_list = []

for page in range(1, pages + 1):
    url = f'https://catalog.wb.ru/catalog/electronic15/v2/catalog?appType=1&cat=60807&curr=rub&dest=-1257786&fbrand=28928;27445&page={page}&sort=popular&spp=30&xsubject=3274'

    response = requests.get(url=url, headers=headers)
    json_data = response.json()
    save_json(json_data)

    json_data = load_json()
    for item in json_data['data']['products']:
        thing = {}
        thing['name'] = item['name']
        thing['price'] = item['sizes'][0]['price']['total'] // 100
        print(thing)
        items_list.append(thing)

save_json(items_list, file='things.json')
pandas.read_json("wb_out/things.json").to_excel("wb_out/things.xlsx")