#Import required libraries
from selenium import webdriver
import time
from PIL import Image
from Screenshot import *


def bigdevice():
    fscreenshot = Screenshot.Screenshot()
    driver = webdriver.Chrome(executable_path='chromedriver.exe')  # Mention location of chrome webdriver

    driver.get("https://accounts.google.com/ServiceLogin?service=mail&passive=1209600&osid=1&continue=https://mail.google.com/mail/u/0/&followup=https://mail.google.com/mail/u/0/&emr=1")  # Opens website
    driver.maximize_window()
    time.sleep(3)
    elem = driver.find_element_by_xpath('//*[@id="profiling_quiz"]/div/button')  # Find the button using XPath
    elem.click()  # Click the button
    time.sleep(3)
    # driver.save_screenshot('singletake.png') #Save screenshot to directory
    # time.sleep(3)
    image = fscreenshot.full_Screenshot(driver, save_path=r'.', image_name='sometest.png')

    time.sleep(3)
    screenshot = Image.open('sometest.png')
    screenshot.show()
    time.sleep(10)

    driver.quit()  # Close the browser
