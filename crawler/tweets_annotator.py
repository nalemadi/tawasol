import re
import logging
import shlex
from pytz import timezone
from models.genderizer.genderizer_client import Genderizer
from labMTsimple.storyLab import emotionFileReader, emotion, stopper, emotionV, subprocess

logging.getLogger().setLevel(logging.INFO)

# model to infer whether the user is male/female
genderizer = Genderizer(male_fname='./data/male.txt', female_fname='./data/female.txt')
labMT_eng, labMTvector_eng, labMTwordList_eng = emotionFileReader(stopval=0.0, lang='english', returnVector=True)
labMT_ar, labMTvector_ar, labMTwordList_ar = emotionFileReader(stopval=0.0, lang='arabic', returnVector=True)

# Sentiment model
senti_server_location = 'models'
process = subprocess.Popen(shlex.split(
    "java -jar {}/SentiStrength.jar stdin sentidata {}/SentStrength_Data/ trinary".format(senti_server_location,
                                                                                          senti_server_location)),
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class TweetsAnnotator:

    def __init__(self):
        pass

    def process_tweet(self, tweet, users_dict):
        """
        It parses a tweet and generated a set of new attributes related to
        sentiment, gender, etc. It also returns the list of users for this
        tweet.
        :param tweet: the input tweet in json format
        :param  users_dict: a dictionary of users:hashtags/accounts. Used to
        identify owners of the tweet.
        :return: tweet object with extra info, plus list of users oweners of
        this tweet.
        """

        logging.info('=== TweetsAnalyzer: process tweet ===')
        # TODO: Noora, why are we doing this for tweets with retweeted_status only?
        # to get full text of retweeted tweet
        if 'retweeted_status' in tweet:
            if 'extended_tweet' in tweet['retweeted_status']:
                tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
            else:
                tweet_text = tweet['text']
        else:
            tweet_text = tweet['text']

        # list of tweet text words
        tweet_text_arr = self.get_clean_text_list(tweet_text, tweet['lang'])

        # Convert datetime
        tweet['created_at'] = self.to_datetime(tweet['created_at']).replace(tzinfo=timezone('GMT'))
        
        # Sentiment/emotion
        tweet['emotion'] = self.get_emotion(tweet_text, tweet['lang'])
        tweet['sentiment'] = self.get_sentiment_sentistrength(tweet_text)

        # gender
        names = tweet['user']['name'].split(' ')
        if names:
            tweet['gender'] = genderizer.infer_gender(names[0])

        tweet_user = tweet['user']['screen_name']
        users_list = []
        # Users of the app are identified using emails with @ character.
        for key, value in users_dict.iteritems():
            user_name = key.split('@')[0]
            keywords = value['keywords']
            for keyword in keywords:
                if keyword in tweet_text_arr:
                    logging.info('keyword found: {} in tweet_text for {}'.format(keyword, user_name))
                    users_list.append(user_name)
                    break

            #check accounts
            accounts = value['accounts']
            for account in accounts:
                if account.lower() == tweet_user.lower():
                    logging.info('account found for: %s' % user_name)
                    users_list.append(user_name)

        return tweet, users_list

    def get_clean_text_list(self, text, lang):
        """
        this method clean tweet text from URLs and puctuations, then retrun list of tweet text words
        :param text: tweet text
        :return: words list
        """
        # 1. remove urls
        text = re.sub(r"http\S+", "", text)
        # 2. remove puctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        if lang == 'ar':
            text = re.sub(r'[\u0600 -\u06FF]+', '', text)
        else:
            text = re.sub(r'[^\w\s]', '', text)
        text_broken = text.lower().strip().split(' ')
        return text_broken

    def get_emotion(self, text, lang):
        """
        calculate the emotion of text using LabMT
        :param text: str
        :param lang: str
        :return: a score between 0 and 9.
        """
        if lang == 'ar':
            valence, fvec = emotion(text, labMT_ar, shift=True, happsList=labMTvector_ar)
            stoppedVec = stopper(fvec, labMTvector_ar, labMTwordList_ar, stopVal=1.0)
            valence = emotionV(stoppedVec, labMTvector_ar)
            if valence == -1:
                return 0
            else:
                return valence
        elif lang == 'en':
            valence, fvec = emotion(text, labMT_eng, shift=True, happsList=labMTvector_eng)
            stoppedVec = stopper(fvec, labMTvector_eng, labMTwordList_eng, stopVal=1.0)
            valence = emotionV(stoppedVec, labMTvector_eng)
            if valence == -1:
                return 0
            else:
                return valence
        else:
            return 0

    def get_sentiment_sentistrength(self, text):
        """
        calculate the sentiment score
        :param text: str
        :param lang: str
        :return: sentiment score
        """
        text = text.encode('utf8')
        stdout_text, stderr_text = process.communicate(text.replace(" ", "+"))
        try:
            result = int(float(stdout_text.rstrip().split(' ')[-1]))
            return result
        except Exception as e:
            logging.info('Exception: get_sentiment_sentistrength')
            return 0
