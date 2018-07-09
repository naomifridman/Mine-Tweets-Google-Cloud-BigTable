import numpy as np
import pandas as pd
import tweepy

# to install re use:
# pip install regexp
import re
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
def tokenize_tweet_text(tweet_text, Qey_words = None):
    
    word_tokens = word_tokenizer.tokenize(tweet_text)
    #print(word_tokens)
    filtered_sentence = []

    for w in word_tokens:
        if (len(w)<= 1): continue
        if w.lower() not in (s_words | set(Qey_words)):
            filtered_sentence.append(w.lower())

    return filtered_sentence

# Define start date of our word survey
import datetime
delta = -30
start_date = datetime.datetime.now() + datetime.timedelta(delta)
start_date = str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day)

## TWEEPY SEARCH FUNCTION
# refernce: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
def tw_get_tweets(api,  query_in, Qey_words, geo, location, num_tweets=200):

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
            word_list += tokenize_tweet_text(text, Qey_words = Qey_words)

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

	words = tw_get_tweets(api,  query_in, [x.lower() for x in Qey_words],
						  location = [x.lower() for x in location_words],
						  geo = None,
						  num_tweets=2000)
       		
	df_city = pd.DataFrame(index = np.arange(0,len(words)), columns=[[fdir]],
						 data=words)
						 	
	return df_city
#======================================================================================
#===============   Global variables
# build a query with logic operators
query = '(Royal AND wedding) OR (wedding AND Meghan) OR (Harry AND wedding) OR (Harry AND Meghan)'

# list of words that we don't want to count, because they are part of the query
# lower case is enought, because we filter words in lower case
Qey_words = word_tokenizer.tokenize(query.lower())

location_list = [['NY', 'New York', 'newyork'], ['London'],
				   ['Dublin'], ['Washington']]	
df_results =  pd.DataFrame()

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
from google.cloud import bigtable
from google.cloud import happybase

def get_max_val(table, no_keyes):
    
    key_max = ''
    val_max = 0
    i = 0
    for key, row in table.scan():
        if (key not in no_keyes):
            val = int.from_bytes(row[b'cf:count'], byteorder='big')
            #print(i, ' word: ', key.decode("utf-8"),  'count: ', int.from_bytes(row[b'cf:count'], byteorder='big'))
            if (val > i):
                key_max = key.decode("utf-8")
                val_max = val
                i = val
    return key_max, val_max
#======================================================================================
def get_top5_freq_words(project_id, instance_id, table_name):
    # [START connecting_to_bigtable]
    # The client must be created with admin=True because it will create a
    # table.
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    connection = happybase.Connection(instance=instance)
    # [END connecting_to_bigtable]
    keys = []
    vals = []

    try:
        # [START creating_a_table]
        tablese = connection.tables()
        print('existing tables: ', tablese)
        column_family_name = 'cf'
        
        table = connection.table(table_name)

        # [START scanning_all_rows]
        print('Scanning all words in table: ', table_name)

       
        column_name = '{fam}:count'.format(fam=column_family_name)
        print('column_name ', column_name)
		
        max_val = 0
        max_key = None
        
        for i in range(5):
            max_val = 0
            max_key = None
            key, val = get_max_val(table, keys)
            print(key, val)
            keys.append(key)
            vals.append(val)

    finally:
        connection.delete_table(table_name)
        connection.close()

    return keys, vals
#======================================================================================
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
    Qey_words = word_tokenizer.tokenize(query)
    #print('Twitter Query: ', query)
    print('Folllowing words will be not counted: ',Qey_words)
    print('args.locations', args.locations)
    query_list = args.locations
    
    df = get_tweets_words(args.locations, args.about)
    print()
    print()
    print('Example of words in Tweets about:')
    print(query)
    print()
    
    print(df.head())
    
    #fname = 'tweet_words' + str(i) +'.txt'
    #print('Twitter words are saved into: ', fname)
    csv_file = df.to_csv('tweet_words.txt', sep=' ', index=False, header=False)
    #fjob = 'gsutil cp ' + fname + ' gs://naomi-bucket'
    #print('running : ', fjob)
    print('Running: gsutil ls -l gs://naomi-bucket/tweet')
    os.system('gsutil ls -l gs://naomi-bucket/tweet')
    print('Running: gsutil rm  -f  gs://naomi-bucket/tweet/*')
    os.system("gsutil rm  -f  gs://naomi-bucket/tweet/tweet_words.txt")
    print('Running: gsutil cp tweet_words.txt gs://naomi-bucket/tweet')
    os.system("gsutil cp tweet_words.txt gs://naomi-bucket/tweet")  
    #os.system(fjob)
    #print(fname, ' is uploaded to gs://naomi-bucket')
    print('Running: gsutil ls -l gs://naomi-bucket/tweet')
    os.system('gsutil ls -l gs://naomi-bucket/tweet')
   
    run_job = '~/hadoop/bin/hadoop  \
    jar target/wordcount-mapreduce-1.0-jar-with-dependencies.jar \
     wordcount-hbase \
      gs://naomi-bucket/tweet \
      \"tweet-words-count\"'
	
    print('Running mapreduce job: ')
    print(run_job)
	
    os.system(run_job)
	
	
    keys, vals = get_top5_freq_words(project_id='naomi-topnwords', instance_id='naomi-mapreduce-bigtable', 
                                     table_name='tweet-words-count')
									 
    # Add results to df_results
    if (i == 0):
           df_results = pd.DataFrame({re.sub(r'\W+', '', str(args.locations[0])) + '_words':keys,
                              re.sub(r'\W+', '',str(args.locations[0])) + '_freq':vals})
           print('df create',df_results.head())
    else:
           df1 = pd.DataFrame({re.sub(r'\W+', '', str(args.locations[0])) + '_words' : keys,
                              re.sub(r'\W+', '',str(args.locations[0])) + '_freq':vals})
           #print('df1',df1.head())
           #print('df_results', df.columns, args.locations[0])
           df_results = pd.concat([df_results,df1], ignore_index=True, axis=1)

           print('df_results after concat:', df_results.head())
	
  
  print('=======================================================================================')

  print(df_results.head())