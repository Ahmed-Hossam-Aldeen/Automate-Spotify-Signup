from PyQt5 import QtWidgets, uic
import sys

from PyQt5.uic.properties import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

import requests

class MainWindow(QtWidgets.QMainWindow):      
    def __init__(self):   
        super(MainWindow, self).__init__()
        uic.loadUi('gui.ui', self)
        self.Download.clicked.connect(self.download)
        self.setWindowTitle("Series downloader!")
        self.show() 
           
  
    def download(self):
        series = self.name.toPlainText()
        series = series.replace(' ','-')
        #print(series)
        season = int(self.sesn.toPlainText())
        episode = int(self.ep.toPlainText())
        j = self.comboBox.currentIndex()
       
        from msedge.selenium_tools import Edge, EdgeOptions
        options = EdgeOptions()
        #options.binary_location = 'edge/msedgedriver.exe'
        options.use_chromium = True


        # Using Chrome to access egybest
        self.driver = Edge(options=options)
        # Open the website
        self.driver.get(f"https://move.egybest.ninja/season/{series}-season-{season}/?ref=search-p1")


        target_episode = self.driver.find_element_by_xpath(f"//a[@href='https://move.egybest.ninja/episode/{series}-season-{season}-ep-{episode}/?ref=search-p1']")
        target_episode.click()
        
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])     
  

        time.sleep(4)

        download = self.driver.find_elements_by_xpath("//a[ @class='nop btn g dl _open_window']")
        download[j].click()
        time.sleep(2)

        self.driver.switch_to.window(self.driver.window_handles[1])

        VidStream = self.driver.find_element_by_xpath("//i[ @class='ico-down-circle']")
        VidStream.click()
        time.sleep(2) 
        VidStream.click()
        time.sleep(3) 
        self.driver.switch_to.window(self.driver.window_handles[1])
        VidStream = self.driver.find_element_by_xpath("//i[ @class='ico-down-circle']")
        #VidStream.click()

        self.driver.switch_to.window(self.driver.window_handles[1])
        elems = self.driver.find_elements_by_xpath("//a[@class='bigbutton']")
        links = [elem.get_attribute('href') for elem in elems]
        print("Download Link: "+links[0])
        name = self.driver.find_elements_by_tag_name('h2')[0].text
        print("Episode Full name:\n" + name+'\n\n\n')      
        self.driver.quit()
        
        
        url = links[0]
        response = requests.get(url, stream=True)
        with open(name, "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        
    
app = 0            
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()                  