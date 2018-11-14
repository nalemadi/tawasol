from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import json
import logging


logger = logging.getLogger(__name__)
__author__ = 'noora'


class TweetsCollector(StreamListener):

	def __init__(self, twitter_keys, hashtags, accounts, redis_db, tweets_channel):
		self.twitter_key = twitter_keys
		self.redis_db = redis_db
		self.redis_channel = tweets_channel
		self.keywords = hashtags
		self.accounts = accounts

	def get_tweets(self):
		"""
		Listens for ever for tweets about hashtags in self.keywords and accounts in self.accounts. Write these tweets to Redis Channel.
		:return: Tweets matching some keywords
		"""
		auth = OAuthHandler(self.twitter_key['consumer_key'], self.twitter_key['consumer_secret'])
		auth.set_access_token(self.twitter_key['access_token'], self.twitter_key['access_token_secret'])
		while True:
			logger.warning('Reconnecting to twitter stream after disconnection.')
			try:
				sapi = Stream(auth, self)
				sapi.filter(track=self.keywords, follow=self.accounts)#,track=self.users_name)
			except Exception as e:
				logger.error('Something went wrong with the listener, the exception is: %s', e)
				continue

	def on_data(self, data):
		# push data to redis queue
		try:
			tweet = json.loads(data)
			self.redis_db.rpush(self.redis_channel, json.dumps(tweet))
			return True
		except ValueError, e:
			return False

	def on_error(self, status):
		logger.error("Error in twitter listener, status: %s", status)
