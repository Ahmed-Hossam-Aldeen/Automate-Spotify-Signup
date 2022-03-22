######################## Direct from Egybest ######################
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys


def skip():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])   

series = input("Enter series name: ")
series = series.replace(' ','-')
print(series)
season = input("Enter season: ")
episode = input("Enter episode: ")
j = int(input("1. 1080p \n2. 720p\n3. 480p\n4. 360p\n"))

from msedge.selenium_tools import Edge, EdgeOptions
options = EdgeOptions()
options.use_chromium = True


# Using Chrome to access egybest
driver = Edge(options=options)
# Open the website
driver.get(f"https://move.egybest.ninja/season/{series}-season-{season}/?ref=search-p1")


target_episode = driver.find_element_by_xpath(f"//a[@href='https://move.egybest.ninja/episode/{series}-season-{season}-ep-{episode}/?ref=search-p1']")
target_episode.click()
skip()

time.sleep(4)

download = driver.find_elements_by_xpath("//a[ @class='nop btn g dl _open_window']")
download[j-1].click()
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
print("Episode Full name:\n" + name+'\n\n\n')