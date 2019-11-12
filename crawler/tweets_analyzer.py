from ..utils.text_operations import simple_clean_text, simple_clean_text_ar
import logging
from ..config.dashboard_config import NBR_HAHSTAGS, NBR_IMAGES
from collections import defaultdict, Counter
from tweet import Tweet
from datetime import datetime
from text_analyzer import TextAnalyzer
from time_analyzer import TimeAnalyzer
from pytz import timezone
from ..utils.consts import langs_dict
from app.models.genderizer.genderizer_client import *

logging.getLogger().setLevel(logging.INFO)

# model to infer whether the user is male/female
genderizer = Genderizer(male_fname='./data/male.txt', female_fname='./data/female.txt')


class TweetsAnalyzer(TextAnalyzer, TimeAnalyzer):

    def __init__(self):
        self.collection = None
        self.time_indexes = set()
        self.time_slots = []
        self.users_distribution = defaultdict(set)
        self.tweets_distribution = defaultdict(set)
        self.tweets_text = defaultdict(set)
        self.language_distribution = defaultdict(int)
        self.hashtags = defaultdict(int)
        self.mentions = defaultdict(int)
        self.top_users = defaultdict(int)
        self.gender_distribution = {'female': 0, 'male': 0}
        self.start_time = datetime.utcnow()
        self.users_profile = dict()
        self.user_cat = dict()
        self.accounts_creation = {'Week': 0, 'Month': 0, '3-Months': 0, '6-Months': 0, 'Year': 0, '+Year': 0}
        self.accounts_tweets_counter = {'Week': 0, 'Month': 0, '3-Months': 0, '6-Months': 0, 'Year': 0, '+Year': 0}
        self.account_age_cat = ['Week', 'Month', '3-Months', '6-Months', 'Year', '+Year']

    def process_tweet(self, tweet, users_dict):
        """
        It parses a tweet and generated a set of new attributes related to
        sentiment, gender, etc. It also returns the list of users for this
        tweet.
        :param tweet: the input tweet in json format
        :param  users_dict: a dictionary of users:hashtags/accounts. Used to
        identify owners of the tweet.
        :return: tweet object with extra info, plus list of users oweners of
        this tweet.
        """

        logging.info('=== TweetsAnalyzer: process tweet ===')
        # TODO: Noora, why are we doing this for tweets with retweeted_status
        # only?
        if 'retweeted_status' in tweet:
            if 'extended_tweet' in tweet['retweeted_status']:
                tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
            else:
                tweet_text = tweet['text']
        else:
            tweet_text = tweet['text']

        if tweet['lang'] == 'ar':
            tweet_text_broken = simple_clean_text_ar(tweet_text)
        else:
            tweet_text_broken = simple_clean_text(tweet_text)

        # Convert datetime
        tweet['created_at'] = self.to_datetime(tweet['created_at']).replace(tzinfo=timezone('GMT'))
        
        # Sentiment/emotion
        tweet['emotion'] = self.get_emotion(tweet_text, tweet['lang'])
        tweet['sentiment'] = self.get_sentiment_sentistrength(tweet_text, tweet['lang'])

        # gender
        names = tweet['user']['name'].split(' ')
        if names:
            tweet['gender'] = genderizer.infer_gender(names[0])

        tweet_user = tweet['user']['screen_name']
        users_list = []
        # Users of the app are identified using emails with @ character.
        for key, value in users_dict.iteritems():
            key_broken = key.split('@')
            user_name = key_broken[0]
            keywords = value['keywords']
            for keyword in keywords:
                if keyword in tweet_text_broken:
                    logging.info('keyword found: {} in tweet_text for {}'.format(keyword, user_name))
                    users_list.append(user_name)
                    break

            #check accounts
            accounts = value['accounts']
            for account in accounts:
                if account.lower() == tweet_user.lower():
                    logging.info('account found for: %s' % user_name)
                    users_list.append(user_name)

        return tweet, users_list

