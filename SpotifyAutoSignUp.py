import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import tkinter as tk
import time

# Using Chrome to access temp-mail
driver = webdriver.Edge()
# Open the website
driver.get('https://temp-mail.org/en/')
time.sleep(10)
copy_box = driver.find_element('xpath',"//button[@class='btn-rds icon-btn bg-theme click-to-copy copyIconGreenBtn']")
copy_box.click()
root = tk.Tk()
tempMail = root.clipboard_get()
with open('data.txt', 'w') as f:
    f.write("Email: %s" % tempMail+ '\n')
print(tempMail)
driver.close()
#############################################################################################################
# Using Chrome to access spotify
driver = webdriver.Edge()
driver.maximize_window()
# Open the website
driver.get('https://www.spotify.com/eg-en/signup')
#time.sleep(10)


##########################################-Capthca-###############################################
# driver.find_element('xpath',"//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']").click()
# WebDriverWait(driver, 40).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='reCAPTCHA']")))
# WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='recaptcha-checkbox-border']"))).click()
# driver.switch_to.default_content()

###########################################################Sign-UP########################################
# Equivalent email! 
email_box = driver.find_element('id','email')
email_box.send_keys(tempMail)
# Equivalent confirm! 
if len(driver.find_elements('xpath',"//input[@id='confirm']")) > 0:
    confirm_box = driver.find_element('xpath',"//input[@id='confirm']")
    confirm_box.send_keys(tempMail)
# Equivalent password! 
password_box = driver.find_element('id','password')
password_box.send_keys('randompassword')
# Equivalent displayname! 
displayname_box = driver.find_element('id','displayname')
displayname_box.send_keys('randomname')
# Equivalent month! 
month_box = driver.find_element('id','month')
month_box.send_keys('October')
# Equivalent day! 
day_box = driver.find_element('id','day')
day_box.send_keys('8')
# Equivalent year! 
year_box = driver.find_element('id','year')
year_box.send_keys('2000')
#choose gender as male! 
displayname_box.send_keys(Keys.TAB + Keys.TAB+ Keys.TAB+ Keys.TAB+" "+Keys.RETURN)
# confirm
displayname_box.send_keys(Keys.TAB + Keys.TAB+ Keys.TAB+ Keys.TAB+Keys.TAB + Keys.TAB+ Keys.TAB+ Keys.TAB+ Keys.TAB+" "+Keys.RETURN)


WebDriverWait(driver, 40).until(EC.presence_of_element_located(('link text',"Premium")))

#After_Captcha
driver.find_element("link text","Premium").click()
driver.find_element("link text","GET STARTED").click()
time.sleep(4)
premium = driver.find_element("link text",'Offer terms')
premium.send_keys(Keys.TAB+Keys.RETURN)

#Credit-Card
WebDriverWait(driver, 2).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@src='https://pci.spotify.com/static/form_no_selects.html']")))
WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='tel' and @id='cardnumber']"))).send_keys("4393 3754 9369 1813")
WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='tel' and @id='expiry-date']"))).send_keys("1225")
WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='tel' and @id='security-code']"))).send_keys("123" + Keys.RETURN)
print('done')
