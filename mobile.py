#Import required libraries
from selenium import webdriver
import time
from PIL import Image
from Screenshot import *


def mobiledevice():
    fscreenshot = Screenshot.Screenshot()
    driver = webdriver.Chrome(executable_path='chromedriver.exe')  # Mention location of chrome webdriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    # bot = webdriver.Chrome(executable_path=CM().install())
    driver.set_window_size(600, 1000)

    driver.get("https://www.nestlebabyandme.com.mx/?wf=engagement_tracker_test&nu_prev=1&var=1")  # Opens website
    #driver.maximize_window()
    time.sleep(3)
    elem = driver.find_element_by_xpath('//*[@id="profiling_quiz"]/div/button')  # Find the button using XPath
    elem.click()  # Click the button
    time.sleep(3)
    driver.save_screenshot('singletake.png') #Save screenshot to directory
    # time.sleep(3)
    #image = fscreenshot.full_Screenshot(driver, save_path=r'.', image_name='sometest.png')

    time.sleep(3)
    screenshot = Image.open('singletake.png')
    screenshot.show()
    time.sleep(10)

    driver.quit()  # Close the browser

if __name__ == '__main__':
    mobiledevice()
