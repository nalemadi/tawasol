from tweepy import OAuthHandler, Stream, TweepError, API
from tweepy.streaming import StreamListener
import json
import datetime
import time
import logging

logger = logging.getLogger(__name__)
__author__ = 'noora'


class TweetsCollector(StreamListener):

	def __init__(self, redis_db, tweets_channel, twitter_key, accounts, hashtags):
		super(StreamListener, self).__init__()
		self.redis_db = redis_db
		self.tweets_channel = tweets_channel
		self.twitter_key = twitter_key
		self.accounts = accounts
		self.hashtags = hashtags
		self.tweets_collector()

	def on_data(self, data):
		try:
			tweet = json.loads(data)
			if tweet['text']:
				self.redis_db.rpush(self.tweets_channel, json.dumps(tweet))
		except Exception as e:
			pass

	def on_error(self, status):
		logging.warn('Error in twitter listener, status: %s' % status)
		if status == 420:
			logging.info('Rate Limit!! ... sleep from 15 minutes, %s' % datetime.datetime.now())
			time.sleep(900)  # 15 minutes

	def get_accounts(self):
		"""
		Return the IDs of a given list of screen_names.
		"""
		users_ids = []
		for account in self.accounts:
			try:
				user = self.api.get_user(screen_name=account)
				if user:
					users_ids.append(str(user.id))
			except TweepError as e:
				logging.info('Exception: tweets_collector: {} account: {}'.format(e, account))
				pass
		users_accounts = users_ids
		return users_accounts

	def tweets_collector(self):
		"""
		Listens for ever for tweets about hashtags in keywords and accounts in accounts. Write these tweets to Redis Channel.
		:return: Tweets matching some keywords
		"""
		logging.info('Start tweets collector')
		auth = OAuthHandler(self.twitter_key['consumer_key'], self.twitter_key['consumer_secret'])
		auth.set_access_token(self.twitter_key['access_token'], self.twitter_key['access_token_secret'])
		#self.api = API(auth)

		#users_accounts = self.get_accounts()
		users_accounts = []

		while True:
			logger.warning('Reconnecting to twitter stream after disconnection.')
			try:
				#stream_listener = TweetsCollector(self.redis_db, self.tweets_channel)
				stream = Stream(auth, self)
				stream.filter(track=self.hashtags, follow=users_accounts)

			except Exception as e:
				logging.warn('Something went wrong with the listener, the exception is %s' % e)
				continue
