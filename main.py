import urllib3
import csv
import os
import tweepy
import configparser
# import pandas as pd

# IMPORT JSON AND PARSE TWEET OBJ
# load and dumps

# https://www.youtube.com/watch?v=Lu1nskBkPJU&ab_channel=AISpectrum
"""
code for later: 

1. modify tweet data
need tweet, user, favorites, reply, reply favorites.. this is just indexing + the sentiment of each tweet
remove stop words
 run over the tweet data with another model, that will tell us the sentiment analysis for each tweet

2. tack on another column in the modified tweet data, if it's ratioed 
if reply.favorites > tweet.favorites: 
    csvwriter.writerow(["RATIOED", True])
else: 
    csvwriter.writerow(["RATIOED", False])
    
3. feed into ML model (second time)
the actual model part is quite easy, just importing a lib and a few lines of code... 
"""



def scrape_tweets(api):
    # df_user_tweets = pd.DataFrame()

    # Iterating through the files in the twitter_handles directory and then every row in each file
    for filename in os.listdir("./twitter_handles/"):
        print("FILENAME: ", filename)
        filename = "./twitter_handles/" + filename
        tweetdatafile = './tweet_data/raw_tweet_data.csv'
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                username = row
                try:

                    tweets = tweepy.Cursor(
                        api.user_timeline, id=username[0]).items(10)

                    # Nested for loops: for every tweet collected (specific timeframe), collect replies, print, and
                    # write to the tweet data file
                    for tweet in tweets:
                        if int(str(tweet.created_at)[0:4]) > 2021:
                            if int(str(tweet.created_at)[5:7]) >= 10:
                                continue
                        print(tweet)

                        top_replies = tweepy.Cursor(api.search_tweets, q='to:'+str(username[0]), result_type='recent,',
                                                    timeout=999999).items(10)
                        max_likes = -1
                        max_likes_reply = -1
                        ratioed = False
                        for reply in top_replies:
                            if reply.favorite_count > max_likes:
                                max_likes = reply.favorite_count
                                max_likes_reply = reply
                        print("most liked reply:",
                              max_likes_reply.favorite_count)

                        with open(tweetdatafile, 'a') as writefile:
                            # creating a csv writer object
                            csvwriter = csv.writer(writefile)

                            # writing the data rows
                            csvwriter.writerow([tweet])
                            csvwriter.writerow(["TOP_REPLY", max_likes_reply, "RATIOED", ])
                except BaseException as e:
                    print('failed on_status,', str(e))


def config():
    # Configuring the tweepy API and authentication

    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    print(api_key)

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    scrape_tweets(api)


def main():

    config()


main()
