import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


class TwitterSpider(scrapy.Spider):
    name = 'twitter_spider'
    start_urls = ['https://x.com/KIPPRAKENYA']

    def __init__(self, *args, **kwargs):
        super(TwitterSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get(response.url)

        # Wait for the tweets to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//article[@role="article"]'))
        )

        tweets_data = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            tweets = self.driver.find_elements(By.XPATH, '//article[@role="article"]')

            for tweet in tweets:
                print("tweet >>>>>>", tweets)
                try:
                    tweet_text = tweet.find_element(By.XPATH, './/div[@lang]').text
                    tweet_actions = tweet.find_elements(By.XPATH, './/div[@data-testid="like"]')
                    likes = int(tweet_actions[0].text.replace(",", "")) if tweet_actions and tweet_actions[0].text.isdigit() else 0
                    retweets = int(tweet_actions[1].text.replace(",", "")) if len(tweet_actions) > 1 and tweet_actions[1].text.isdigit() else 0
                    comments = int(tweet_actions[2].text.replace(",", "")) if len(tweet_actions) > 2 and tweet_actions[2].text.isdigit() else 0

                    username = tweet.find_element(By.XPATH, './/div[@dir="ltr"]/span').text
                    date = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')

                    tweets_data.append({
                        'username': username,
                        'tweet': tweet_text,
                        'date': date,
                        'likes': likes,
                        'retweets': retweets,
                        'comments': comments
                    })

                except Exception as e:
                    self.logger.error(f"Error processing tweet: {e}")

            # Scroll down to load more tweets
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        # Save data to CSV
        with open('tweets_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['username', 'tweet', 'date', 'likes', 'retweets', 'comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for tweet in tweets_data:
                writer.writerow(tweet)

        self.driver.quit()
