from time_analyzer import TimeAnalyzer
from text_analyzer import TextAnalyzer

text_analyzer = TextAnalyzer()
time_analyzer = TimeAnalyzer()


class Tweet():
	def __init__(self, tweet, time_index):
		self.tweet_id = int(tweet['id'])

		# time / time index
		self.created_at = tweet['created_at']
		self.time_index = time_index

		# name
		self.names = tweet['user']['name'].split(' ')

		# lang
		self.lang = tweet['lang']

		# tweet text
		#self.tweet_text = tweet['text']
		if 'retweeted_status' in tweet.keys():
			if 'extended_tweet' in tweet['retweeted_status'].keys():
				tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
			else:
				tweet_text = tweet['text']
		else:
			tweet_text = tweet['text']
		self.tweet_text = tweet_text

		# screen name
		self.screen_name = tweet['user']['screen_name']

		# sentiment
		if 'sentiment' not in tweet.keys():
			tweet['sentiment'] = text_analyzer.get_sentiment_sentistrength(tweet_text, tweet['lang'])
			self.sentiment_score = tweet.get('sentiment', None)
		else:
			self.sentiment_score = tweet.get('sentiment', None)

		# hashtags
		self.hashtags = [x.get(u'text') for x in tweet.get('entities').get('hashtags')]

		# user profile
		self.user_profile = {'frequency': 1, 'uid': self.tweet_id, 'user_bio': tweet['user']['description'], 'user_img': tweet['user']['profile_image_url'], 'user_name': self.screen_name}

		# tweet emotion
		if 'emotion' not in tweet.keys():
			tweet['emotion'] = text_analyzer.get_emotion(tweet_text, tweet['lang'])
			self.emotion_score = tweet['emotion']
		else:
			self.emotion_score = tweet['emotion']

		# list of mentioned users
		self.lst_mentioned_usrs = text_analyzer.get_mentioned_users(tweet['text'])

		# tweet emotion
		self.emotion_score = tweet['emotion']

		# Get images
		if tweet.get('entities',{}).get('media',None):
			if tweet['coordinates'] is not None:
				self.tweet_images = [t.get(u'media_url') for t in tweet.get('entities',{}).get('media',{})]
			else:
				self.tweet_images = []
		else:
			self.tweet_images = []