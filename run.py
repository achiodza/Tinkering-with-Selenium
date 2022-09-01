import http.client
import json
import os
import time
import urllib

import bs4
import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM

import csv

# Complete these 2 fields ==================


# ==========================================

TIMEOUT = 15


def scrape():
    # user_name = input('[Required] - Please enter username: ')
    #
    # user_password = input('[Required] - Please enter password: ')

    user_csv = input('[Required] - Please enter csv name *** NB without the extension .csv please please: ')

    user_failed = input('[Required] - is this a failed file [yes/no]: ')

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(executable_path=CM().install())
    # bot.set_window_size(600, 1000)

    bot.get('https://www.instagram.com/accounts/login/')

    time.sleep(15)

    cluster = open('{}.csv'.format(user_csv), encoding="utf-8")

    if user_failed == 'yes':
        scrapped = open('{}scrapped.csv'.format(user_csv[0:-6]), 'a', encoding="utf-8", newline='')
    else:
        scrapped = open('{}scrapped.csv'.format(user_csv), 'w', encoding="utf-8", newline='')
    failed = open('{}failed.csv'.format(user_csv), 'w', encoding="utf-8", newline='')
    header = [
        'id', 'username', 'full_name', 'biography', 'external_url',
        'facebook_id', 'contact_method', 'email', 'phone',
        'business_category', 'category', 'pic_url', 'is_private',
        'followers_count',
        'following_count',
    ]
    failed_header = ['username']
    writer = csv.writer(scrapped)
    writer_failed = csv.writer(failed)
    writer.writerow(header)
    writer_failed.writerow(failed_header)

    csvreader = csv.reader(cluster)
    next(csvreader)
    rows = []
    count = 0
    total = 0
    total_f = 0
    limit = 'no'
    for index, row in enumerate(csvreader):
        rows.append(row)
        if limit == 'yes':
            writer_failed.writerow([row[0]])
            total_f += 1
            continue
        bot.get("https://www.instagram.com/{}/?__a=1&__d=dis".format(row[0].strip()))
        time.sleep(5)
        data = json.loads(bot.find_element(by=By.TAG_NAME, value='body').text)
        count += 1
        if "graphql" in data:
            user = data['graphql']['user']
            writer.writerow([
                user['id'], user['username'], user['full_name'],
                user['biography'], user['external_url'], user['fbid'],
                user['business_contact_method'], user['business_email'], user['business_phone_number'],
                user['business_category_name'], user['category_name'], user['profile_pic_url'],
                user['is_private'], user['edge_followed_by']['count'], user['edge_follow']['count'],
            ])
            total += 1
        elif "message" in data:
            print("timeout at {}".format(index))
            limit = 'yes'
        else:
            writer_failed.writerow([row[0]])
            total_f += 1
        if count == 200:
            print("pausing at {}".format(index))
            time.sleep(10)
            count = 0
        print("index = {}   total_failed = {}  total_success = {} ".format(index, total_f, total))

    scrapped.close()
    failed.close()


if __name__ == '__main__':
    scrape()