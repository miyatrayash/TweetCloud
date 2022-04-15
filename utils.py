from email import header
from urllib import request, response
import requests
from config import Config
import string

from nltk.corpus import stopwords
from nltk import download
from nltk.tokenize import word_tokenize

download('stopwords')
download('punkt')

remove_word_set = set(stopwords.words()).union(set(string.punctuation))
headers = {'Authorization': f'Bearer {Config.TW_BEARER_TOKEN}'}

def get_tweet_details(username):
    try:
        data = requests.get(f"{Config.TW_BASE_URL}/users/by/username/{username}", headers=headers).json()
        userid = data['data']['id']
    except Exception as e:
        return False, "Can't find tweets for you :(", None, None
    try:
        response = requests.get(f"{Config.TW_BASE_URL}/users/{userid}/tweets?exclude=replies,retweets&max_results=100", \
                            headers=headers)
        if response.status_code != 200:
            return False, "Something went (slightly) off. Cops are investigating.", None, None
        response = response.json()
        return True, "", response['data'], response['meta']
    except Exception as e:
        return False, "Something went (slightly) off. Cops are investigating.", None, None

def get_word_list(tweets):
    d = {}
    for tweet in [x["text"] for x in tweets]:
        tweet = tweet.lower()
        tweet = " ".join([x for x in tweet.split() if not x.startswith("@")])
        tweet = word_tokenize(tweet)
        tweet = [x for x in tweet if len(x) > 2]
        for word in tweet:
            d[word] = d.get(word, 0) + 1
    to_be_removed = set(d.keys()).intersection(remove_word_set)
    for key in d.keys():
        if not key[0].isalpha():
            to_be_removed.add(key)
    for k in to_be_removed:
        del d[k]
    return d
