from tweepy.streaming import StreamListener
from tawasol.app import twitter_keys
import json
import logging


logger = logging.getLogger(__name__)
__author__ = 'noora'


class TweetsCollector(StreamListener):

	def __init__(self):
		self.twitter_key = twitter_keys

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