from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from user_data import username, password
import time
import random
import os
import requests

from bs4 import BeautifulSoup as bs

"""Instagram Bot - InstaPOP.

Info:
This bot will help you keep your account more relevant and raise your activity to a high level

Features:
-Auto liking posts
-Auto subscription
-Auto liking posts by hashtag
-Make a list of all subscribers
-Download all media from instagram account
-Unsubscribe from profiles that do not follow you
-Automatic browsing of stories
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

    # scrolling page and grab all url of posts into file
    def scrolling_get_urls(self):
        browser = self.browser
        all_post = []

        posts_num = int(
            browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
        # 12 posts loads each scrolling
        if posts_num < 12:
            loops_count = 1
        else:
            loops_count = int(posts_num / 12)

        try:
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
        except Exception as ex:
            print(ex)

        with open(f'{self.file_name}.txt', "w") as file_posts:
            for z in all_post:
                file_posts.write(z + "\n")

    # liking post by certain link
    def like_exactly_post(self, link_post):
        browser = self.browser

        time.sleep(3)
        browser.get(link_post)
        time.sleep(3)

        try:
            wrong_user_page = "/html/body/div[1]/section/main/div/h2"
            if self.xpath_existing(wrong_user_page):
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

            # !!! make number of scrolling manually change
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

        time.sleep(random.randrange(1, 3))

        self.open_profile(url_profile)
        self.scrolling_get_urls()

        try:
            with open(f'{self.file_name}.txt', 'r') as file_reader:
                for like_post in file_reader:
                    time.sleep(1)
                    browser.get(like_post)
                    time.sleep(random.randrange(2))

                    wrong_user_page = "/html/body/div[1]/section/main/div/h2"
                    if self.xpath_existing(wrong_user_page):
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

        self.exit()

    def download_media(self, url_profile):
        browser = self.browser
        file_name = url_profile.split("/")[-2]

        self.open_profile(url_profile)
        self.scrolling_get_urls()

        if os.path.exists(f'{file_name}'):
            print("Folder exist yet!")
        else:
            os.mkdir(f"{file_name}")

        # Clean folder with content
        for f in os.listdir(f"{file_name}"):
            os.remove(os.path.join(file_name, f))

        # OPTION 0
        # Download only images!
        # Make futures ( download video, download multiple post )
        with open(f"{self.file_name}.txt", "r") as file_reader:
            for like_post in file_reader:
                browser.get(like_post)

                try:
                    soup = bs(browser.page_source, 'lxml')

                    ''' Extract the url of the image from the source code'''
                    img = soup.find('img', class_='FFVAD')
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    if self.xpath_existing(video_src):
                        continue
                    img_url = img['src']

                    '''Download the image via the url using the requests library'''
                    r = requests.get(img_url)

                    with open(f"{file_name}" + "/" + "instagram" + str(time.time()) + ".png", 'wb') as f:
                        f.write(r.content)
                except Exception as ex:
                    print(ex)
        self.exit()

    # OPTION 1
    # download_url = ''
    # with open(f"{self.file_name}.txt", "r") as file_reader:
    #     for like_post in file_reader:
    #         browser.get(like_post)
    #         shortcode = browser.current_url.split("/")[-2]
    #         time.sleep(5)
    #         if browser.find_element_by_css_selector("img[style='object-fit: cover;']") is not None:
    #             download_url = browser.find_element_by_css_selector(
    #                 "img[style='object-fit: cover;']").get_attribute(
    #                 'src')
    #             urllib.request.urlretrieve(download_url, '{}.jpg'.format(shortcode))
    #         else:
    #             download_url = browser.find_element_by_css_selector("video[type='video/mp4']").get_attribute('src')
    #             urllib.request.urlretrieve(download_url, '{}.mp4'.format(shortcode))
    #         time.sleep(5)

    # OPTION 2
    # button_next = ["/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/button[2]/div",
    #                "/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/button",
    #                "/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/button/div"]
    # media_url_list = []
    # post_id = url_profile.split("/")[-2]
    #
    # self.open_profile(url_profile)
    # self.scrolling_get_urls()
    #
    # with open(f"{self.file_name}.txt", "r") as file_reader:
    #     for like_post in file_reader:
    #         browser.get(like_post)
    #
    #         tag_img = browser.find_elements_by_tag_name("img")
    #
    #         video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
    #         single_src_img = [media_url_list.append(i.get_attribute("src")) for i in tag_img if
    #                           "Photo shared by" in i.get_attribute("alt") or "Photo by" in i.get_attribute("alt")]
    #         # save images
    #         for save_link in media_url_list:
    #             get_media = requests.get(save_link)
    #             with open(f"{post_id}_img.jpg", "wb") as img_file:
    #                 img_file.write(get_media.content)
    #
    #         if self.xpath_existing(video_src):
    #             tag_video = browser.find_elements_by_tag_name("video")
    #             single_src_video = [media_url_list.append(i.get_attribute("src")) for i in tag_video]
    #
    #         for i in button_next:
    #             if self.xpath_existing(i):
    #                 browser.find_element_by_xpath(i).click()
    #
    #         with open("media_url_list.txt", "w") as file:
    #             for i in media_url_list:
    #                 file.write(i + "\n")
    #
    #

    # follow to exact profile
    def follow_exact_profile(self, url_profile):
        browser = self.browser
        follow_button = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button"

        self.open_profile(url_profile)
        if self.xpath_existing(follow_button):
            time.sleep(3)
            browser.find_element_by_xpath(follow_button).click()
        else:
            pass

        self.exit()

    # follow to all of user's followers
    def follow_engine(self, url_profile):
        num_scroll = 1
        browser = self.browser
        browser.get(url_profile)
        name_user = url_profile.split("/")[-2]

        time.sleep(2)

        # Create User folder
        if os.path.exists(f"{name_user}"):
            print("Folder already exist!")
        else:
            print("Create folder!")
            os.mkdir(name_user)

        num_followers = int(
            browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text)
        if num_followers <= 12:
            num_scroll = 1
        if num_followers > 12:
            num_scroll = int(num_followers / 12)

        browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()

        time.sleep(3)

        follower_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        follower_urls = []

        for scroll in range(num_scroll):
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follower_ul)
            time.sleep(2)

        all_divs = follower_ul.find_elements_by_tag_name("li")

        for link_follower in all_divs:
            link_follower = link_follower.find_element_by_tag_name("a").get_attribute("href")
            follower_urls.append(link_follower)

        with open(f"{name_user}/{name_user}.txt", "w") as file_urls:
            for iter_link in follower_urls:
                file_urls.write(iter_link + "\n")

        time.sleep(random.randrange(2, 3))

        with open(f"{name_user}/{name_user}.txt") as urls_reader:
            for user_url in urls_reader:
                try:
                    with open(f"{name_user}/{name_user}_following.txt") as check_list:
                        if user_url in check_list.readlines():
                            continue
                except Exception as ex:
                    print("File do not exist yet!")

                browser.get(user_url)

                follow_button = [
                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button",
                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button"]
                already_followed_button = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div/span"
                our_profile = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a"

                time.sleep(3)

                if self.xpath_existing(already_followed_button):
                    print("You have already subscribed to this user!")
                    continue
                if self.xpath_existing(follow_button[0]):
                    browser.find_element_by_xpath(follow_button[0]).click()
                    print("Following to " + user_url.split("/")[-2])
                if self.xpath_existing(our_profile):
                    print("It's me!")
                elif self.xpath_existing(follow_button[1]):
                    browser.find_element_by_xpath(follow_button[1]).click()
                    print("Following to " + user_url.split("/")[-2])

                # create a file to skip our following users
                with open(f"{name_user}/{name_user}_following.txt", "a") as following:
                    following.write(user_url)

                time.sleep(random.randrange(120, 180))

test = InstaBot(username, password, "test_list")

test.sign_in()
# test.like_profile("https://www.instagram.com/rocketskywalker/")
# test.download_media("https://www.instagram.com/rocketskywalker/")
test.follow_engine("https://www.instagram.com/anny_eyebrow/")
