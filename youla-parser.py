from pprint import pprint
import json
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup


url = 'https://youla.ru/kostroma/nedvijimost/arenda-kvartiri-posutochno/arenda-dvuhkomnatnoj-kvartiry-posutochno'


def get_scripts(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        scripts = soup.find_all('script')
        return scripts
    else:
        print('Request error')
        return None



scripts = get_scripts(url)
script = scripts[1]
data = script.text.split('window.__YOULA_STATE__ = ')[1].split('window.__YOULA_TEST__')[0].split(';')[0]
data = unquote(data)
json_data = json.loads(data)
with open('youla_data.json', 'w') as file:
    json.dump(json_data, file, ensure_ascii=False)
