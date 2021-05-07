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
    def __init__(self, username, password, file_name):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")
        self.file_name = file_name

    # closing tab and quiting the browser
    def exit(self):
        self.browser.close()
        self.browser.quit()

    # checking by xpath if element exist
    def xpath_existing(self, xpath):
        browser = self.browser
        try:
            browser.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # signing into profile
    def sign_in(self):
        browser = self.browser
        try:
            browser.get("https://www.instagram.com/")
            browser.maximize_window()
            browser.implicitly_wait(10)
            # closing pop-up window
            browser.find_element_by_xpath("/html/body/div[2]/div/div/button[1]").click()
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
            time.sleep(5)
        except Exception as ex:
            print(ex)
            self.exit()

    def open_profile(self, link):
        browser = self.browser
        try:
            browser.get(link)
        except NoSuchElementException:
            print("Sorry, this page isn't available.")

        time.sleep(random.randrange(2))

    # scrolling page and grab all url of posts
    def scrolling_get_urls(self):
        browser = self.browser
        all_post = []

        try:
            posts_num = int(
                browser.find_element_by_xpath(
                    "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            # 12 posts loads each scrolling
            if posts_num < 12:
                loops_count = 1
            else:
                loops_count = int(posts_num / 12)

            for x in range(loops_count):
                time.sleep(random.randrange(1, 2))
                tag_a = browser.find_elements_by_tag_name("a")

                for href_a in tag_a:
                    href = href_a.get_attribute("href")
                    if "/p/" in href:
                        if href not in all_post:
                            all_post.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            with open(f'{self.file_name}.txt', "w") as file_posts:
                for z in all_post:
                    file_posts.write(z + "\n")
        except Exception as ex:
            print(ex)

    # liking post by certain link
    def like_exactly_post(self, link_post):
        browser = self.browser

        try:
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
                time.sleep(random.randrange(2, 4))
                self.exit()
        except Exception as ex:
            print(ex)

    def like_by_hash(self, hashtag):
        global posts
        browser = self.browser

        try:
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

            for y in posts:
                browser.get(y)

                # check if like already exist
                like = browser.find_elements_by_css_selector("svg[fill = '#ed4956']")
                if like:
                    print("Like already put")
                    continue
                elif posts[-1]:
                    self.exit()
                else:
                    browser.find_element_by_xpath(
                        "//*[@id=\"react-root\"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                    # make a delay due to Instagram restriction
                    time.sleep(random.randrange(80, 100))
        except Exception as ex:
            print(ex)

    def like_profile(self, url_profile):
        browser = self.browser

        try:
            time.sleep(random.randrange(1, 3))

            self.open_profile(url_profile)
            self.scrolling_get_urls()

            with open(f'{self.file_name}.txt', 'r') as file_reader:
                for like_post in file_reader:
                    time.sleep(1)
                    browser.get(like_post)
                    time.sleep(random.randrange(2))

                    wrong_userpage = "/html/body/div[1]/section/main/div/h2"
                    if self.xpath_existing(wrong_userpage):
                        print("The post does not exist!")
                    else:
                        print("Post detected! Put our like!")

                    like = browser.find_elements_by_css_selector("svg[fill = '#ed4956']")
                    if like:
                        print("Like already put")
                    else:
                        # make a delay due to Instagram restriction
                        time.sleep(random.randrange(80, 100))
                        browser.find_element_by_xpath(
                            "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                        time.sleep(random.randrange(2, 3))
        except Exception as ex:
            print(ex)

        time.sleep(10)
        self.exit()


test = InstaBot(username, password, "test_list")

test.sign_in()
test.like_profile("https://www.instagram.com/rocketskywalker/")

# !!!!!!!!!!!!!! CLEAN TRY EXCEPT BLOCKS WHERE THEY NONSENSICAL