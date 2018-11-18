import praw #This module is used to create Reddit instances
import json
from urllib import request
from string import punctuation

def create_reddit_instance(read_only = False):
    credentials = None
    with open('credentials.json', 'r') as creds:
        credentials = json.load(creds) 
    if(not read_only):
        reddit_instance = praw.Reddit(
                                    client_id = credentials['client_id'],
                                    client_secret = credentials['client_secret'],
                                    username= credentials['username'], 
                                    password=credentials['password'],
                                    user_agent = credentials['user_agent']
                                     )
    else:
        reddit_instance = praw.Reddit(                                    
                                    client_id = credentials['client_id'],
                                    client_secret = credentials['client_secret'],
                                    user_agent = credentials['user_agent']
                                    )
    return reddit_instance
    
    
def ten_top_posts(reddit_instance, subreddit_name):
    '''This function takes a subreddit name as a string and prints out ten posts under the top category'''
    subreddit = reddit_instance.subreddit(subreddit_name)

    return subreddit.top(limit = 10)

def returnTitle_Description_Comments(post):
    '''returns a list that extracts all the information from the post: title, description, comments'''
    listComment = returnCommentArray(post)
    contentArray = [post.title, post.selftext, listComment]
    return contentArray

def returnCommentArray(post):
    '''returns a list of the posts' comments'''
    listComment = []
    for comment in post.comments:
        listComment.append(comment.body)
    return listComment

def count_words_in_sentence(wordfreq, sentence):
    '''Takes a sentence and counts the individual words after removing punctuations.'''
    sentence_str = ''.join(c.lower() for c in sentence if c not in punctuation)
    sentence_arr = sentence_str.split()
    for word in sentence_arr:
        if word not in wordfreq:
            wordfreq[word] = 0
        wordfreq[word] += 1
    return wordfreq

def createDictionary(posts):
    wordfreq = {}

    for raw_post in posts:
        post_information = returnTitle_Description_Comments(raw_post)
        wordfreq.update(count_words_in_sentence(wordfreq, post_information[0]))
        wordfreq.update(count_words_in_sentence(wordfreq, post_information[1]))
        for comment in post_information[2]:
            wordfreq.update(count_words_in_sentence(wordfreq, comment))
    return wordfreq

def returnTop10Keywords(dictWords):
    ''' returns the top 10 keywords from a dictionary'''
    keywords = []
    counter = 0
    for key,value in sorted(dictWords.items(), key = lambda x: x[1], reverse = True):
        if(counter < 10):
            if(len(key) > 4):
                keywords.append(key)
                counter += 1
    return keywords

if __name__ == '__main__':
    subreddit_name = 'grandorder' 
    reddit_instance = create_reddit_instance(read_only=True)
    posts = ten_top_posts(reddit_instance,subreddit_name)
    
    dictionary = createDictionary(posts)
    top10 = returnTop10Keywords(dictionary)
    counter = 1
    for key in top10:
        print("%d." % counter, key, dictionary[key])
        counter += 1
