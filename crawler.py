from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
# Remove erro que estava sendo exibido com o chrome
# Fonte: https://bugs.chromium.org/p/chromedriver/issues/detail?id=2907#c3
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://clubeceticismo.com.br")
print(driver.title)

assert "No results found." not in driver.page_source
driver.close()