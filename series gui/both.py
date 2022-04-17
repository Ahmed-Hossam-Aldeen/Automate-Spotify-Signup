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
        self.folder = ""
        self.action_choose_location.triggered.connect(self.openFileNameDialog) 
        self.Download_2.clicked.connect(self.downloadMovie)
        self.Download.clicked.connect(self.downloadSeries)
        self.setWindowTitle("Series downloader!")
        self.show() 
   
    def openFileNameDialog(self):
        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(self.folder)       
  
    def downloadSeries(self):
        
        if self.folder == "":
            QMessageBox.information(self , "Error" , "Please Choose where to download first!")
            return  
        
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
            return
           
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
            
            r = requests.get(url, stream=True)
            file_size = int(r.headers['content-length'])
            print(file_size/1024/1024)
            downloaded = 0
            start = last_print = monotonic()
            QApplication.processEvents()
            with open(self.folder+"/"+name, 'wb') as fp:
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

            
    def downloadMovie(self):
        if self.folder == "":
            QMessageBox.information(self , "Error" , "Please Choose where to download first!")
            return  
        movie = self.name_2.toPlainText()
        j = self.comboBox.currentIndex()
       
        from msedge.selenium_tools import Edge, EdgeOptions
        options = EdgeOptions()
        #options.binary_location = 'edge/msedgedriver.exe'
        options.use_chromium = True


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
            driver.quit()
            QMessageBox.information(self , "Error" , "Movie not found")
            print("movie not found")
            return

        time.sleep(4)  

        try:
            download = driver.find_elements_by_xpath("//a[ @class='nop btn g dl _open_window']")
            time.sleep(4)
            download[j].click()
            time.sleep(2)

            driver.switch_to.window(driver.window_handles[1])

            VidStream = driver.find_element_by_xpath("//i[ @class='ico-down-circle']")
            VidStream.click()
            time.sleep(2) 
            VidStream.click()
            time.sleep(3) 
            driver.switch_to.window(driver.window_handles[1])
            VidStream = driver.find_element_by_xpath("//i[ @class='ico-down-circle']")
            #VidStream.click()

            driver.switch_to.window(driver.window_handles[1])
            elems = driver.find_elements_by_xpath("//a[@class='bigbutton']")
            links = [elem.get_attribute('href') for elem in elems]
            print("Download Link: "+links[0])
            name = driver.find_elements_by_tag_name('h2')[0].text
            print("Movie Full name:\n" + name+'\n\n\n')      
            driver.quit()
            url= links[0] 

            r = requests.get(url, stream=True)
            file_size = int(r.headers['content-length'])
            print(file_size/1024/1024)
            downloaded = 0
            start = last_print = monotonic()
            QApplication.processEvents()
            with open(self.folder+"/"+name, 'wb') as fp:
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

            self.progressBar.setValue(1000)
            QMessageBox.information(self , "Download Completed" , "The Download Completed Successfully ")
            self.progressBar.setValue(0)     
            
        except:
            self.driver.quit()
            QMessageBox.information(self , "Error" , "Series not found, Please try again")
            return        
    
app = 0            
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()                  