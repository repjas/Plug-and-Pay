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

open_browser()

driver.get('https://admin.plugandpay.nl')

email = driver.find_element(By.ID, 'email')
email.send_keys(creds["user"])
psswrd = driver.find_element(By.ID, 'password')
psswrd.send_keys(creds["password"])
driver.find_element(By.XPATH, '//button[@class="button has-arrow-right"]').click()

driver.get('https://admin.plugandpay.nl/contracts')

table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'orders')))
orders = table.find_elements(By.XPATH, './/tbody/tr')
order_hrefs = []
for order in orders:
    state = order.find_element(By.XPATH,'.//span[contains(@class, "tag")]').text
    if state == 'Actief':
        order_hrefs.append(order.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    else:
        continue
for href in order_hrefs:
    driver.get(href)
    date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="box-body"]'))).find_element(By.XPATH, './/input[@class="input"]')
    date.clear()
    date.send_keys('30-09-2022')
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
