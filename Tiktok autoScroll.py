import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge, EdgeOptions
options = EdgeOptions()
options.use_chromium = True

# Using Chrome to access 
driver = Edge(options=options)

# Open the website
driver.get('https://www.tiktok.com/en/')
driver.find_element("xpath","//video[@mediatype='video']").click()

while True:
    try:
      duration = driver.find_element("xpath","//div[@class='tiktok-1ioucls-DivSeekBarCircle e1rpry1m4']").get_attribute('style')
      # remove special charchters
      duration = duration.replace(";", "")
      duration = duration.replace("%", "")
      duration = duration.replace(")", "")
      duration = float(duration[11:16])

      #print(duration)

      if duration > 99:
          print("video done!")
          time.sleep(1)
          # swipe the video
          driver.find_element("xpath","//button[@data-e2e='arrow-right']").click()
          time.sleep(2)
    except:
       print("no scroll found") 
       time.sleep(5)
       #continue       