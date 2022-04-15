from flask import Flask
from datetime import datetime
from flask_cors import CORS

from config import Config
from utils import *

from wordcloud import WordCloud
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

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
    word_counts = get_word_list(tweets_list)
    word_list = [{'value': k, 'count': word_counts[k]} for k in word_counts]
    text = " ".join([x['value'] for x in word_list])
    wordcloud = WordCloud(max_font_size=40).generate(text)
    wordcloud.to_file(f"static/{username}.png")
    return {
        "status": True,
        "message": "",
        "data": {
            "wordcloud_url": f"/static/{username}.png",
            "username": username,
            "timestamp": now
        }
    }, 200