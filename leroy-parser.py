import os
import time
from platform import system
import json
from urllib.parse import unquote


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

import requests
from bs4 import BeautifulSoup

from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1080))
display.start()

url = 'https://leroymerlin.ru/catalogue/tovary-dlya-uborki/'
# url = 'https://leroymerlin.ru/catalogue/teploizolyaciya/'
# url = 'https://leroymerlin.ru/product/uteplitel-teploknauf-stena-plita-50-mm-6-m-18482116/'
script_name = 'window.INITIAL_STATE["plp"]'


options = Options()
# options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

def get_scripts(html):
    soup = BeautifulSoup(html, 'lxml')
    scripts = soup.find_all('script')
    return scripts



with webdriver.Chrome(options=options, service=ChromiumService(ChromeDriverManager().install())) as driver:


    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    '''
    })



    # driver.get('https://nowsecure.nl')

    # wait = WebDriverWait(driver, 500)
    # driver.set_page_load_timeout(30)
    # driver.implicitly_wait(10)
    driver.get(url)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="product-cart-button"]')))
    time.sleep(15)
    # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="product-cart-button"]')))
    # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'button')))
    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()
    print('FIND!!')
    # element = driver.find_element(By.CSS_SELECTOR, '[data-qa="product-cart-button"]')
    # element.click()
    html = driver.page_source
    print(html)
    # print(html)
    scripts = get_scripts(html) 
    print(len(scripts))
    scripts = [script.text for script in scripts]
    for script in scripts:
        if script_name in script:
            print('script find')
            script = script.split('window.INITIAL_STATE["plp"]=')[1]
            script = script[:-1]
            with open('leroy.json', 'w', encoding='utf-8') as file:
                file.write(script)

            # with open('leroy.json', 'w') as file:
            #     json.dump(script, file)
            # print(script)
    # scripts = driver.find_elements(By.TAG_NAME, 'script')
    # # script_html = scripts[0].get_attribute('innerHTML')
    # print(len(scripts))
    # scripts = [script.get_attribute('innerHTML') for script in scripts]
    # for script in scripts:
    #     if script_name in script:
    #         script.split('window.mainBundle = ')[-1].split('</script>')[0]
    #         print(scripts)
    #         print('True')
    #         # script = unquote(script)
    #         with open('leroy.json', 'w') as file:
    #             json.dump(script, file, ensure_ascii=False)

    # html = driver.page_source
    # scripts = get_scripts(html)
    # print(scripts[0])
    
    # driver.close()
    # driver.quit()




# scripts = get_scripts(url)
# print(scripts)
# for script in scripts:
#     if script_name in script:
#         print(script)

