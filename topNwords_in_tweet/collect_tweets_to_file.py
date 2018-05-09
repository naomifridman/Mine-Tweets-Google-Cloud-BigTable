import numpy as np
import pandas as pd
import tweepy

# AUTHENTICATION (OAuth)
def tw_oauth():
    authfile = 'auth.k'
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    return tweepy.API(auth1)
	


# List of stop words, words we dont want to appear in our list.
s_words = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 
              'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be',
              'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself',
              'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each',
              'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 
              'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself',
              'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 
              'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 
              'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on',
              'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why',
              'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has',
              'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after',
              'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
              'doing', 'it', 'how', 'further', 'was', 'here', 'than', 'The',
              'RT', '&amp', ' ', '', 'http', 'via', 'https', 'is', 'rt', '\'s'}

import nltk
nltk.download('punkt')			  
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
def tokenize_tweet_text(tweet_text, Qye_words = None):
    
    word_tokens = word_tokenize(tweet_text)

    filtered_sentence = [w.lower() for w in word_tokens if not w in s_words]

    filtered_sentence = []

    for w.lower() in word_tokens:
        if w not in s_words | set(Qye_words):
            if (len(w)<= 1): continue
            if ('\\' in w): continue
            if ('/' in w): continue
            filtered_sentence.append(w)

    return filtered_sentence
	
# Define start date of our word survey
import datetime
delta = -1#-30
start_date = datetime.datetime.now() + datetime.timedelta(delta)

start_date = str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day)
#print('Collecting tweets since: ', start_date)
# TWEEPY SEARCH FUNCTION
# refernce: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
def tw_get_tweets(api,  query_in, Qye_words, geo, location, num_tweets=50):
    
    counter = 0
    example_tweet = None
    global df, word_list
           
    # We will not use geocode inorder not to miss most of the tweets.
    for tweet in tweepy.Cursor(api.search,
                                q = query_in,                 # the actual words we search
                                #geocode = geo,          # location
                                since = start_date,
                                count = num_tweets).items():

        #TWEET INFO
        created = tweet.created_at             #tweet created
        text    = tweet.text                   #tweet text
        tweet_id = tweet.id                    #tweet ID# (not author ID#)
        cords   = tweet.coordinates            #geographic co-ordinates
        geo_e   = tweet.author.geo_enabled     #is author/user account geo enabled?
        place   = tweet.place
        authorloc = tweet.author.location      #author/user location

             
        if any(word in authorloc for word in location):
            #print(authorloc ,'in', location)
            df.loc[counter] = [created, text, authorloc]
            word_list += tokenize_tweet_text(text, Qye_words = Qye_words)
            
        counter = counter +1
        #print (counter,created, text, num_tweets)
        if (counter >= num_tweets):
            break
            
    return (example_tweet)
#===================================================================================================
import sys
import os

def ensure_dir(fdir):
    #fdirectory = os.path.dirname(file_path)
	
    #print('dir from file path',file_path, fdirectory)
    if not os.path.exists(fdir):
        print('Creating ', fdir, ' directory')
        os.makedirs(fdir)
#===================================================================================================
import sys
import os
import os.path

Qye_words= ['BigData', 'bigdata', 'Bigdata']
query_in = {'(BIGDATA) OR (BigData) OR (BigData)'}
# example of locations
city_list = ['NY', 'London', 'Mumbai', 'Paris']
query_list = [['NY', 'New York'], ['London', 'london'], 
              ['Mumbai', 'mumbai', 'bombei'], ['paris', 'Paris']]

location_words = []
if (len(sys.argv) == 1):
    # using default location
    print ('No Location is given, Using default location: ', query_list[0])
    location_words = query_list[0]
else:
    location_words = sys.argv[1:]
    print('using Locations: ', location_words)

print('Retreiving tweets since: ', start_date, ' About BigData Tweeted in locations: ',  location_words )  
	   
# output file
fdir = location_words[0].replace(" ", "_")
ensure_dir(fdir)
fname = 'tweets_from_' + fdir+'.txt'	 

authfile = 'auth.k'
api = tw_oauth()
i = 0
cols = ['created', 'text', 'authorloc']
df = pd.DataFrame(columns=cols)
word_list = []
 
example_tweet = tw_get_tweets(api,  query_in, Qye_words, 
                                  location = location_words, 
                                  geo = None,
                                  num_tweets=2000)


df_city = pd.DataFrame(index = np.arange(0,len(word_list)), columns=['word'],
                     data=word_list)

			 
#df_city.to_csv(location_words[0]+'.csv', encoding='utf-8', index=False)
out_name = os.path.join(fdir, fname)
df_city.word.to_csv(out_name, encoding='utf-8', index=False, header=False)
#print (len(sys.argv), sys.argv)
print(len(df_city),' Words collected and saved in ', out_name)