from flask import Flask, request, jsonify
import requests

from config import twitter_api, FACEBOOK_ACCESS_TOKEN

app = Flask(__name__)


@app.route('/twitter', methods=['GET'])
def twitter_search():
    query = request.args.get('query', '')
    tweets = twitter_api.search_tweets(q=query, count=10)
    return jsonify([tweet.text for tweet in tweets])


@app.route('/facebook', methods=['GET'])
def facebook_search():
    query = request.args.get('query', '')
    url = f'https://graph.facebook.com/v12.0/search'
    params = {
        'q': query,
        'type': 'page',
        'access_token': FACEBOOK_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
