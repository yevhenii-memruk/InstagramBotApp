from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from user_data import username, password
import time
import random
import os
import requests

"""Instagram Bot - InstaPOP.

Info:
This bot will help you keep your account more relevant and raise your activity to a high level

Features:
-Auto liking posts
-Auto subscription
-Make a list of all subscribers
-Download all media from instagram account
-Unsubscribe from profiles that do not follow you
"""


class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")

    def exit(self):
        self.browser.close()
        self.browser.quit()

    def sign_in(self):
        browser = self.browser
        try:
            browser.get("https://www.instagram.com/")
            browser.implicitly_wait(10)
            browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]").click()
            time.sleep(1)

            name_tag = browser.find_element_by_name("username")
            name_tag.clear()
            for step_typing in self.username:
                time.sleep(random.uniform(0.1, 0.3))
                name_tag.send_keys(step_typing)

            password_tag = browser.find_element_by_name("password")
            password_tag.clear()
            for step_typing in self.password:
                time.sleep(random.uniform(0.1, 0.3))
                password_tag.send_keys(step_typing)
            time.sleep(1)
            password_tag.send_keys(Keys.ENTER)

        except Exception as ex:
            print(ex)
            self.exit()

    

test = InstaBot(username, password)

test.sign_in()
