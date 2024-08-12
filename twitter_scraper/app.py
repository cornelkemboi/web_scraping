import os

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    print("Current working directory:", os.getcwd())
    df = pd.read_csv('tweets_data.csv')
    data_html = df.to_html(index=False, classes='table table-striped')
    return render_template('index.html', table=data_html)


if __name__ == '__main__':
    app.run(debug=True)
