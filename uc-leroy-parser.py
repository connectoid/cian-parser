import time

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options


options = Options()
# options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--headless')
options.add_argument("--headless=chrome")
# options.add_argument('--no-sandbox')
# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)


driver = uc.Chrome(options=options)

url = 'https://leroymerlin.ru/catalogue/tovary-dlya-uborki/'


driver.get(url)
time.sleep(10)
html = driver.page_source
print(html)
driver.close()
driver.quit()