from flask import Flask, render_template
import json
import reddit


app = Flask(__name__)

@app.route('/')
def index():
    #TODO: (14) Assign a Reddit subreddit name to use in this function.
    subreddit_name = 'meme' #Assign this variable to your favorite subreddit.
    #TODO: (15) Create an instance of the praw Reddit object. Refer to reddit.py
    reddit_instance = reddit.create_reddit_instance(read_only =True)
    #TODO: (16) Generate a list of top ten posts for your subreddit.
    top_ten_posts = reddit.ten_top_posts(reddit_instance, subreddit_name)
    #TODO: (17) Pass the list you created above to the render_template function call below.
    return render_template('index.html',posts = top_ten_posts ,name = subreddit_name)

if __name__ == "__main__":
    app.run(debug = True) #Set debug = False in a production environment