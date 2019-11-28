
class Tweet():

	def __init__(self, tweet, time_index):
		self.tweet_id = int(tweet['id'])

		# time / time index
		self.created_at = tweet['created_at']
		self.time_index = time_index

		if 'gender' in tweet:
			self.gender = tweet['gender']
		else:
			self.gender = None

		# name
		self.names = tweet['user']['name'].split(' ')

		# lang
		self.lang = tweet['lang']

		# tweet text
		if 'retweeted_status' in tweet:
			if 'extended_tweet' in tweet['retweeted_status']:
				tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
			else:
				tweet_text = tweet['text']
		else:
			tweet_text = tweet['text']
		self.tweet_text = tweet_text

		# screen name
		self.screen_name = tweet['user']['screen_name']

		# sentiment
		self.sentiment_score = tweet['sentiment']

		# hashtags
		self.hashtags = [x.get(u'text') for x in tweet.get('entities').get('hashtags')]

		# user info
		self.user_info = {'user_id': tweet['user']['id_str'], 'account_creation':tweet['user']['created_at']}

		# mentions
		self.mentions = [x['screen_name'] for x in tweet['entities']['user_mentions']]

		# tweet emotion
		self.emotion_score = tweet['emotion']
