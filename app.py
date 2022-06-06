import markovify
import tweepy
import os
from dotenv import load_dotenv
import re
import time

load_dotenv()

tweets = []
auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_KEY_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'],
                      os.environ['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)


def send_tweets():

    for message in tweepy.Cursor(api.user_timeline, id=os.environ['TWITTER_ID'], include_rts=False, exclude_replies=True).items():
        tweets.append(message.text.lower())

    tweets_joined = ' '.join(tweets)

    tweets_joined = re.sub(r'http\S+', '', tweets_joined)
    tweets_joined = re.sub(r'@(?<=@)\w+', '', tweets_joined)

    text_model = markovify.Text(tweets_joined)

    tweets_generated = [
        text_model.make_short_sentence(280) for x in range(0, 4)]

    for message in tweets_generated:
        api.update_status(status=message)
        time.sleep(60*15)  # 15 minutes


while True:
    send_tweets()
    time.sleep(60*75)  # 60 minutes
