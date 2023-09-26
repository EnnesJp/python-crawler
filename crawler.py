from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
# Remove erro que estava sendo exibido com o chrome
# Fonte: https://bugs.chromium.org/p/chromedriver/issues/detail?id=2907#c3
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://clubeceticismo.com.br")

assert "No results found." not in driver.page_source

print(driver.title)

debates_locator = (By.CLASS_NAME,'category-4')
topics_locator = (By.CLASS_NAME,'forumbg')
forum_title_locator = (By.CLASS_NAME,'forumtitle')
topic_title_locator = (By.CLASS_NAME,'topictitle')

def get_wrapper():
  return driver.find_element(By.ID,'wrap')
  
def visit_debates_forum():
  allTags = debatesContainer.find_elements(*forum_title_locator)
  for tag in allTags:
    tag.click()
    wait = WebDriverWait(driver, 10)
    forumTitle = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'forum-title')))
    print(forumTitle.text)
    get_topics_title()
    driver.back()
    
def get_topics_title():
  newWrapper = get_wrapper()
  topicsContainer = newWrapper.find_element(*topics_locator)
  allTags = topicsContainer.find_elements(*topic_title_locator)
  for tag in allTags:
    print(tag.text)
  
mainWrapper = get_wrapper()
debatesContainer = mainWrapper.find_element(*debates_locator)

visit_debates_forum()

driver.close()