import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

movie = input("Enter movie name: ")
i = int(input("1. 1080p \n2. 720p\n3. 480p\n4. 360p\n"))
#choice =int(input("1.Download \n 2.Li"))

from msedge.selenium_tools import Edge, EdgeOptions
options = EdgeOptions()
options.use_chromium = True

# Using Chrome to access Google_Search
driver = Edge(options=options)
# Open the website
driver.get("http://www.google.com")
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
element.send_keys("site:egybest.com "+movie)
element.send_keys(Keys.ENTER)
time.sleep(3)
result = driver.find_element_by_tag_name('h3')
result.click()
time.sleep(3) 
driver.find_element_by_xpath("//a[@href='#download']").click()
driver.switch_to.window(driver.window_handles[1])
time.sleep(5)
driver.close()
driver.switch_to.window(driver.window_handles[0])

download = driver.find_elements_by_xpath("//a[ @class='nop btn g dl _open_window']")
download[i-1].click()
time.sleep(2)    
driver.switch_to.window(driver.window_handles[1])
VidStream = driver.find_element_by_xpath("//i[ @class='ico-down-circle']")
VidStream.click()
time.sleep(2) 
VidStream.click()
time.sleep(3) 
driver.switch_to.window(driver.window_handles[1])
VidStream = driver.find_element_by_xpath("//i[ @class='ico-down-circle']")
VidStream.click()

driver.switch_to.window(driver.window_handles[1])
elems = driver.find_elements_by_xpath("//a[@class='bigbutton']")
links = [elem.get_attribute('href') for elem in elems]
print("Download Link: "+links[0])
name = driver.find_elements_by_tag_name('h2')[0].text
print("Movie Full name:\n" + name)