from flask import Flask, render_template
from flask import request, redirect
import json
import reddit

app = Flask(__name__)

@app.route('/')
def index(keyword=None):
    if keyword== None:
        subreddit_name = 'uci' 
    else:
        subreddit_name=keyword
    reddit_instance = reddit.create_reddit_instance(read_only =True)
    top_ten_posts = reddit.ten_top_posts(reddit_instance, subreddit_name)
    return render_template('index.html',posts = top_ten_posts ,name = subreddit_name)

@app.route('/handlesearch', methods=['POST'])
def search_function():
    return index(keyword=(request.form['name']))

if __name__ == "__main__":
    app.run(debug = True)