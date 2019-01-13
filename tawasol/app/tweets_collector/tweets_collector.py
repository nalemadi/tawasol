import tweepy
from tweepy import OAuthHandler, Stream
from tweets_listener import TweetsListener
import logging
from .. import sqlite_manager


logger = logging.getLogger(__name__)
__author__ = 'noora'


def get_accounts(api, accounts):
	users_ids = []
	for account in accounts:
		db_user_ids = sqlite_manager.get_userID_from_account(account)
		db_user_id = db_user_ids[0][0]
		if db_user_id:
			users_ids.append(str(db_user_id))
		else:
			try:
				user = api.get_user(screen_name=account)
				if user:
					# insert to sqlite
					sqlite_manager.insert_userID_into_accounts(user.id, account)
					users_ids.append(str(user.id))
			except tweepy.TweepError as e:
				print 'tweets_collector:', e, 'account: ', account
				pass
	###
	users_accounts = ','.join(users_ids)
	return users_accounts


def tweets_collector(twitter_key, hashtags, accounts, redis_db, tweets_channel):
	print 'tweets collector'
	"""
	Listens for ever for tweets about hashtags in keywords and accounts in accounts. Write these tweets to Redis Channel.
	:return: Tweets matching some keywords
	"""
	auth = OAuthHandler(twitter_key['consumer_key'], twitter_key['consumer_secret'])
	auth.set_access_token(twitter_key['access_token'], twitter_key['access_token_secret'])
	api = tweepy.API(auth)

	users_accounts = get_accounts(api, accounts)

	while True:
		logger.warning('Reconnecting to twitter stream after disconnection.')
		try:
			stream_listener = TweetsListener(redis_db, tweets_channel)
			stream = Stream(auth, stream_listener)
			#hashtags='qatar'
			stream.filter(track=hashtags,follow=users_accounts)#, follow=accounts)#,track=self.users_name)

		except Exception as e:
			print 'Something went wrong with the listener, the exception is:', e
			continue
