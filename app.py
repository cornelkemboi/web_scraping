from flask import Flask, request, jsonify
import requests

from config import twitter_api, FACEBOOK_ACCESS_TOKEN

app = Flask(__name__)


def get_twitter_mentions(query):
    tweets = twitter_api.search_tweets(q=query, count=100)
    return tweets


def get_facebook_mentions(query):
    url = f'https://graph.facebook.com/v12.0/search'
    params = {
        'q': query,
        'type': 'page',
        'access_token': FACEBOOK_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


@app.route('/twitter', methods=['GET'])
def twitter_search():
    query = request.args.get('query', '')
    tweets = get_twitter_mentions(query)
    return jsonify([tweet.text for tweet in tweets])


@app.route('/facebook', methods=['GET'])
def facebook_search():
    query = request.args.get('query', '')
    data = get_facebook_mentions(query)
    return jsonify(data)


@app.route('/mentions', methods=['GET'])
def mentions():
    query = request.args.get('query', '')
    twitter_count = get_twitter_mentions(query)
    facebook_count = get_facebook_mentions(query)
    return jsonify({
        'twitter_mentions': twitter_count,
        'facebook_mentions': facebook_count
    })


if __name__ == '__main__':
    app.run(debug=True)
