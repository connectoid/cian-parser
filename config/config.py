import logging
from environs import Env


logger = logging.getLogger(__name__)
env: Env = Env()
env.read_env()

logging.basicConfig(
    level=logging.INFO,
    filename = "botlog.log",
    filemode='a',
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

token = env('token')


cookies = {
    '_CIAN_GK': '94c63ded-a282-4949-a2b9-fc737cb9e328',
    '_gcl_au': '1.1.323410645.1710834443',
    'tmr_lvid': '5302648a3193a641de006a283b24ac4d',
    'tmr_lvidTS': '1710834458627',
    'login_mro_popup': '1',
    'sopr_utm': '%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'uxfb_usertype': 'searcher',
    '_ym_uid': '1710834508159927190',
    '_ym_d': '1710834508',
    'uxs_uid': '27fca1d0-e5c5-11ee-a6fa-bf1853765323',
    'adrcid': 'ARvfXEzxg7yaLzHMpYLmG3Q',
    'afUserId': 'ae0ee7c1-152d-4b78-8ece-7fe0388bd2a2-p',
    'cookie_agreement_accepted': '1',
    'my_home_tooltip_key': '1',
    'session_region_name': '%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%BB%D1%8C',
    'forever_region_id': '5075',
    'forever_region_name': '%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%BB%D1%8C',
    'session_region_id': '175050',
    'session_main_town_region_id': '175050',
    '_gid': 'GA1.2.785801873.1711422453',
    'uxfb_card_satisfaction': '%5B300038946%2C300026939%5D',
    '_ga': 'GA1.2.1493516238.1710834497',
    '__cf_bm': '_9bL02OEHeKP.VtH068yXz7tuIXFxw.f4aPIgjlByWk-1711498203-1.0.1.1-JDBQCmtacBQSaPq5NBbxhc9WMPVtpm7_IcEfIVgNmyMICRIlZE9VP0yEyHVTUx.pQKgNlKnmBnsSVs.Tv4RuZA',
    'sopr_session': '148c491d278d4686',
    '_dc_gtm_UA-30374201-1': '1',
    '_ga_3369S417EL': 'GS1.1.1711498276.12.1.1711498328.8.0.0',
}

headers = {
    'authority': 'api.cian.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'content-type': 'application/json',
    # 'cookie': '_CIAN_GK=94c63ded-a282-4949-a2b9-fc737cb9e328; _gcl_au=1.1.323410645.1710834443; tmr_lvid=5302648a3193a641de006a283b24ac4d; tmr_lvidTS=1710834458627; login_mro_popup=1; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; uxfb_usertype=searcher; _ym_uid=1710834508159927190; _ym_d=1710834508; uxs_uid=27fca1d0-e5c5-11ee-a6fa-bf1853765323; adrcid=ARvfXEzxg7yaLzHMpYLmG3Q; afUserId=ae0ee7c1-152d-4b78-8ece-7fe0388bd2a2-p; cookie_agreement_accepted=1; AF_SYNC=1710838667758; _gid=GA1.2.1052767571.1710974219; _ym_isad=1; __cf_bm=b4wPcM_N0.zyWABm6IhDmx3mQpxeVLjeWtEJwji.yVM-1710994063-1.0.1.1-gO6csZe4DjnoXEsCemd9Z6HdNSC70D3zVasvRZ8kTdpeND7O3iI_t8A354IV0c3LUjI8dLofcp9DFRoVCmWKlw; my_home_tooltip_key=1; sopr_session=e600f07fbd474622; _ym_visorc=b; session_region_name=%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%BB%D1%8C; forever_region_id=5075; forever_region_name=%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%BB%D1%8C; session_region_id=4636; session_main_town_region_id=5075; _ga=GA1.2.1493516238.1710834497; _dc_gtm_UA-30374201-1=1; _ga_3369S417EL=GS1.1.1710994146.7.1.1710994762.60.0.0',
    'origin': 'https://yaroslavl.cian.ru',
    'referer': 'https://yaroslavl.cian.ru/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}
