from PyQt5 import QtWidgets, uic
import sys

from PyQt5.uic.properties import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

import requests
import urllib 
from time import monotonic 
class MainWindow(QtWidgets.QMainWindow):      
    def __init__(self):   
        super(MainWindow, self).__init__()
        uic.loadUi('gui.ui', self)
        self.Download.clicked.connect(self.download)
        self.setWindowTitle("Series downloader!")
        self.show() 
   
       
  
    def download(self):

        try:
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


        except:
            self.driver.quit()
            QMessageBox.information(self , "Error" , "Series not found, Please try again")    
           
        try:

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
            url= links[0]
            
            
            #url = "https://a7-pl5-e5i6.vdst.one/dl/59038328bc7fca09caTCMNtHaI0mT2glV.W9J93Sua-HoGO53gNR5OEg__.NjA3WXE4bHNMOStlL0pEMFVkY1F2eldnYUNzejdXUTFSYXhmc0xqOWRUekV1a1dabEFmM2FDeGVKK1ZyYVRyTlZYaHVjMVVETGl2ZlJLSGZKbzduRGpKam03eGhxdysrRmFVR0FQcmUwb3p0dUVFYUZJZXJ1R092L1R1RWY5aHNrME16TmxMd1UwOTRJeVZOa2xaZzFGWFdpRnNUK0g5d3gxU3JpMlhNWVJUMWpTbGc1Wnl3VWRKV1VHRU41NWdlZnREaFQ1bWczeEZFK3NIMUdCR25mY1Y4cEd5TThyZ3hvQzkzMFpNU2RwQmZEZC9TU2xwSVA1YkFtR0V1MnA5dVlVbFdhNkVkWGpPblkvdEw0UWx3OWRXSk1QYms2Qll3SVpvakNPT244TG5zUkpobWxLNHJrSTNvaGJiZDBYNGlHNEpXczE4UnBPdDRZcThVN1FzQWlhTC9OMGprKzBjWExtMHVQa3BBbkRNeG5BQnRML055QVViYVJNamlNbUxEWXo5WHhPc3hodHQrSEp2ejZJWU82QmZDWVdTNy9TTk5aNVE9"
           
            
            r = requests.get(url, stream=True)
            file_size = int(r.headers['content-length'])
            print(file_size/1024/1024)
            downloaded = 0
            start = last_print = monotonic()
            QApplication.processEvents()
            with open(name, 'wb') as fp:
                for chunk in r.iter_content(chunk_size=1024):
                    downloaded += fp.write(chunk)
                    now = monotonic()
                    if now - last_print > 1:
                        pct_done = round(downloaded / file_size * 100)
                        speed = round(downloaded / (now - start) / 1024)
                        #print(f'Download {pct_done}% done, avg speed {speed} kbps')
                        remaining_time = int((file_size - downloaded)/speed/1024)

                        self.progressBar.setValue(pct_done)
                        self.speed_label.setText(f'Avg. speed: {speed} kbps')
                        self.time_label.setText(f'Time remaining: {remaining_time} s')
                        QApplication.processEvents()
                        last_print = now


            self.progressBar.setValue(100)   
            QMessageBox.information(self , "Download Completed" , "The Download Completed Successfully ")
            self.progressBar.setValue(0)         

        except:
            self.driver.quit()
            QMessageBox.information(self , "Error" , "adblocker detected, Please try again")    
        
    
app = 0            
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()                  
