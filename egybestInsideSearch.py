######################## Direct from Egybest ######################
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

movie = input("Enter movie name: ")
movie = movie.replace(' ','-')
print(movie)
j = int(input("1. 1080p \n2. 720p\n3. 480p\n4. 360p\n"))

from msedge.selenium_tools import Edge, EdgeOptions
options = EdgeOptions()
options.use_chromium = True

def egybestInside():
    # Using Chrome to access egybest
    driver = Edge(options=options)
    # Open the website
    driver.get("https://move.egybest.ninja/movies/subbed")

    element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
    element.send_keys(movie + Keys.RETURN)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

    movies = driver.find_elements_by_xpath("//a[@class='movie']")
    lnks = []
    for i in movies:
        lnks.append(i.get_attribute("href"))
    if any(movie in word for word in lnks):
        print('Movie is there inside the list!')
        movies[0].click()
    else:
        print("movie not found")

          
    time.sleep(4)    
    download = driver.find_elements_by_xpath("//a[ @class='nop btn g dl _open_window']")
    #print(download)
    time.sleep(4)
    
    while len(driver.find_elements_by_xpath("//i[@class='i-refresh']"))>0:
        print("ad block error, trying again....")
        driver.close()
        egybestInside()    
        break
        
    download[j-1].click()
    time.sleep(2)
    
    driver.switch_to.window(driver.window_handles[1])
    
    while len(driver.find_elements_by_xpath("//i[@class='i-refresh']"))>0:
        print("ad block error, trying again....")
        driver.close()
        egybestInside() 
        break
        
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
    print("Movie Full name:\n" + name+'\n\n\n')
    
    
egybestInside()    