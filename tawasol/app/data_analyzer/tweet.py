
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
        self.tweet_text = tweet['text']

        # screen name 
        self.screen_name = tweet['user']['screen_name']

        # sentiment
        self.sentiment_score = tweet.get('sentiment', None)

        # hashtags 
        self.hashtags = [x.get(u'text') for x in tweet.get('entities').get('hashtags')]


        # user profile 
        self.user_profile = {'frequency': 1, 'uid': self.tweet_id, 'user_bio': tweet['user']['description'], 'user_img': tweet['user']['profile_image_url'], 'user_name': self.screen_name}

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