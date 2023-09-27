from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

import csv

import time
from time import sleep 

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
# Remove erro que estava sendo exibido com o chrome
# Fonte: https://bugs.chromium.org/p/chromedriver/issues/detail?id=2907#c3
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://clubeceticismo.com.br")

assert "No results found." not in driver.page_source

print(driver.title, '\n')

debates_locator = (By.CLASS_NAME,'category-4')
topics_locator = (By.CLASS_NAME,'forumbg')
forum_title_locator = (By.CLASS_NAME,'forumtitle')
topic_title_locator = (By.CLASS_NAME,'topictitle')
currentTopic = 1

wait = WebDriverWait(driver, 10)

csvFile = open('clubeceticismo_dataset.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvFile)

def csv_writer(data):
  writer.writerow(data)

def get_wrapper():
  return driver.find_element(By.ID,'wrap')
  
def visit_debates_forum():
  allDebates = debatesContainer.find_elements(*forum_title_locator)
  debateTitles = [debate.text for debate in allDebates]
  debateLinks = [debate.get_attribute("href") for debate in allDebates]
  
  for index, link in enumerate(debateLinks):
    if("https://clubeceticismo.com.br/" in link):
      print('Visiting debate "', debateTitles[index], '"\n')
      driver.get(link)
      time.sleep(3)
      visit_topics()
    else:
      print("Invalid Link")

def visit_topics(page = 1):
  print("Getting debate page", page, "\n")
  
  global currentTopic
  debatesWrapper = get_wrapper()
  nextPage = debatesWrapper.find_elements(By.CLASS_NAME, 'arrow.next')
  
  if nextPage:
    nextPageUrl = nextPage[0].find_element(By.TAG_NAME,'a').get_attribute("href")
    
  forumTitle = debatesWrapper.find_element(By.CLASS_NAME, 'forum-title').text
  topicsContainer = debatesWrapper.find_element(*topics_locator)
  allTopics = topicsContainer.find_elements(*topic_title_locator)
  topicTitles = [topic.text for topic in allTopics]
  topicLinks = [topic.get_attribute("href") for topic in allTopics]
  
  for index, link in enumerate(topicLinks):
    if("https://clubeceticismo.com.br/" in link):
      print('Visiting topic "', topicTitles[index], '"\n')
      driver.get(link)
      time.sleep(3)
      get_topics_data(forumTitle)
      currentTopic = currentTopic + 1
    else:
      print("Invalid Link")
      
  if nextPage:
    driver.get(nextPageUrl)
    visit_topics(page + 1)

def get_topics_data(forumTitle, previousIndex = 0, page = 1):
  print("Getting topic page", page, "\n")
  
  url = driver.current_url
  topicsWrapper = get_wrapper()
  
  wait = WebDriverWait(driver, timeout=60,ignored_exceptions=[NoSuchElementException])	
  wait.until(lambda d : driver.find_element(By.CLASS_NAME, "page-body"))	
  
  topicTitle = topicsWrapper.find_element(By.CLASS_NAME, 'topic-title')
  posts = topicsWrapper.find_elements(By.CLASS_NAME, 'post')
  
  for index, post in enumerate(posts):
    print('Getting post', index+previousIndex+1, 'data\n')
    authorElement = post.find_element(By.CLASS_NAME, 'author')
    authorNameElement = authorElement.find_element(By.TAG_NAME, 'strong')
    authorURL = authorNameElement.find_element(By.TAG_NAME, 'a').get_attribute('href')
    authorTotalMessages= post.find_element(By.CLASS_NAME,'profile-posts').find_element(By.TAG_NAME, 'a')
    postDateTime = authorElement.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
    content = post.find_element(By.CLASS_NAME, 'content')
    
    csvData = [
      currentTopic,
      index + previousIndex,
      topicTitle.text,
      forumTitle,
      url,
      authorNameElement.text,
      authorURL,
      authorTotalMessages.text,
      postDateTime,
      content.get_attribute('innerHTML')
    ]
    csv_writer(csvData)

  nextPage = topicsWrapper.find_elements(By.CLASS_NAME, 'arrow.next')
  if nextPage:
    
    nextPage[0].click()
    get_topics_data(forumTitle, previousIndex + 50, page + 1)
  
mainWrapper = get_wrapper()
debatesContainer = mainWrapper.find_element(*debates_locator)

print("Init crawling...\n")
visit_debates_forum()
print("Crawling finished!")

csvFile.close()
driver.close()