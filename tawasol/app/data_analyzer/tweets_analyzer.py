from ..utils.text_operations import simple_clean_text, simple_clean_text_ar
import logging
logging.getLogger().setLevel(logging.INFO)


class TweetsAnalyzer():

	def __init__(self):
		return None

	def process_tweet(self, tweet, users_dict):
		"""
		assign tweet to tawasol_user
		:param tweet:
		:return: tweet object with extra info
		"""
		tweet_text = ''
		logging.info('=== TweetsAnalyzer: process tweet ===')
		if 'retweeted_status' in tweet.keys():
			if 'extended_tweet' in tweet['retweeted_status'].keys():
				tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
			else:
				tweet_text = tweet['text']
		else:
			tweet_text = tweet['text']

		if tweet['lang'] == 'ar':
			tweet_text_broken = simple_clean_text_ar(tweet_text)
		else:
			tweet_text_broken = simple_clean_text(tweet_text)

		#print tweet_text_broken
		user_name = ''
		tweet_user = tweet['user']['screen_name']
		collections = []
		for key, value in users_dict.iteritems():
			key_broken = key.split('@')
			user_name = key_broken[0]

			keywords = value['keywords']
			for keyword in keywords:
				if keyword in tweet_text_broken:
					logging.info('keyword found: {} in tweet_text for {}'.format(keyword, user_name))
					collections.append(user_name+'_tweets')

			#check accounts
			accounts = value['accounts']
			for account in accounts:
				if account.lower() == tweet_user.lower():
					logging.info('account found for: %s' % user_name)
					collections.append(user_name + '_tweets')

		return tweet, collections, user_name
