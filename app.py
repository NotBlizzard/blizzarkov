import markovify
import tweepy
from dotenv import load_dotenv
import re


load_dotenv()

auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_KEY_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'],
                      os.environ['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)


def send_tweets():
    tweets = []
    for message in tweepy.Cursor(api.user_timeline, id=os.environ['TWITTER_ID'], include_rts=False, exclude_replies=True).items():
        tweets.append(message.text.lower())

    tweets_joined = ' '.join(tweets)

    tweets_joined = re.sub(r'http\S+', '', tweets_joined)
    tweets_joined = re.sub(r'@(?<=@)\w+', '', tweets_joined)

    text_model = markovify.Text(tweets_joined)

    message = text_model.make_short_sentence(280, tries=100)
    api.update_status(status=message)

send_tweets()

