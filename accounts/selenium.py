import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_recaptcha_token():
    options = Options()
    options.add_argument('disable-infobars')
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://cadastro.cfp.org.br/")
    time.sleep(1)
    recaptcha_value = driver.find_element(By.ID, "g-recaptcha-response-100000").get_attribute('value')
    return recaptcha_value