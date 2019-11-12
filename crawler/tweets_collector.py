import tweepy
from tweepy import OAuthHandler, Stream
from tweets_listener import TweetsListener
import logging
from .. import sqlite_manager


logger = logging.getLogger(__name__)
__author__ = 'noora'


def get_accounts(api, accounts):
    """
    Return the IDs of a given list of screen_names.
    """
	users_ids = []
	for account in accounts:
		try:
			user = api.get_user(screen_name=account)
			if user:
				users_ids.append(str(user.id))
		except tweepy.TweepError as e:
			logging.info('Exception: tweets_collector: {} account: {}'.format(e, account))
			pass
	users_accounts = users_ids
	return users_accounts


def tweets_collector(twitter_key, hashtags, accounts, redis_db, tweets_channel):
	"""
		Listens for ever for tweets about hashtags in keywords and accounts in accounts. Write these tweets to Redis Channel.
		:return: Tweets matching some keywords
	"""
	logging.info('Start tweets collector')
	auth = OAuthHandler(twitter_key['consumer_key'], twitter_key['consumer_secret'])
	auth.set_access_token(twitter_key['access_token'], twitter_key['access_token_secret'])
	api = tweepy.API(auth)

	users_accounts = get_accounts(api, accounts)

	while True:
		logger.warning('Reconnecting to twitter stream after disconnection.')
		try:
			stream_listener = TweetsListener(redis_db, tweets_channel)
			stream = Stream(auth, stream_listener)
			stream.filter(track=hashtags, follow=users_accounts)

		except Exception as e:
			logging.warn('Something went wrong with the listener, the exception is %s' % e)
			continue
