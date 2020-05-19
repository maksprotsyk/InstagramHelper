"""
Example of selenium and Webdriver API
"""
from time import sleep
from selenium import webdriver


# opening the browser
CHROME = webdriver.Chrome('chromedriver')

# opening the page
CHROME.get('https://www.instagram.com/toyota/')

#waiting for page to load
sleep(4)

# getting the number of posts
POSTS = CHROME.find_element_by_class_name('g47SY').text

print(POSTS)

# closing the browser
CHROME.quit()
