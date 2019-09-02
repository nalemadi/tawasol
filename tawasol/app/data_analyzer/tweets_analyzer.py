from ..utils.text_operations import simple_clean_text, simple_clean_text_ar
import logging
from ..config.dashboard_config import NBR_HAHSTAGS, NBR_IMAGES
from collections import defaultdict, Counter
from tweet import Tweet
from datetime import datetime
from text_analyzer import TextAnalyzer
from time_analyzer import TimeAnalyzer
from pytz import timezone
from ..utils.consts import langs_dict

logging.getLogger().setLevel(logging.INFO)


class TweetsAnalyzer(TextAnalyzer, TimeAnalyzer):

    def __init__(self):
        self.collection = None
        self.categories = set()
        self.time_slots = []
        self.users_distribution = defaultdict(set)
        self.tweets_distribution = defaultdict(set)
        self.tweets_sentiment = defaultdict(lambda: defaultdict(int))
        self.tweets_happiness = {}
        self.language_distribution = defaultdict(int)
        self.hashtags = defaultdict(int)
        # self.images = []
        #self.users_graph_nodes = defaultdict()
        #self.gender_distribution = {'female': 0, 'male': 0}
        #self.community_graph = {'nodes': [], 'links': []}
        #self.users_graph_links = set()
        self.start_time = datetime.utcnow()

    def process_tweet(self, tweet, users_dict):
        """
        assign tweet to tawasol_user
        :param tweet:
        :return: tweet object with extra info
        """
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

        tweet['emotion'] = self.get_emotion(tweet_text, tweet['lang'])
        tweet['sentiment'] = self.get_sentiment_sentistrength(tweet_text, tweet['lang'])

        # Convert datetime
        tweet['created_at'] = self.to_datetime(tweet['created_at']).replace(tzinfo=timezone('GMT'))

        tweet_user = tweet['user']['screen_name']
        users_list = []
        for key, value in users_dict.iteritems():
            key_broken = key.split('@')
            user_name = key_broken[0]

            keywords = value['keywords']
            for keyword in keywords:
                if keyword in tweet_text_broken:
                    logging.info('keyword found: {} in tweet_text for {}'.format(keyword, user_name))
                    users_list.append(user_name)

            #check accounts
            accounts = value['accounts']
            for account in accounts:
                if account.lower() == tweet_user.lower():
                    logging.info('account found for: %s' % user_name)
                    users_list.append(user_name)

        return tweet, users_list

    def generate_tweet_with_timeIndex(self, tweet):
        is_string = isinstance(tweet['created_at'], basestring)
        if is_string:
            tweet_date = self.to_datetime(tweet['created_at'])
        else:
            tweet_date = tweet['created_at']
        time_index = self.get_time_index(tweet_date, self.time_slots)
        result_tweet = Tweet(tweet, time_index)
        return result_tweet

    def get_language_dist(self, lang_list, limit=7):
        lst_lang_top = sorted(lang_list, key=lambda x:x[1], reverse=True)[:limit]
        others_lang_freq = sum([x[1] for x in sorted(lang_list, key=lambda x:x[1], reverse=True)[limit:]])
        return map(list, lst_lang_top) + [['other', others_lang_freq]]

    def get_tweets_summary_report(self):
        """
        get summary of all tweets statistics
        :return: dictionary for all tweets statistics
        """
        logging.info('Generating Tweets Report')
        result = dict()

        # Categories
        result['categories'] = sorted(self.categories)

        # Tweets Sentiment
        result['positive'] = [self.tweets_sentiment[x].get('positive', 0) for x in self.categories]
        result['negative'] = [self.tweets_sentiment[x].get('negative', 0) for x in self.categories]
        result['neutral'] = [self.tweets_sentiment[x].get('neutral', 0) for x in self.categories]

        # Nbr of tweets/users
        result['nbr_users'] = sum([len(list(self.users_distribution[x])) for x in self.categories])
        result['nbr_tweets'] = sum([len(list(self.tweets_distribution[x])) for x in self.categories])

        # Happiness Chart
        result['happiness'] = [self.get_emotion(' '.join(list(self.tweets_distribution[x])), lang='en') for x in self.categories]

        # Users Chart
        result['users'] = [len(list(self.users_distribution[x])) for x in self.categories]

        # Hashtags Chart
        users_hashtags = [{'text': hashtag, 'weight': freq, 'link': '%s%s' % ('https://twitter.com/hashtag/', hashtag)} for hashtag, freq in self.hashtags.iteritems()]
        result['hashtags'] = sorted(users_hashtags, key=lambda x:x['weight'], reverse=True)[:NBR_HAHSTAGS]

        # # Language
        lst_lang = [[langs_dict.get(k,k),v] for k,v in self.language_distribution.items()]
        result['language'] = self.get_language_dist(lst_lang)

        # Images
        # result['images'] = self.images[(-1)*NBR_IMAGES:]

        # # Gender Distribution
        # result['gender'] = [['Female', self.gender_distribution['female']],['Male', self.gender_distribution['male']]]

        # # Community Graph
        # result['community_graph'] = {'nodes': self.users_graph_nodes, 'links': []}

        try:
            if len(self.tweets_distribution.keys()) > 0:
                result['tweets'] = [tweet for tweet in self.tweets_distribution[max(self.tweets_distribution.keys())]] # [(-1)*NBR_TWEETS:]
            else:
                result['tweets'] = []

        except Exception as e:
            result['tweets'] = []
            # print 'error get_tweets_summary_report', e


        # top_users
        if len(result['tweets']) is not 0:
            # [tweet.tweet_text, '-- @' + tweet.screen_name, tweet_date.strftime('%Y-%m-%dT%H:%M:%S'), str(tweet.tweet_coor)]
            tweets = result['tweets']
            users = []
            tweets_arr = []
            for tweet in tweets:
                broken = tweet.split('-- ')
                tweet_text = broken[0]
                tweets_arr.append(tweet_text)
                userscreen = broken[1].split('\n')[0]
                #print '===userscreen==', userscreen
                users.append(userscreen)
            counter_users = Counter(users)
            users_count = [{'text': username, 'weight': freq, 'link': '%s%s' % ('https://twitter.com/', username.split('@')[1])} for username, freq in counter_users.iteritems()]
            result['top_users'] = sorted(users_count, key=lambda x: x['weight'], reverse=True)[:10]
            #
            counter_tweets = Counter(tweets_arr)
            tweets_count = [{'text': tweet_txt, 'weight': freq} for tweet_txt, freq in counter_tweets.iteritems()]
            result['top_tweets'] = sorted(tweets_count, key=lambda x:x['weight'], reverse=True)[:10]

        return result

    def populate_tweets(self, tweet):
        # time_index
        self.categories.add(tweet.time_index)

        # # Gender
        # if tweet.gender is not None:
        # 	self.gender_distribution[tweet.gender] += 1

        # Language
        self.language_distribution[tweet.lang] += 1

        # Sentiment
        self.calculate_sentiment_dist(tweet.time_index, tweet.sentiment_score)

        # User distribution
        self.users_distribution[tweet.time_index].add(tweet.screen_name)

        # Tweet distribution
        is_string = isinstance(tweet.created_at, basestring)
        if is_string:
            tweet_date = self.to_datetime(tweet.created_at)
        else:
            tweet_date = tweet.created_at
        self.tweets_distribution[tweet.time_index].add('\n'.join([tweet.tweet_text, '-- @' + tweet.screen_name, tweet_date.strftime('%Y-%m-%dT%H:%M:%S'), str(tweet.tweet_coor)]))

        # Used hashtags
        for hashtag in tweet.hashtags:
            self.hashtags[hashtag] += 1

        # add images
        # self.images += tweet.tweet_images

        # graph nodes
        # if self.users_graph_nodes.get(tweet.tweet_id, None) is None:
        # 	self.users_graph_nodes[tweet.screen_name] = tweet.user_profile
        # else:
        # 	self.users_graph_nodes[tweet.screen_name]['frequency'] += 1
        #
        # for user in self.get_mentioned_users(tweet.tweet_text):
        # 	self.users_graph_links.add((user, tweet.screen_name))

    def calculate_sentiment_dist(self, date_index, sentiment_score):
        """
        calculate sentiment distribution in date index
        :param date_index: date
        :param sentiment_score: int
        :return:
        """
        # tweet sentiment
        if self.tweets_sentiment.get(date_index, None) is None:
            self.tweets_sentiment[date_index] = {'negative': 0, 'positive': 0, 'neutral': 0 }

        if sentiment_score < 0:
            self.tweets_sentiment[date_index]['negative'] += 1
        elif sentiment_score > 0:
            self.tweets_sentiment[date_index]['positive'] += 1
        else:
            self.tweets_sentiment[date_index]['neutral'] += 1

    def get_analyzed_tweets(self, tweets):
        """
        :param tweets:
        :return:
        """
        self.time_slots = self.get_all_timeslots()
        # This is iterating over PyMongoDB cursor.
        n = 0
        for tweet in tweets:
            # Assign a tweet to a time slot
            result_tweet = self.generate_tweet_with_timeIndex(tweet)
            # Update all reports: e.g., gender distribution, user distribution, etc.
            self.populate_tweets(result_tweet)
            n += 1
        result = self.get_tweets_summary_report()
        return result, n
