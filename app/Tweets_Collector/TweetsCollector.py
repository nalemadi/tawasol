from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from app import twitter_keys
import json
import logging


logger = logging.getLogger(__name__)
__author__ = 'noora'


class TweetsCollector(StreamListener):

	def __init__(self):
		self.twitter_key = twitter_keys

	def get_tweets(self):
		"""
		Listens for ever for tweets about keywords in self.keywords. Write these tweets to Redis Channel.
		:return: Tweets matching some keywords
		"""
		auth = OAuthHandler(self.twitter_key['consumer_key'], self.twitter_key['consumer_secret'])
		auth.set_access_token(self.twitter_key['access_token'], self.twitter_key['access_token_secret'])
		while True:
			logger.warning('Reconnecting to twitter stream after disconnection.')
			try:
				sapi = Stream(auth, self)
				sapi.filter(track=self.keywords)
			except Exception as e:
				logger.error('Something went wrong with the listener, the exception is: %s', e)
				continue

	def on_data(self, data):

		# push data to redis queue
		try:
			o = json.loads(data)
			if not o['text']:
				logger.warning('Tweepy returned a non Tweet object: %s', data)
			return True
		except ValueError, e:
			return False

	def on_error(self, status):
		logger.error("Error in twitter listener, status: %s", status)
