from ..utils.text_operations import simple_clean_text, simple_clean_text_ar


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
		print '=== process tweet ==='
		if 'retweeted_status' in tweet.keys():
			if 'extended_tweet' in tweet['retweeted_status'].keys():
				#print 'this tweet has extended text'
				tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
			else:
				tweet_text = tweet['text']
		else:
			tweet_text = tweet['text']

		if tweet['lang'] == 'ar':
			tweet_text_broken = simple_clean_text_ar(tweet_text)
		else:
			tweet_text_broken = simple_clean_text(tweet_text)
		#print 'tweet text: ', tweet_text.encode('utf-8')
		#tweet_text_broken = simple_clean_text(tweet_text)
		#print 'tweet text broken', tweet_text_broken#[x.decode("unicode_escape").encode("utf-8") for x in tweet_text_broken]
		print tweet_text_broken
		tweet_user = tweet['user']['screen_name']
		collections = []
		for key, value in users_dict.iteritems():
			key_broken = key.split('@')
			user_name = key_broken[0]

			keywords = value['keywords']
			for keyword in keywords:
				if keyword in tweet_text_broken:
					print 'keyword found:', keyword, ' in tweet_text for', user_name
					collections.append(user_name+'_tweets')

			#check accounts
			accounts = value['accounts']
			for account in accounts:
				if account.lower() == tweet_user.lower():
					print 'account found'
					collections.append(user_name + '_tweets')

		return tweet, collections
