import requests
from pprint import pprint

cookies = {
    'u': '2xt085cd.nrwk63.19sc3y2l2x800',
    'buyer_laas_location': '626470',
    '_ym_uid': '1678942044277874789',
    'cto_bundle': '14v6ol9SQmdWaFoyc0M1OHRvdFI5YzFjeDRibkdoMEpJJTJGbnl2ckxIZ0RRb3VJUmpkSkU2TFJ0a2pucG12MDl5bW5WV29zVDdyYkZOdTU0MW1EJTJCRjZLRWFLbkczQkQ0U0dDMzFYbURWUnBQSDhoVWJNRjZvRGJ2NFEzUnl4ZWJtVnRmQ0VCS28xV085QW1CZTBXR2hmYyUyQkM4c3clM0QlM0Q',
    'uxs_uid': 'b82235a0-c3b5-11ed-bbba-ab8b0dd58849',
    '_ga': 'GA1.1.400783223.1678942102',
    'adrcid': 'ABcrYNIRcOAWDAKlhFedJcA',
    'srv_id': 'F29i6Ojh7F7nnC-L.9QfbIH2lzNq38h1HQktFE6A-osrlBq5-8M82oWGnbHnfAsKkCLkCJKv_Gd4XafLib0mV.JvYlmC2_yWXX_1QQnQBduAJiTSIRfpO34J1Rb7NNL9s=.web',
    '_ym_d': '1707090148',
    '_gcl_au': '1.1.1689687010.1707090148',
    'gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN',
    'v': '1711572953',
    'dfp_group': '38',
    '_ym_visorc': 'b',
    '_ym_isad': '1',
    'buyer_location_id': '632490',
    'luri': 'kostroma',
    '__upin': '/1xhPppDUFD4uvSiUyziDw',
    'f': '5.0c4f4b6d233fb90636b4dd61b04726f1e50e2480c65fe234e50e2480c65fe234e50e2480c65fe2341929191c9a5cc7585284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b984dcacfe8ebe897bfa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa38e6a683f47425a8352c31daf983fa077a7b6c33f74d335c84df0fd22b85d35fee5ad4b32fbbc9d802c730c0109b9fbb963daedbf4968a60f63c1114aca04b6a0e28148569569b79c485c541e08d3214a1c5d8dc224db8902ebf3cb6fd35a0ac0df103df0c26013a28a353c4323c7a3aefcfb0a8b1110195aa81573a66b038ce3de19da9ed218fe23de19da9ed218fe29e05a03e27b662cf3740ddbb7a20c3778edd6a0f40cbfd87da3d420d6cca468c',
    'ft': '"VEVfB4c1PVYY0zFhoVpSPrNwfOCmyw9lbBTmD80jCoxdFL4L7du07mMhAgaeHzU3bn7izz9JOMee34uCaQEv5pv8Nc+sBUnzitTo08XRYJmnBa0yf6LIGMCb8z6LN+8yJJQNBil0IRKVIynN+Otn2PmPzxpSW1X9gIXT7PaqsKlmOlyu4DwbmbBh0CaZhabl"',
    'sx': 'H4sIAAAAAAAC%2F1TQQa7iMAyA4btkzSJOYjvmNkmcFGgLTFteOzz17iMWjNQLfPr1%2FxqbwDJS8RpcAQkaNUeWQEq5IkVz%2FjU%2F5mwcP5fo8R0zpjDeHn5d7AubdNvYDX%2FEnEw1Z2AAQkHn9pMhIirK1IQEKZBUztWLMtpSWOUr5%2Fu4Bvu3Df1lcTq9k6dHP2CTK%2BK1vx9kj34%2FGSbkUAskVqGaRMFKq7VBaYWtuq9cmToSOwvdlcfulvK6lBif2xR7O%2BlBDvhpjqGCNIIG2QWpTj%2B1XmKOJQUb%2Ft%2BgW1zbdX17wOgSPGXb%2BgGnYbvo%2FNLxKHPYT0aLMjO73ABrRPCMKqTswSZXlL5y%2BeF1vmJ7kV7qPHf31Dql4THdIAPgUY5%2B3%2F8FAAD%2F%2F%2Fq9ZqPDAQAA',
    '_mlocation': '621540',
    '_mlocation_mode': 'default',
    '_ga_M29JC28873': 'GS1.1.1711572996.3.1.1711573232.39.0.0',
}

