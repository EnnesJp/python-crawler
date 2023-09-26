from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

chrome_options = Options()
chrome_options.add_argument("--headless")
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

csvFile = open('clubeceticismo_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvFile)

def csv_writer(data):
  writer.writerow(data)

def get_wrapper():
  return driver.find_element(By.ID,'wrap')
  
def visit_debates_forum():
  allDebates = debatesContainer.find_elements(*forum_title_locator)
  for debate in allDebates:
    debate.click()
    visit_topics()
    driver.back()
    
def visit_topics():
  debatesWrapper = get_wrapper()
  forumTitle = debatesWrapper.find_element(By.CLASS_NAME, 'forum-title').text
  topicsContainer = debatesWrapper.find_element(*topics_locator)
  allTopics = topicsContainer.find_elements(*topic_title_locator)
  for topic in allTopics:
    topic.click()
    get_topics_data(forumTitle)
    driver.back()

# TODO: paginacao
# tratar posts inválidos
def get_topics_data(forumTitle):
  url = driver.current_url
  topicsWrapper = get_wrapper()
  topicTitle = topicsWrapper.find_element(By.CLASS_NAME, 'topic-title')
  posts = topicsWrapper.find_elements(By.CLASS_NAME, 'postbody')
  
  for post in posts:
    authorElement = post.find_element(By.CLASS_NAME, 'author')
    authorNameElement = authorElement.find_element(By.TAG_NAME, 'strong')
    authorURL = authorNameElement.find_element(By.TAG_NAME, 'a').get_attribute('href')
    postDateTime = authorElement.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
    content = post.find_element(By.CLASS_NAME, 'content')
    
    csvData = [
      content.get_attribute('innerHTML'),
      authorNameElement.text,
      authorURL,
      postDateTime,
      topicTitle.text,
      forumTitle,
      url
    ]
    
    csv_writer(csvData)
    
  
  
mainWrapper = get_wrapper()
debatesContainer = mainWrapper.find_element(*debates_locator)

visit_debates_forum()

csvFile.close()
driver.close()