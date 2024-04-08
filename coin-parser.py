import requests
from bs4 import BeautifulSoup

url = 'https://www.coingecko.com/en/coins/polygon'


def get_coin_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(response)



get_coin_info(url)