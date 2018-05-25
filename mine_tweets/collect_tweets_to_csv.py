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
              'some', 'for', 'do', 'its', 'yours','de', 'vs', 'such', 'into', 'of', 'most', 'itself',
              'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each',
              'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 
              'through', 'don', '\'\'','nor', 'me', 'were', 'her', 'more', 'himself',
              'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 
              'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 
              'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on',
              'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why',
              'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has',
              'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after',
              'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
              'doing', 'it', 'how', 'further', 'was', 'here', 'than', 'The',
              'rt', '&amp', ' ', '','``', 'http', 'via', 'https', 'amp','\'s'}


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

import string
#string.printable
str_prt='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
printable_chars = bytes(str_prt, 'ascii')
word_tokenizer = RegexpTokenizer('[a-zA-Z]\w+')
from bs4 import BeautifulSoup
def my_print(s):
    soup = BeautifulSoup(s)
    #print('encode', soup.encode("utf-8"))
    tmp = soup.encode("utf-8")
    soup = BeautifulSoup(s, 'html.parser').encode("ascii")
    if len(soup) > 0:
        print(soup)
    #print('decode', tmp.decode("utf-8"))
def get_ascii(s):
   soup = BeautifulSoup(s, 'html.parser').encode("ascii")
   return soup 
import re
# match characters from ¿ to the end of the JSON-encodable range


#def isprintable(s):
#   return all(char @in printable_chars for char in s)
def tokenize_tweet_text(tweet_text, Qye_words = None):
    
    word_tokens = word_tokenizer.tokenize(tweet_text)
    #for word in word_tokens:
    #    if isprintable(word): print(word)
    filtered_sentence = []

    for w in word_tokens:
        if (len(w)<= 1): continue
        if w.lower() not in (s_words | set(Qye_words)):
            filtered_sentence.append(w.lower())

    return filtered_sentence

# Define start date of our word survey
import datetime
delta = -30
start_date = datetime.datetime.now() + datetime.timedelta(delta)
start_date = str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day)

## TWEEPY SEARCH FUNCTION
# refernce: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
def tw_get_tweets(api,  query_in, Qye_words, geo, location, num_tweets=200):

    counter = 0
    example_tweet = None
    word_list = []
    
    
    
    #print('query_in', query_in)
    #print('location', location)
    # We will not use geocode inorder not to miss most of the tweets.
    cs = tweepy.Cursor(api.search,
                                q = query_in,           # the actual words we search
                                #geocode = geo,          # location
                                since = start_date,
                                count = num_tweets).items()
    
    while True:
      
      try:
        
        tweet = cs.next()
        if (len(get_ascii(tweet.author.location)) == 0):
              continue

        #print('tweet text')
        #my_print(tweet.text)
        #print('authour location')
        #my_print(tweet.author.location)
        #TWEET INFO
        created = tweet.created_at             #tweet created
        text    = tweet.text                   #tweet text
        tweet_id = tweet.id                    #tweet ID# (not author ID#)
        cords   = tweet.coordinates            #geographic co-ordinates
        geo_e   = tweet.author.geo_enabled     #is author/user account geo enabled?
        place   = tweet.place
        authorloc = tweet.author.location      #author/user location
                
        #if (authorloc is None): continue
        #if (len(authorloc) <= 1) : continue
        location_token = word_tokenizer.tokenize(authorloc)
        #location_token = [x for x in location_token]
        #print('location_token', location_token)
        
        if any(word.lower() in location_token for word in location):
            #print('text', word_tokenizer.tokenize(text))
            #print('location', word_tokenizer.tokenize(authorloc))
            word_list += tokenize_tweet_text(text, Qye_words = Qye_words)

        counter = counter +1
        if (counter >= num_tweets):
            break
        # Insert into db
      except tweepy.TweepError:
        break
      except StopIteration:
        break

    print('	******************** counter of collected tweets: ', counter)	
    return word_list
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
import os
import os.path
import argparse
import sys

def get_tweets_words(location_words, query_in):



	# check user input for location. If not given use default


	print('Retreiving tweets since: ', start_date, ' about: ')
	print(query_in)
	print('Tweeted in locations: ',  location_words[0] )
     
	# output file - use first phrase of the given location 
	fdir = location_words[0].replace(" ", "_")
	ensure_dir(fdir)
	fname = 'tweets_from_' + fdir+'.txt'

	authfile = 'auth.k'
	api = tw_oauth()

	
	#table, connection, column_name = create_BigTable_table(location_words[0])
	words = tw_get_tweets(api,  query_in, [x.lower() for x in Qye_words],
						  location = [x.lower() for x in location_words],
						  geo = None,
						  num_tweets=80000)
	
	#connection.close()        		
	df_city = pd.DataFrame(index = np.arange(0,len(words)), columns=[[fdir]],
						 data=words)
						 
	out_name = os.path.join(fdir, fname)
	df_city[fdir].to_csv(out_name, encoding='utf-8', index=False, header=False)

	print(len(df_city), ' Words collected and saved in ', out_name)
	print(df_city.head())
	return df_city
#======================================================================================
#===============   Global variables
# build a query with logic operators
query = '(Royal AND wedding) OR (wedding AND Meghan) OR (Harry AND wedding) OR (Harry AND Meghan)'

# list of words that we don't want to count, because they are part of the query
# lower case is enought, because we filter words in lower case
Qye_words = word_tokenizer.tokenize(query.lower())

location_list = [['NY', 'Newyork', 'New York', 'newyork', 'NYC'], ['London'], #, 'New York', 'Newyork'
				   ['Dublin'], ['Washington']]	

#=======================================================================================
from collections import Counter
import re
def count_and_sort_words(df):

    df_results =  []
    # lets count and sort words
    
    
    
    words = df[df.columns[0]].tolist()

    
    counts = Counter(words)
    word_list=[]
    freq_list=[]
       
    if (len(counts) > 0):
        for item, frequency in counts.most_common(5):
            word_list.append(item)
            freq_list.append(frequency)

    df_results = pd.DataFrame({re.sub(r'\W+', '', str(df.columns[0])) + '_words':word_list,
                              re.sub(r'\W+', '',str(df.columns[0])) + '_freq':freq_list})   
    return df_results

#=============================================================================================

if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--locations', nargs='+', default=location_list[0], help = " (default location: %(default)s)")
    parser.add_argument('-q', '--about',  default=query, help = " (default Query: %(default)s)")
    args = parser.parse_args()
    #print('args',args, args.about, 'len',len(args.about))
    query = args.about
    Qye_words = word_tokenizer.tokenize(query)
    #print('Twitter Query: ', query)
    print('Folllowing words will be not counted: ',Qye_words)
    print('args.locations', args.locations)
    query_list = args.locations
    print('query', query, 'Qye_words',Qye_words)
    
    df = get_tweets_words(args.locations, args.about)
    
    df.fillna(0)
    print()
    print()
    print('Most Popular words in Tweets about:')
    print(query)
    print()
	

    print('=======================================================================================')    
    print(df.head())

    df_results = count_and_sort_words(df.fillna(0))
  
    print(df_results.head(10))