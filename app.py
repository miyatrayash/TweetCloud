from flask import Flask
from datetime import datetime

from config import Config
from utils import *

app = Flask(__name__)


@app.route('/')
def healthcheck():
    return {
        "status": True,
        "name": "TweetCloud Backend",
        "time": datetime.now(),
        "repo": Config.REPO_URL,
    }


@app.route('/details/<username>', methods=['GET'])
def details(username):
    now = datetime.now()
    username = (username or "").lower()
    if username.strip() == "":
        return {
            "status": False,
            "message": "Username is not correct."
        }, 500
    status, error, tweets_list, metadata = get_tweet_details(username)
    if not status:
        return {
            "status": False,
            "message": error
        }, 500
    word_list = get_word_list(tweets_list)
    return {
        "status": True,
        "message": "",
        "data": {
            "word_list": word_list,
            "username": "",
            "timestamp": now,
            "followers": 0,
            "following": 0,
            "tweets": 0,
        }
    }, 200