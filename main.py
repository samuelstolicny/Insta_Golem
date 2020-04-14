from selenium import webdriver
import os
import time
import random
import configparser
import ast
import logging
import datetime


class InstagramBot:

    #CONSTRUCTOR
    def __init__(self, username, password):
        #/////////////////////////////////////////////////////////////////////////////////////////////////////
        """
        Initializes an instance of the InstagramBot class.
        Call the login method to authenticate a user with Instagram.

        Args:
            username:str: The Instagram username for a user
            password:str: The Instagram password for a user    

        Atributes:
            driver:Selenium.webdriver.Chrome: The Chromedriver that is used to automate browser actions
        """
        #/////////////////////////////////////////////////////////////////////////////////////////////////////
        self.username = username
        self.password = password
        self.base_url = "https://www.instagram.com"
        self.driver = webdriver.Chrome('./chromedriver.exe')

        self.login()

    
        
    #LOGIN
    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        self.driver.implicitly_wait(5) #wait 5 second after loading the page, there was a problem when driven.find was faster and never found the element
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(self.username) #finds element in html by Xpath and paste there username
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
        time.sleep(5)

    #NAVIGATE TO USER
    def nav_user(self, user):
        self.driver.get('{}/{}/'.format(self.base_url, user))

    #NAVIGATE TO HASHTAG
    def nav_hashtag(self, hashtag):
        self.driver.get('{}/explore/tags/{}/'.format(self.base_url, hashtag))

    #FOLLOW USER
    def follow_user(self, user):
        self.nav_user(user) 
        time.sleep(3)
        follow_button = self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")[0]
        follow_button.click()

    #LIKE HASHTAG 
    #-- like "count" images of hashtag
    def like_hashtag(self, hashtag, count):
        self.nav_hashtag(hashtag)   #navigate to hashtag page
        
        self.driver.find_elements_by_class_name('_9AhH0')[9].click() #open the most recent photo, 10th photo on the hashtag page

        for x in range(count): #loop liking count photos
            time.sleep(random.randrange(3,7)) 
            try:
                self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click() #click on the like button
                print(x+1, "posts liked")
            except:
                print("Like button not found skipping photo")
                x-=1
                
            self.driver.find_element_by_xpath("//a[contains(text(), 'Next')]").click() #click on the next arrow

        logger.info("Round liked: %d posts", x)
        

#LOGGER CONFIG
logging.basicConfig(filename="test.log", format='%(asctime)s %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.INFO)

#MAIN
if __name__ == '__main__':

    #CONFIGPARSER CONFIG
    config = configparser.ConfigParser()
    config.read('config.ini')

    username = config.get("login","username")
    password = config.get("login","password")

    ig_bot = InstagramBot(username, password) #creating class InstagramBot with username and password parameters Login to account
    logger.info("Logged user: %s", username)

    #INFINITE LOOP FOR PROGRAM
    # parameters are from "config.ini" file
    # liking random pictures of hashtag
    # sleeping for random time interval
    # randomly picking hashtag from list
    while True:

        time_start = time.strptime(config.get("general", "time_start"), '%H:%M').tm_hour
        time_end = time.strptime(config.get("general", "time_end"), '%H:%M').tm_hour
        local_time = time.localtime().tm_hour

        if ((time_start <= local_time) and (local_time <= time_end)):
            #PREPARATION PROCESS
            like_count = int(random.normalvariate(config.getint("like","like_count"), 5)) #generating number of likes
            sleep_time = int(random.normalvariate(config.getint("like","sleep_timer"), 10)) #generating number of sleep seconds
            hashtag = random.choice(ast.literal_eval(config.get("like", "hashtags"))) #randomly picking hashtag from list 
            print("Like count: ", like_count)
            logger.info("Like count: %d", like_count)
            print("Sleep time: ", sleep_time)
            logger.info("Sleep time: %d", sleep_time)
            print("Liking hashtag: ", hashtag)
            logger.info("Liking hashtag: %s", hashtag)
            
            #LIKING PROCESS       
            ig_bot.like_hashtag(hashtag, like_count)
            print("Waiting for ", sleep_time, " seconds till", datetime.timedelta(seconds=sleep_time))
            logger.info("Waiting for %d seconds till %s", sleep_time, str(datetime.timedelta(seconds=sleep_time)))
            time.sleep(sleep_time)
        else:
            pass

    print('SUCCESS')