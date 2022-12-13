import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
if platform.system() == 'Windows':
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options
import json
from time import sleep

def open_browser():
    global driver
    if platform.system() == 'Windows':
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif platform.system() == 'Linux':
        driver = webdriver.Chrome('/usr/bin/chromedriver')
    elif platform.system() == 'Darwin':
        driver = webdriver.Chrome()

with open('creds.txt') as f:
    data = f.read()
creds = json.loads(data)

input('!!! ALLES WORDT OP INACTIEF GEZET. DRUK OP EEN TOETS OM VERDER TE GAAN !!!')

# OPEN BROWSER
open_browser()
driver.get('https://admin.plugandpay.nl')

# LOGIN
email = driver.find_element(By.ID, 'email')
email.send_keys(creds["user"])
psswrd = driver.find_element(By.ID, 'password')
psswrd.send_keys(creds["password"])
driver.find_element(By.XPATH, '//button[@class="button has-arrow-right"]').click()

# GET NUMBER OF PAGES
driver.get('https://admin.plugandpay.nl/contracts')
page_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination-list"]')))
last_page = int(page_list.find_elements(By.TAG_NAME, 'a')[-2].text)
current_page = 1

# ADD ALL 'ACTIEF' CONTRACTS TO LIST
order_hrefs = []
while current_page < last_page:
    page_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination-list"]')))
    current_page = int(page_list.find_element(By.XPATH,'//li[@class="is-current"]').text)
    print(str(current_page) + 'of' + str(last_page))
    sleep(2)
    # READ TABLE WITH ORDER LINKS
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'orders')))
    orders = table.find_elements(By.XPATH, './/tbody/tr')
    for order in orders:
        state = order.find_element(By.XPATH,'.//span[contains(@class, "tag")]').text
        if state == 'Actief':
            order_hrefs.append(order.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        else:
            continue
    if current_page < last_page:
        page_list.find_elements(By.TAG_NAME, 'a')[-1].click()
    else:
        continue

# SET TO INACTIVE
for href in order_hrefs:
    driver.get(href)
    checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="box-body"]'))).find_element(By.XPATH, './/label[@for="isActive"]')
    checkbox.click()
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    sleep(2)

# # CHANGE DATE FOR CONTRACTS IN LIST
# for href in order_hrefs:
#     driver.get(href)
#     date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="box-body"]'))).find_element(By.XPATH, './/input[@class="input"]')
#     date.clear()
#     date.send_keys(new_date)
#     driver.find_element(By.XPATH, '//button[@type="submit"]').click()
#     sleep(2)

driver.quit()
print('Orders aangepast... Browser afgesloten...')
