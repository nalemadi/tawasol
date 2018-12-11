from tweepy.streaming import StreamListener
import json


class TweetsListener(StreamListener):

    def __init__(self, redis_db, tweets_channel):
        super(StreamListener, self).__init__()

        self.redis_db = redis_db
        self.redis_channel = tweets_channel

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            if tweet['text']:
                self.redis_db.rpush(self.redis_channel, json.dumps(tweet))
        except Exception, e:
            pass

    def on_error(self, status):
        print 'Error in twitter listener, status:', status
        pass