headers = {
    'authority': 'm.avito.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    # 'cookie': 'u=2xt085cd.nrwk63.19sc3y2l2x800; buyer_laas_location=626470; _ym_uid=1678942044277874789; cto_bundle=14v6ol9SQmdWaFoyc0M1OHRvdFI5YzFjeDRibkdoMEpJJTJGbnl2ckxIZ0RRb3VJUmpkSkU2TFJ0a2pucG12MDl5bW5WV29zVDdyYkZOdTU0MW1EJTJCRjZLRWFLbkczQkQ0U0dDMzFYbURWUnBQSDhoVWJNRjZvRGJ2NFEzUnl4ZWJtVnRmQ0VCS28xV085QW1CZTBXR2hmYyUyQkM4c3clM0QlM0Q; uxs_uid=b82235a0-c3b5-11ed-bbba-ab8b0dd58849; _ga=GA1.1.400783223.1678942102; adrcid=ABcrYNIRcOAWDAKlhFedJcA; srv_id=F29i6Ojh7F7nnC-L.9QfbIH2lzNq38h1HQktFE6A-osrlBq5-8M82oWGnbHnfAsKkCLkCJKv_Gd4XafLib0mV.JvYlmC2_yWXX_1QQnQBduAJiTSIRfpO34J1Rb7NNL9s=.web; _ym_d=1707090148; _gcl_au=1.1.1689687010.1707090148; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; v=1711572953; dfp_group=38; _ym_visorc=b; _ym_isad=1; buyer_location_id=632490; luri=kostroma; __upin=/1xhPppDUFD4uvSiUyziDw; f=5.0c4f4b6d233fb90636b4dd61b04726f1e50e2480c65fe234e50e2480c65fe234e50e2480c65fe2341929191c9a5cc7585284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d5284c253a1c0cd7d0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b984dcacfe8ebe897bfa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa38e6a683f47425a8352c31daf983fa077a7b6c33f74d335c84df0fd22b85d35fee5ad4b32fbbc9d802c730c0109b9fbb963daedbf4968a60f63c1114aca04b6a0e28148569569b79c485c541e08d3214a1c5d8dc224db8902ebf3cb6fd35a0ac0df103df0c26013a28a353c4323c7a3aefcfb0a8b1110195aa81573a66b038ce3de19da9ed218fe23de19da9ed218fe29e05a03e27b662cf3740ddbb7a20c3778edd6a0f40cbfd87da3d420d6cca468c; ft="VEVfB4c1PVYY0zFhoVpSPrNwfOCmyw9lbBTmD80jCoxdFL4L7du07mMhAgaeHzU3bn7izz9JOMee34uCaQEv5pv8Nc+sBUnzitTo08XRYJmnBa0yf6LIGMCb8z6LN+8yJJQNBil0IRKVIynN+Otn2PmPzxpSW1X9gIXT7PaqsKlmOlyu4DwbmbBh0CaZhabl"; sx=H4sIAAAAAAAC%2F1TQQa7iMAyA4btkzSJOYjvmNkmcFGgLTFteOzz17iMWjNQLfPr1%2FxqbwDJS8RpcAQkaNUeWQEq5IkVz%2FjU%2F5mwcP5fo8R0zpjDeHn5d7AubdNvYDX%2FEnEw1Z2AAQkHn9pMhIirK1IQEKZBUztWLMtpSWOUr5%2Fu4Bvu3Df1lcTq9k6dHP2CTK%2BK1vx9kj34%2FGSbkUAskVqGaRMFKq7VBaYWtuq9cmToSOwvdlcfulvK6lBif2xR7O%2BlBDvhpjqGCNIIG2QWpTj%2B1XmKOJQUb%2Ft%2BgW1zbdX17wOgSPGXb%2BgGnYbvo%2FNLxKHPYT0aLMjO73ABrRPCMKqTswSZXlL5y%2BeF1vmJ7kV7qPHf31Dql4THdIAPgUY5%2B3%2F8FAAD%2F%2F%2Fq9ZqPDAQAA; _mlocation=621540; _mlocation_mode=default; _ga_M29JC28873=GS1.1.1711572996.3.1.1711573232.39.0.0',
    'referer': 'https://m.avito.ru/items/search?locationId=632490&localPriority=0&categoryId=24&params[201]=1060&params[504]=5257&params[2900-from]=2024-04-01&params[2900-to]=2024-04-08&params[123093]=3022415&presentationType=serp',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
    'x-laas-timezone': 'Asia/Kamchatka',
}

proxies = {
#    'http': 'socks5://ZGTxtv:gnttyS@194.67.214.57:9658',
#    'https': 'socks5://ZGTxtv:gnttyS@194.67.214.57:9658',
   'http': 'socks5://wGJX8p:unz2MG@88.218.72.74:9060',
   'https': 'socks5://wGJX8p:unz2MG@88.218.72.74:9060',
}



import ssl
from requests.adapters import HTTPAdapter

class SSLAdapter(HTTPAdapter):

    def init_poolmanager(self, *args, **kwargs):
 
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        kwargs["ssl_context"] = ssl_context
        return super().init_poolmanager(*args, **kwargs)

url = 'https://m.avito.ru/api/11/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=632490&localPriority=0&categoryId=24&params[201]=1060&params[504]=5257&params[2900-from]=2024-04-01&params[2900-to]=2024-04-08&params[123093]=3022415&page=1&lastStamp=1711573200&display=list&limit=25&presentationType=serp'

s = requests.Session()
s.mount('https://', SSLAdapter())

r=s.post(url, cookies=cookies, headers=headers)
pprint(r.json())

# response = requests.get(
#     'https://m.avito.ru/api/11/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=632490&localPriority=0&categoryId=24&params[201]=1060&params[504]=5257&params[2900-from]=2024-04-01&params[2900-to]=2024-04-08&params[123093]=3022415&page=1&lastStamp=1711573200&display=list&limit=25&presentationType=serp',
#     cookies=cookies,
#     headers=headers,
#     # proxies=proxies
# )

