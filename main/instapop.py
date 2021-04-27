from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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

    # closing tab and quiting the browser
    def exit(self):
        self.browser.close()
        self.browser.quit()

    # checking by xpath if element exist
    def xpath_existing(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # signing into profile
    def sign_in(self):
        browser = self.browser
        try:
            browser.get("https://www.instagram.com/")
            browser.implicitly_wait(10)
            # closing pop-up window
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
            time.sleep(2)

        except Exception as ex:
            print(ex)
            self.exit()

    def open_profile(self, link):
        browser = self.browser
        browser.get(link)
        time.sleep(random.randrange(3))

    # liking post by certain link
    def like_exactly_post(self, link_post):
        browser = self.browser
        time.sleep(3)
        browser.get(link_post)
        time.sleep(3)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_existing(wrong_userpage):
            print("The post does not exist!")
        else:
            print("Post detected! Put our like!")

        like = browser.find_elements_by_css_selector("svg[fill = '#ed4956']")
        if like:
            print("Like already put")
            self.exit()
        else:
            browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
            time.sleep(2, 4)
            self.exit()

    def like_by_hash(self, hashtag):
        global posts
        browser = self.browser

        browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(5)

        for x in range(1, 5):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

            refs = browser.find_elements_by_tag_name("a")

            posts = [i.get_attribute("href") for i in refs if "/p/" in i.get_attribute("href")]
            # for i in refs:
            #     href = i.get_attribute("href")
            #     if "/p/" in href:
            #        posts.append(href)

        for y in posts[0:1]:
            browser.get(y)

            like = browser.find_elements_by_css_selector("svg[fill = '#ed4956']")
            if like:
                print("Like already put")
                self.exit()
            else:
                browser.find_element_by_xpath(
                    "//*[@id=\"react-root\"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                time.sleep(5)
                self.exit()

test = InstaBot(username, password)

test.sign_in()
test.like_by_hash("dog")
