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
word_tokenizer = RegexpTokenizer('[a-zA-Z]\w+')
def tokenize_tweet_text(tweet_text, Qye_words = None):
    
    word_tokens = word_tokenizer.tokenize(tweet_text)
    #print(word_tokens)
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
        #print(re.sub(r'a-zA-Z\W+', '', tweet.text))
        #print('loc ',re.sub(r'\W+', '', tweet.author.location))
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
		
    return word_list
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
	
	fname = 'tweets_from_' + fdir+'.txt'

	authfile = 'auth.k'
	api = tw_oauth()

	words = tw_get_tweets(api,  query_in, [x.lower() for x in Qye_words],
						  location = [x.lower() for x in location_words],
						  geo = None,
						  num_tweets=20000)
       		
	df_city = pd.DataFrame(index = np.arange(0,len(words)), columns=[[fdir]],
						 data=words)
						 	
	return df_city
#======================================================================================
#===============   Global variables
# build a query with logic operators
query = '(Royal AND wedding) OR (wedding AND Meghan) OR (Harry AND wedding) OR (Harry AND Meghan)'

# list of words that we don't want to count, because they are part of the query
# lower case is enought, because we filter words in lower case
Qye_words = word_tokenizer.tokenize(query.lower())

location_list = [['NY', 'New York', 'newyork', ], ['London'],
				   ['Dublin'], ['Washington']]	
df_results =  pd.DataFrame()
#=======================================================================================
from collections import Counter
import re
def count_and_sort_words(df):

    df_results =  []
    # lets count and sort words
    i = 0;
    for col in df.columns:
       #print('counting and sorting: ', col)
       words = df[col].tolist()

       if len(words) < 1: return df_results
       counts = Counter(words)
       word_list=[]
       freq_list=[]
       
       
       for item, frequency in counts.most_common(10):
           word_list.append(item)
           freq_list.append(frequency)

       
       if (i -- 0):
           df_results = pd.DataFrame({re.sub(r'\W+', '', str(col)) + '_words':word_list,
                              re.sub(r'\W+', '',str(col)) + '_freq':freq_list})
           print('df create',df_results.head())
       else:
           df1 = pd.DataFrame({re.sub(r'\W+', '', str(col)) + '_words' : word_list,
                              re.sub(r'\W+', '',str(col)) + '_freq':freq_list})
           print('df1',df1.head())
           print('df_results', df_results)
           df_results = pd.concat([df_results,df1], ignore_index=True, axis=1)

           print(df_results.head())
       df_results.fillna(0)
       i += 1  
    df.fillna(0)
    return df_results

#=============================================================================================
# https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/read-write-to-cloud-storage
def load_csv_to_bucket(df):
  
  # The call to get_default_gcs_bucket_name succeeds only if you have created the default bucket for your project.
  bucket_name = os.environ.get('BUCKET_NAME',
                               app_identity.get_default_gcs_bucket_name())

  self.response.headers['Content-Type'] = 'text/plain'
  self.response.write('Demo GCS Application running from Version: '
                      + os.environ['CURRENT_VERSION_ID'] + '\n')
  self.response.write('Using bucket name: ' + bucket_name + '\n\n')
#=============================================================================================
from subprocess import call
if __name__ == '__main__':
  n_times=4
  df = []
  for i in range(n_times):
    
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--locations', nargs='+', default=location_list[i], help = " (default location: %(default)s)")
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
    print()
    print()
    print('Most Popular words in Tweets about:')
    print(query)
    print()
    
    print(df.head())
    
    csv_file = df.to_csv('tweet_words.txt', sep=' ', index=False, header=False)
    os.system("gsutil cp tweet_words.txt gs://naomi-bucket")
      
	  
    
    run_job = 'gcloud dataproc jobs submit hadoop --cluster naomi-mapreduce-bigtable \
    --jar target/wordcount-mapreduce-1.0-jar-with-dependencies.jar \
    -- wordcount-hbase \
    gs://naomi-bucket/tweet_words.txt \
    \"tweet-words-count\"'
    os.system(run_job)
	
	python_job = python3 hbase_table_head.py --table \'tweet-words-count\' naomi-topnwords naomi-mapreduce-bigtable'
    os.system(python_job)
  df_results = count_and_sort_words(df.fillna(0))
  print('=======================================================================================')

  print(df_results.head(10))