__author__ = 'austin'

import time
import RPi.GPIO as RPIO
from datetime import datetime, timedelta
import twitter
from pop.decorators import async
from pop import consumer_key, consumer_secret, pop_hashtags, mashape_key
import unirest


class AlreadyMakingException(Exception):
    """

    """
    def __init__(self, message, finish_time):
        self.message = message
        self.finish_time = finish_time

    def __str__(self):
        return repr(self.message +
                    "\n There's " + str((self.finish_time - datetime.utcnow()).total_seconds()) + " left!")


class Maker:
    """
        Very Simple Popcorn maker
    """

    is_on = False
    pin_switch = 38
    default_pop_time = 15
    current_pop_time = 15
    start_time = datetime.utcnow()

    def __init__(self):
        """

        :return:
        """
        # Read the pins and figure out if the maker is on
        RPIO.setwarnings(False)
        RPIO.setmode(RPIO.BOARD)
        RPIO.setup(self.pin_switch, RPIO.OUT)
        RPIO.output(self.pin_switch, True)

    @async
    def make_popcorn(self, pop_time=None, on_finish_function=lambda f:None):
        """

        :param pop_time:
        :return:
        """
        if self.is_on:
            raise AlreadyMakingException("Already making popcorn dog",
                                         (self.start_time + timedelta(seconds=self.current_pop_time)))

        self.start()

        if pop_time is None:
            pop_time = self.default_pop_time

        self.current_pop_time = pop_time
        time.sleep(pop_time)
        # Until we do thread stoppin', just check if it was stopped during sleep
        if self.is_on:
            self.stop()
            # How to make this type specific?
            on_finish_function()

    def stop(self):
        """
        :return:
        """
        RPIO.output(self.pin_switch, True)
        self.is_on = False

    def start(self):
        """

        :return:
        """
        RPIO.output(self.pin_switch, False)
        self.is_on = True
        self.start_time = datetime.utcnow()

    def get_status(self):
        if self.is_on:
            return "on"
        else:
            return "off"

    def time_until_done(self):
        """

        :return:
        """
        finish_time = (self.start_time + timedelta(seconds=self.current_pop_time))
        return (finish_time - datetime.utcnow()).total_seconds()

    def is_making(self):
        return self.is_on


class Crawler:
    """

    """
    last_time = datetime.utcnow()
    tweets_crawled = 0
    times_crawled = 0
    found_pop_command = False
    crawl_time = 5
    running = False
    command_data = {}
    found_function = lambda f: None

    def __init__(self, access_token_key=None, access_token_secret=None, crawl_time=5,
                 found_function=lambda f: None):
        """
            Just setup the twitter api for now
        :return:
        """
        if access_token_key is None:
            access_token_key = '4245114382-F525Tzwz4TWq3OdIskSV3u9OBqCiLlxpkU5MmZS'

        if access_token_secret is None:
            access_token_secret = 'HoeolGuwgEOTdFS2H0CASluZixWzq2KzBle0bK6kgfvl5'

        self.twitter_api = twitter.Api(consumer_key=consumer_key,
                                       consumer_secret=consumer_secret,
                                       access_token_key=access_token_key,
                                       access_token_secret=access_token_secret)
        user = self.twitter_api.VerifyCredentials()
        self.username = user.GetScreenName()
        self.found_pop_command = False
        self.crawl_time = crawl_time
        self.found_function = found_function

    def stop(self):
        self.running = False

    # @async
    def crawl(self):
        """

        :return:
        """

        self.running = True

        while self.running:
            self.found_pop_command = False
            last_tweets = self.twitter_api.GetUserTimeline(self.username,
                                                           count=5,
                                                           include_rts=False,
                                                           exclude_replies=True)
            for tweet in last_tweets:
                tweet_time = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y")
                if tweet_time > self.last_time:
                    # Analyze the tweet
                    for tag in tweet.hashtags:
                        if tag.text in pop_hashtags:
                            print "Found a pop-able tweet!"
                            self.last_time = tweet_time
                            self.make_pop_command(tweet)
                            self.found_pop_command = True
                            self.found_function()

                self.tweets_crawled += 1
            self.times_crawled += 1
            print "Done crawl number: " + str(self.times_crawled)
            time.sleep(self.crawl_time)
        print "Done crawling after " + str(self.times_crawled) + " crawls. Phewf."

    def found_pop(self):
        return self.found_pop_command

    def make_pop_command(self, tweet):
        """

        :return:
        """
        # Let's try to get how good they're feeling
        print tweet.text
        sentiment_data = {'language': 'english', 'text': tweet.text}
        sentiment_headers = {
            "X-Mashape-Key": mashape_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
                                headers=sentiment_headers,
                                params=sentiment_data)
        print response.body['label']

        self.command_data = {'sentiment': response.body['label']}

    def get_pop_command(self):
        return self.command_data

    def get_num_tweets_crawled(self):
        return self.tweets_crawled


class Robot:
    """
        A wrapper for commanding the Roomba sooper cool deliver system

        Current Command format:
        {
            action: stay, deliver, comeback
            message: a message to the popcorn getter
            # music: url to music to play ??
        }
    """
    action = "stay"

    def __init__(self, message="Sup dog, here's some popcorn"):
        self.message = message

    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def current_command(self):
        """

        :return:
        """
        return {'message': self.message, 'action': self.action}

    def set_home(self):
        """

        :return:
        """
        self.action = "stay"
        self.message = "Turn down on a Tuesday"

    def come_back(self, message=None):
        """
            Send a push notification to return to the base station
        :return:
        """
        self.action = "deliver"
        if message is not None:
            self.message = message
        print "Coming home!"

    def deliver(self, message=None):
        """
            Send a push notification to go search out the person
        :return:
        """
        self.action = "deliver"
        if message is not None:
            self.message = message
        print "Delivering: " + self.get_message()

