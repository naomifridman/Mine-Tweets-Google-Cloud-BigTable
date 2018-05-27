
# What people from different places tweet, and they tweet about ... ?
In this fun python project, I mine tweets about a subject, and compare most frequent words in different locations.
I Collect the words people Tweet, on a given query, filtered by location, tokenize and strip the text, count words and find 
highest frequency ones. I used "Royal Weding" and "BigData" as example subjects.

### Python files in repository
#### Python notebook to play around with Twitter mining. 
Functionality in Python notebook:
* Implement Tweets retrieving, according to a given query.
* Reserch Tweet data structure.
* Reserch Tweets location issues.
* Implement word tokenizing and filtering.
#### Python script to mine Tweets by location and subject.
Usage:<br>
```

$ python collect_tweets_to_csv.py -h
usage: collect_tweets_to_csv.py [-h] [-n LOCATIONS [LOCATIONS ...]] [-q ABOUT]

optional arguments:
  -h, --help            show this help message and exit
  -n LOCATIONS [LOCATIONS ...], --locations LOCATIONS [LOCATIONS ...]
                        (default location: ['NY', 'New York', 'newyork'])
  -q ABOUT, --about ABOUT
                        (default Query: (Royal AND wedding) OR (wedding AND
                        Meghan) OR (Harry AND wedding))
```
Query should be written according to Twitter format. Mo processing is done on the query.<br>
Script is running on 4 locations, you can change it in source, by changing n_time varible.<br>
Results example, for query: (Royal AND wedding) OR (wedding AND Meghan) OR (Harry AND wedding)
```
      NY_words  NY_freq 
0         love       27
1        white        5  
2       prince        5 
3        house        4
4       markle        4 
5        trump        3 
6     pb_curry        2  
7           go        2  
8       newday        2  
9  independent        2  
```
# Python Notebook


```python
import numpy as np
import pandas as pd
import tweepy   #Python library for accessing the Twitter API.

import nltk     #Python NLP library for tokenizing tweeter text
nltk.download('punkt')
```

    [nltk_data] Downloading package punkt to C:\Users\yoav
    [nltk_data]     fridman\AppData\Roaming\nltk_data...
    [nltk_data]   Package punkt is already up-to-date!
    




    True



## 1. Twitter API Authentication 
In order to extract tweets, we need an access kyes to Twitter API. To get those, you need a twitter acount, and you need to create a Twitter App to get the following 4 keys:

* Consumer Key (API Key)
* Consumer Secret (API Secret)
* Access Token
* Access Token Secret

Write those kyes in a text file, each in separate row. name the file: auth.k
Website to create the Twitter App https://apps.twitter.com/. 


```python
# AUTHENTICATION (OAuth)
def tw_oauth():
    authfile = 'auth.k'
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    return tweepy.API(auth1)
```

## 2. Tweet data structure
Lets extract 5 recent tweets, and view the tweet data structure.


```python
example_tweet = None

api = tw_oauth()
print ('5 recent tweets about Bigdata:')
Counter = 0
for tweet in tweepy.Cursor(api.search, q = 'Bigdata',lang = 'en',count = 5).items(): 
    print (tweet.text)
    Counter += 1
    if (Counter == 5):
        example_tweet = tweet 
        break
    
```

    5 recent tweets about Bigdata:
    RT @AiFinTek: AIRDROP Alert -Crypto project live, Free Tokens,100$ AFTK TOKEN,50$ AFTK Friend Referral, https://t.co/Hy9MZ5jfLS #ICO #block…
    RT @jblefevre60: What are the #Top10 #Disruptive #technologies?
    
    #fintech #Digital #Blockchain #AI #AR #VR #Drones #BigData #IoT #Robots #3…
    RT @IainLJBrown: Accelerating big data for social good with UNICEF
    
    Read more here: https://t.co/kMc9w7n63p
    
    #BigData #DataScience #Machine…
    RT @MarcoPark21: RT DeepLearn007 "RT DeepLearn007: Stanford University: Deep Learning Comes Full Circle
    #AI #MachineLearning #DeepLearning…
    How Is #BigData Influencing the Education Sector? #AI #ML  https://t.co/jMpsNVIWLE
    

** Tweet data is an object containing information about the authour and the Tweet.Lest view few fildes that is relevant to us.**


```python
# We print info from the first tweet:
print('id: ', example_tweet.id)
print('created_at:', example_tweet.created_at)
print('geo:',example_tweet.geo)
print('coordinates',example_tweet.coordinates)

print('text:',example_tweet.text)                   #tweet text
print('geo_enabled:',example_tweet.author.geo_enabled)     #is author/user account geo enabled

```

    id:  994303915171565568
    created_at: 2018-05-09 19:51:41
    geo: None
    coordinates None
    text: How Is #BigData Influencing the Education Sector? #AI #ML  https://t.co/jMpsNVIWLE
    geo_enabled: True
    

## 3. Tokenize tweet
** Lest look at tweet test example:**<br>
RT @Hiredscore: Our team is gearing up for @Littler's 35th annual Executive Employer Conference in Phoenix, AZ this week! Attending the con…<br>
** To analize commom words in tweet, We need to tokenize and filter tweet text**<br>
* we change all words to lower case not to have doubles
* We will use nltk library for tokenizing
* we will remove stop words a, is, the...
* we will remove unintersting words, specific to tweeter, as: RT, &amp
* nltk tokenizing separate @ and # from the words, so if we limit word size to >1, its good enought.
* We will get user_id as a word in our list, since nltk splits @ronbon to @ and ronbon, but its interseting to the users that tweet so much about the given subgect.
    


```python
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

```


```python
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
def tokenize_tweet_text(tweet_text, Qye_words = None):
    
    word_tokens = word_tokenize(tweet_text)

    filtered_sentence = []

    for w in word_tokens:
        if w.lower() not in s_words | set(Qye_words):
            if (len(w)<= 1): continue
            if ('\\' in w): continue
            if ('/' in w): continue
                
            if (w.endswith('...')): w = w[:-4]
            if (w.startswith('...')): w = w[4:]
            if (w.endswith('-')): w = w[:-1]
            if (w.startswith('-')): w = w[1:]
            if (w.endswith('…')): w = w[:-1]
            if (w.startswith('…')): w = w[1:]
            if (w.isdigit()): continue
            filtered_sentence.append(w.lower())

    return filtered_sentence
```


```python
# Lets check the tokenizing function

example_sent = "April 2018 JAX Magazine is Out: Machine Learning. #BigData #DeepLearning #MachineLeaning #DataScience #AI #Python #RStats @filtration \\ppo."
word_tokens = tokenize_tweet_text(example_sent, Qye_words = ['BigData'])

print(word_tokens)

```

    ['april', 'jax', 'magazine', 'machine', 'learning', 'bigdata', 'deeplearning', 'machineleaning', 'datascience', 'ai', 'python', 'rstats', 'filtration']
    

## 4. Retrive Tweet data definitions
There is a lot of data associated with each tweet. Lest view few the search fieldes that is relevant to our task.<br>
refernce: https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
* **q	required**	A UTF-8, URL-encoded search query of 500 characters maximum, including logical operators operators. <br>
    example: <br>
    * q = 'bigdata' : will retrive Tweets that have the word bigdata
    * q = 'puppy filter:media' : will retrive Tweets containing “puppy” and an image or video.
* **geocode	optional**	Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferably taken from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by ” latitude,longitude,radius ”, where radius units must be specified as either ” mi ” (miles) or ” km ” (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly. A maximum of 1,000 distinct “sub-regions” will be considered when using the radius modifier.<br>
    example: 37.781157 -122.398720 1mi
* **lang	optional**	Restricts tweets to the given language, given by an ISO 639-1 code. Language detection is best-effort. We will use only english<br>
    example: eu, en
* **count	optional**	The number of tweets to return per page, up to a maximum of 100. Defaults to 15. This was formerly the “rpp” parameter in the old Search API.<br>
    example: 100
<br>
Full definition can be found here: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets


## 4.1 How can we Filter Tweet by location


When working with Tweet data, there are two classes of geographical metadata:<br>

* **Tweet location** - Available when user shares location at time of Tweet.
* **Account Location** - Based on the ‘home’ location provided by user in their public profile. This is a free-form character field and may or may not contain metadata that can be geo-referenced.
Nullable . The user-defined location for this account’s profile. Not necessarily a location, nor machine-parseable. This field will occasionally be fuzzily interpreted by the Search service. Example: "location": "San Francisco, CA"

**Important Notes:**

    * Geographical coordinates are provided in the [LONG, LAT] order. <br>
The one exception is the deprecated  ‘geo’ attribute, which has the reverse [LAT, LONG] order.

    
#### Tweet locations ("geo-tagged" Tweets)
Twitter enables users to specify a location for individual Tweets. Tweet-specific location information falls into two general categories:

    * Tweets with a specific latitude/longitude “Point” coordinate
    * Tweets with a Twitter “Place” 
Tweets with a Point coordinate come from GPS enabled devices, and represent the exact GPS location of the Tweet in question. This type of location does not contain any contextual information about the GPS location being referenced (e.g. associated city, country, etc.), unless the exact location can be associated with a Twitter Place.

Tweets with a Twitter “Place” contain a polygon, consisting of 4 lon-lat coordinates that define the general area (the “Place”) from which the user is posting the Tweet. Additionally, the Place will have a display name, type (e.g. city, neighborhood), and country code corresponding to the country where the Place is located, among other fields.

#### Autor location 
Author location is an an arbitary centence that describe the author location. It is saved in authorloc varible. Author location for example can be:
* Hillingdon, London
* NY USA
Or any other centence the user chose to use as location description.
** To filter our desired locations, we will check if strings such as NY or London are contained in the authorlocation filed.

## Conclusions:
### From our tests and Tweeter documentation, not more then 0.5% of the tweets has geo tagging, so to get the full picture, we will filter tweet locations by the description in the Author location field.

## 4.2 Filter tweets by time
* **since**	optional filed in tweeter retriving. It Filter tweets created from the given date. Date should be formatted as YYYY-MM-DD. **Keep in mind that the search index has a 7-day limit**. In other words, no tweets will be found for a date older than one week!!.<br>
    example: 2015-07-19

source: https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location <br>    


```python
# Define start date of our word survey
import datetime
delta = -30
start_date = datetime.datetime.now() + datetime.timedelta(delta)
start_date = str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day)
print('Collecting tweets since: ', start_date)

```

    Collecting tweets since:  2018-4-9
    


```python
print('Collecting tweets since: ', start_date)
# TWEEPY SEARCH FUNCTION
# refernce: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
def tw_get_tweets(api,  query_in, Qye_words, geo, location, num_tweets=200):

    counter = 0
    example_tweet = None
    word_list = []
    
    # We will not use geocode inorder not to miss most of the tweets.
    for tweet in tweepy.Cursor(api.search,
                                q = query_in,           # the actual words we search
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
            word_list += tokenize_tweet_text(text, Qye_words = Qye_words)

        counter = counter +1
        if (counter >= num_tweets):
            break
    return word_list
```

    Collecting tweets since:  2018-4-9
    

 ## 5. Lets Run some tests


```python
import sys
import os
import os.path
from collections import Counter

authfile = 'auth.k'
api = tw_oauth()

df_results =  pd.DataFrame()
i = 0

Qye_words= ['bigdata']
query_in = 'BIGDATA+BigData+BigData'

# example of locations
location_list = ['NY', 'London', 'Mumbai', 'Paris']
query_list = [['NY', 'New York'], 
              ['London', 'london'],
              ['Mumbai', 'mumbai', 'bombay', 'Bombay'],
              ['paris', 'Paris']]

# lets view frequent words about Bigdata in different cities
for i in range(len(location_list)):
    
    location_words = query_list[i]

    print('Retreiving tweets since: ', start_date, ' about', Qye_words[0] ,
          ' Tweeted in locations: ',  location_list[i] )

    words = tw_get_tweets(api,  query_in, Qye_words = Qye_words,
                                      location = location_words,
                                      geo = None,
                                      num_tweets=2000)

    # lets count and sort words
    counts = Counter(words)
    word_list=[]
    freq_list=[]
    
    if (len(counts) > 0):
        for item, frequency in counts.most_common(10):
            word_list.append(item)
            freq_list.append(frequency)


        df_results[location_list[i] + '_words'] = word_list
        df_results[location_list[i] + '_freq'] = freq_list  

df_results.head(10)
```

    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  NY
    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  London
    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  Mumbai
    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  Paris
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>NY_words</th>
      <th>NY_freq</th>
      <th>London_words</th>
      <th>London_freq</th>
      <th>Mumbai_words</th>
      <th>Mumbai_freq</th>
      <th>Paris_words</th>
      <th>Paris_freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>iot</td>
      <td>29</td>
      <td>ai</td>
      <td>33</td>
      <td>machinelearning</td>
      <td>2</td>
      <td>data</td>
      <td>22</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ai</td>
      <td>25</td>
      <td>iot</td>
      <td>25</td>
      <td>kirkdborne</td>
      <td>2</td>
      <td>read</td>
      <td>20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>data</td>
      <td>15</td>
      <td>read</td>
      <td>23</td>
      <td>aftk</td>
      <td>2</td>
      <td>iainljbrown</td>
      <td>19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>cybersecurity</td>
      <td>13</td>
      <td>data</td>
      <td>21</td>
      <td>datascience</td>
      <td>2</td>
      <td>big</td>
      <td>17</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tech</td>
      <td>13</td>
      <td>iainljbrown</td>
      <td>17</td>
      <td>falling</td>
      <td>1</td>
      <td>datascience</td>
      <td>17</td>
    </tr>
    <tr>
      <th>5</th>
      <td>digital</td>
      <td>13</td>
      <td>datascience</td>
      <td>17</td>
      <td>project</td>
      <td>1</td>
      <td>ai</td>
      <td>16</td>
    </tr>
    <tr>
      <th>6</th>
      <td>fisher85m</td>
      <td>11</td>
      <td>machinelearning</td>
      <td>16</td>
      <td>love</td>
      <td>1</td>
      <td>machinelearning</td>
      <td>15</td>
    </tr>
    <tr>
      <th>7</th>
      <td>vladobotsvadze</td>
      <td>11</td>
      <td>analytics</td>
      <td>15</td>
      <td>block</td>
      <td>1</td>
      <td>iot</td>
      <td>12</td>
    </tr>
    <tr>
      <th>8</th>
      <td>analytics</td>
      <td>10</td>
      <td>google</td>
      <td>12</td>
      <td>short</td>
      <td>1</td>
      <td>ml</td>
      <td>7</td>
    </tr>
    <tr>
      <th>9</th>
      <td>vr</td>
      <td>10</td>
      <td>vladobotsvadze</td>
      <td>11</td>
      <td>alert</td>
      <td>1</td>
      <td>artificialintelligence</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



## Lets query more intersting staff
Lest check the popular words in Tweets abount president Trump and Iran in different countries.


```python
df_politics =  pd.DataFrame()
i = 0

# list of words that we don't want to count, because they are part of the query
# lower case is enought, because we filter words in lower case
Qye_words= ['trump', 'iran', 'president', 'us', 'america']

# build a query with logic operators
query_in ='(Trump AND Iran) OR (trump AND iran) OR (TRUMP AND IRAN)'

# define location names
location_list = ['US', 'INDIA', 'ENGLAND']

# define list of string by wich tweets are filtered
query_list = [['NY', 'New York', 'Washington', 'San Fransisco', 'US', 'USA'], 
              ['Mumbai', 'mumbai', 'bombay', 'Bombay', 'Delhi', 
               'India', 'Bangalore', 'INDIA'],
                ['London', 'london', 'Liverpool', 'England', 'Manchester']]


# lets view frequent words about Bigdata in different cities
for i in range(len(location_list)):
    
    location_words = query_list[i]

    print('Retreiving tweets since: ', start_date, ' about', Qye_words[0] ,
          ' Tweeted in locations: ',  location_list[i] )

    words = tw_get_tweets(api,  query_in, Qye_words = Qye_words,
                                      location = location_words,
                                      geo = None,
                                      num_tweets=6000)

    # lets count and sort words
    counts = Counter(words)
    word_list=[]
    freq_list=[]
    
    if (len(counts) > 0):
        for item, frequency in counts.most_common(10):
            word_list.append(item)
            freq_list.append(frequency)


        df_politics[location_list[i] + '_words'] = word_list
        df_politics[location_list[i] + '_freq'] = freq_list  

df_politics.head(10)
```

    Retreiving tweets since:  2018-4-9  about trump  Tweeted in locations:  US
    Retreiving tweets since:  2018-4-9  about trump  Tweeted in locations:  INDIA
    Retreiving tweets since:  2018-4-9  about trump  Tweeted in locations:  ENGLAND
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>US_words</th>
      <th>US_freq</th>
      <th>INDIA_words</th>
      <th>INDIA_freq</th>
      <th>ENGLAND_words</th>
      <th>ENGLAND_freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>deal</td>
      <td>436</td>
      <td>deal</td>
      <td>14</td>
      <td>deal</td>
      <td>82</td>
    </tr>
    <tr>
      <th>1</th>
      <td>nuclear</td>
      <td>149</td>
      <td>nuclear</td>
      <td>4</td>
      <td>nuclear</td>
      <td>31</td>
    </tr>
    <tr>
      <th>2</th>
      <td>decision</td>
      <td>80</td>
      <td>syria</td>
      <td>4</td>
      <td>n't</td>
      <td>19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>obama</td>
      <td>77</td>
      <td>dow</td>
      <td>3</td>
      <td>speech</td>
      <td>16</td>
    </tr>
    <tr>
      <th>4</th>
      <td>world</td>
      <td>50</td>
      <td>went</td>
      <td>3</td>
      <td>donald</td>
      <td>15</td>
    </tr>
    <tr>
      <th>5</th>
      <td>go</td>
      <td>50</td>
      <td>breaks</td>
      <td>3</td>
      <td>fact</td>
      <td>14</td>
    </tr>
    <tr>
      <th>6</th>
      <td>kurteichenwald</td>
      <td>38</td>
      <td>celebrate</td>
      <td>3</td>
      <td>buckle</td>
      <td>14</td>
    </tr>
    <tr>
      <th>7</th>
      <td>went</td>
      <td>37</td>
      <td>facts</td>
      <td>3</td>
      <td>reckless</td>
      <td>14</td>
    </tr>
    <tr>
      <th>8</th>
      <td>stocks</td>
      <td>37</td>
      <td>energy</td>
      <td>3</td>
      <td>checked</td>
      <td>14</td>
    </tr>
    <tr>
      <th>9</th>
      <td>iranian</td>
      <td>37</td>
      <td>matter</td>
      <td>3</td>
      <td>nowthisnews</td>
      <td>14</td>
    </tr>
  </tbody>
</table>
</div>

## Twitter Tips
### printing - causing problems due to charechter the Twitter createa.
Worked for me only with the following:
```
from bs4 import BeautifulSoup
def my_print(s):
    soup = BeautifulSoup(s)
    print(soup.encode("utf-8"))
```

# What people from different places tweet, and they tweet about ... ?
In this fun python project, I mine tweets about a subject, and compare most frequent words in different locations.
I Collect the words people Tweet, on a given query, filtered by location, tokenize and strip the text, count words and find 
highest frequency ones. I used "Royal Wedding" and "BigData" as example subjects.

### Python files in repository
#### Python notebook to play around with Twitter mining. 
Functionality in Python notebook:
* Implement Tweets retrieving, according to a given query.
* Research Tweet data structure.
* Research Tweets location issues.
* Implement word tokenizing and filtering.
#### Python script to mine Tweets by location and subject.
Usage:<br>
```

$ python collect_tweets_to_csv.py -h
usage: collect_tweets_to_csv.py [-h] [-n LOCATIONS [LOCATIONS ...]] [-q ABOUT]

optional arguments:
  -h, --help            show this help message and exit
  -n LOCATIONS [LOCATIONS ...], --locations LOCATIONS [LOCATIONS ...]
                        (default location: ['NY', 'New York', 'newyork'])
  -q ABOUT, --about ABOUT
                        (default Query: (Royal AND wedding) OR (wedding AND
                        Meghan) OR (Harry AND wedding))
```
Query should be written according to Twitter format. Mo processing is done on the query.<br>
Script is running on 4 locations, you can change it in source, by changing n_time varible.<br>
Results example, for query: (Royal AND wedding) OR (wedding AND Meghan) OR (Harry AND wedding)
```
      NY_words  NY_freq London_words  London_freq
0         love       27     prince             16
1        white        5       markle            8
2       prince        5      youtube            7
3        house        4   everything            5
4       markle        4   qfpbyngknq            5
5        trump        3         find            5
6     pb_curry        2         love            5
7           go        2    beautiful            5
8       newday        2         went            5
9  independent        2       really            5
```
# Python Notebook


```python
import numpy as np
import pandas as pd
import tweepy   #Python library for accessing the Twitter API.

import nltk     #Python NLP library for tokenizing tweeter text
nltk.download('punkt')
```

    [nltk_data] Downloading package punkt to C:\Users\yoav
    [nltk_data]     fridman\AppData\Roaming\nltk_data...
    [nltk_data]   Package punkt is already up-to-date!
    




    True



## 1. Twitter API Authentication 
In order to extract tweets, we need an access keys to Twitter API. To get those, you need a twitter account, and you need to create a Twitter App to get the following 4 keys:

* Consumer Key (API Key)
* Consumer Secret (API Secret)
* Access Token
* Access Token Secret

Write those keys in a text file, each in separate row. name the file: auth.k
Website to create the Twitter App https://apps.twitter.com/. 


```python
# AUTHENTICATION (OAuth)
def tw_oauth():
    authfile = 'auth.k'
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    return tweepy.API(auth1)
```

## 2. Tweet data structure
Lets extract 5 recent tweets, and view the tweet data structure.


```python
example_tweet = None

api = tw_oauth()
print ('5 recent tweets about Bigdata:')
Counter = 0
for tweet in tweepy.Cursor(api.search, q = 'Bigdata',lang = 'en',count = 5).items(): 
    print (tweet.text)
    Counter += 1
    if (Counter == 5):
        example_tweet = tweet 
        break
    
```

    5 recent tweets about Bigdata:
    RT @AiFinTek: AIRDROP Alert -Crypto project live, Free Tokens,100$ AFTK TOKEN,50$ AFTK Friend Referral, https://t.co/Hy9MZ5jfLS #ICO #block…
    RT @jblefevre60: What are the #Top10 #Disruptive #technologies?
    
    #fintech #Digital #Blockchain #AI #AR #VR #Drones #BigData #IoT #Robots #3…
    RT @IainLJBrown: Accelerating big data for social good with UNICEF
    
    Read more here: https://t.co/kMc9w7n63p
    
    #BigData #DataScience #Machine…
    RT @MarcoPark21: RT DeepLearn007 "RT DeepLearn007: Stanford University: Deep Learning Comes Full Circle
    #AI #MachineLearning #DeepLearning…
    How Is #BigData Influencing the Education Sector? #AI #ML  https://t.co/jMpsNVIWLE
    

** Tweet data is an object containing information about the author and the Tweet.Lest view few fields that is relevant to us.**


```python
# We print info from the first tweet:
print('id: ', example_tweet.id)
print('created_at:', example_tweet.created_at)
print('geo:',example_tweet.geo)
print('coordinates',example_tweet.coordinates)

print('text:',example_tweet.text)                   #tweet text
print('geo_enabled:',example_tweet.author.geo_enabled)     #is author/user account geo enabled

```

    id:  994303915171565568
    created_at: 2018-05-09 19:51:41
    geo: None
    coordinates None
    text: How Is #BigData Influencing the Education Sector? #AI #ML  https://t.co/jMpsNVIWLE
    geo_enabled: True
    

## 3. Tokenize tweet
** Lest look at tweet test example:**<br>
RT @Hiredscore: Our team is gearing up for @Littler's 35th annual Executive Employer Conference in Phoenix, AZ this week! Attending the con…<br>
** To analyze common words in tweet, We need to tokenize and filter tweet text**<br>
* we change all words to lower case not to have doubles
* We will use nltk library for tokenizing
* we will remove stop words a, is, the...
* we will remove un-interesting words, specific to tweeter, as: RT, &amp
* nltk tokenizing separate @ and # from the words, so if we limit word size to >1, its good enough.
* We will get user_id as a word in our list, since nltk splits @ronbon to @ and ronbon, but its interesting to the users that tweet so much about the given subject.
    


```python
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

```


```python
from nltk.corpus import stop-words
from nltk.tokenize import word_tokenize
def tokenize_tweet_text(tweet_text, Qye_words = None):
    
    word_tokens = word_tokenize(tweet_text)

    filtered_sentence = []

    for w in word_tokens:
        if w.lower() not in s_words | set(Qye_words):
            if (len(w)<= 1): continue
            if ('\\' in w): continue
            if ('/' in w): continue
                
            if (w.endswith('...')): w = w[:-4]
            if (w.startswith('...')): w = w[4:]
            if (w.endswith('-')): w = w[:-1]
            if (w.startswith('-')): w = w[1:]
            if (w.endswith('…')): w = w[:-1]
            if (w.startswith('…')): w = w[1:]
            if (w.isdigit()): continue
            filtered_sentence.append(w.lower())

    return filtered_sentence
```


```python
# Lets check the tokenizing function

example_sent = "April 2018 JAX Magazine is Out: Machine Learning. #BigData #DeepLearning #MachineLeaning #DataScience #AI #Python #RStats @filtration \\ppo."
word_tokens = tokenize_tweet_text(example_sent, Qye_words = ['BigData'])

print(word_tokens)

```

    ['april', 'jax', 'magazine', 'machine', 'learning', 'bigdata', 'deeplearning', 'machineleaning', 'datascience', 'ai', 'python', 'rstats', 'filtration']
    

## 4. Retrieve Tweet data definitions
There is a lot of data associated with each tweet. Lest view few the search fields that is relevant to our task.<br>
reference: https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
* **q	required**	A UTF-8, URL-encoded search query of 500 characters maximum, including logical operators operators. <br>
    example: <br>
    * q = 'bigdata' : will retrieve Tweets that have the word bigdata
    * q = 'puppye filter:media' : will retrieve Tweets containing “puppy” and an image or video.
* **geocode	optional**	Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferably taken from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by ” latitude,longitude,radius ”, where radius units must be specified as either ” mi ” (miles) or ” km ” (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly. A maximum of 1,000 distinct “sub-regions” will be considered when using the radius modifier.<br>
    example: 37.781157 -122.398720 1mi
* **lang	optional**	Restricts tweets to the given language, given by an ISO 639-1 code. Language detection is best-effort. We will use only English<br>
    example: eu, en
* **count	optional**	The number of tweets to return per page, up to a maximum of 100. Defaults to 15. This was formerly the “rpp” parameter in the old Search API.<br>
    example: 100
<br>
Full definition can be found here: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets


## 4.1 How can we Filter Tweet by location


When working with Tweet data, there are two classes of geographical metadata:<br>

* **Tweet location** - Available when user shares location at time of Tweet.
* **Account Location** - Based on the ‘home’ location provided by user in their public profile. This is a free-form character field and may or may not contain metadata that can be geo-referenced.
Nullable . The user-defined location for this accounts profile. Not necessarily a location, nor machine-parseable. This field will occasionally be fuzzily interpreted by the Search service. Example: "location": "San Francisco, CA"

**Important Notes:**

    * Geographical coordinates are provided in the [LONG, LAT] order. <br>
The one exception is the deprecated  ‘geo’ attribute, which has the reverse [LAT, LONG] order.

    
#### Tweet locations ("geo-tagged" Tweets)
Twitter enables users to specify a location for individual Tweets. Tweet-specific location information falls into two general categories:

    * Tweets with a specific latitude/longitude “Point” coordinate
    * Tweets with a Twitter “Place” 
Tweets with a Point coordinate come from GPS enabled devices, and represent the exact GPS location of the Tweet in question. This type of location does not contain any contextual information about the GPS location being referenced (e.g. associated city, country, etc.), unless the exact location can be associated with a Twitter Place.

Tweets with a Twitter “Place” contain a polygon, consisting of 4 lon-lat coordinates that define the general area (the “Place”) from which the user is posting the Tweet. Additionally, the Place will have a display name, type (e.g. city, neighborhood), and country code corresponding to the country where the Place is located, among other fields.

#### Author location 
Author location is an an arbitrary content that describe the author location. It is saved in authorloc variable. Author location for example can be:
* Hillingdon, London
* NY USA
Or any other content the user chose to use as location description.
** To filter our desired locations, we will check if strings such as NY or London are contained in the authorlocation filed.

## Conclusions:
### From our tests and Tweeter documentation, not more then 0.5% of the tweets has geo tagging, so to get the full picture, we will filter tweet locations by the description in the Author location field.

## 4.2 Filter tweets by time
* **since**	optional filed in tweeter retrieving. It Filter tweets created from the given date. Date should be formatted as YYYY-MM-DD. **Keep in mind that the search index has a 7-day limit**. In other words, no tweets will be found for a date older than one week!!.<br>
    example: 2015-07-19

source: https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location <br>    


```python
# Define start date of our word survey
import datetime
delta = -30
start_date = datetime.datetime.now() + datetime.timedelta(delta)
start_date = str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day)
print('Collecting tweets since: ', start_date)

```

    Collecting tweets since:  2018-4-9
    


```python
print('Collecting tweets since: ', start_date)
# TWEEPY SEARCH FUNCTION
# refernce: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
def tw_get_tweets(api,  query_in, Qye_words, geo, location, num_tweets=200):

    counter = 0
    example_tweet = None
    word_list = []
    
    # We will not use geocode inorder not to miss most of the tweets.
    for tweet in tweepy.Cursor(api.search,
                                q = query_in,           # the actual words we search
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
            word_list += tokenize_tweet_text(text, Qye_words = Qye_words)

        counter = counter +1
        if (counter >= num_tweets):
            break
    return word_list
```

    Collecting tweets since:  2018-4-9
    

 ## 5. Lets Run some tests


```python
import sys
import os
import os.path
from collections import Counter

authfile = 'auth.k'
api = tw_oauth()

df_results =  pd.DataFrame()
i = 0

Qye_words= ['bigdata']
query_in = 'BIGDATA+BigData+BigData'

# example of locations
location_list = ['NY', 'London', 'Mumbai', 'Paris']
query_list = [['NY', 'New York'], 
              ['London', 'london'],
              ['Mumbai', 'mumbai', 'bombay', 'Bombay'],
              ['paris', 'Paris']]

# lets view frequent words about Bigdata in different cities
for i in range(len(location_list)):
    
    location_words = query_list[i]

    print('Retreiving tweets since: ', start_date, ' about', Qye_words[0] ,
          ' Tweeted in locations: ',  location_list[i] )

    words = tw_get_tweets(api,  query_in, Qye_words = Qye_words,
                                      location = location_words,
                                      geo = None,
                                      num_tweets=2000)

    # lets count and sort words
    counts = Counter(words)
    word_list=[]
    freq_list=[]
    
    if (len(counts) > 0):
        for item, frequency in counts.most_common(10):
            word_list.append(item)
            freq_list.append(frequency)


        df_results[location_list[i] + '_words'] = word_list
        df_results[location_list[i] + '_freq'] = freq_list  

df_results.head(10)
```

    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  NY
    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  London
    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  Mumbai
    Retreiving tweets since:  2018-4-9  about bigdata  Tweeted in locations:  Paris
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>NY_words</th>
      <th>NY_freq</th>
      <th>London_words</th>
      <th>London_freq</th>
      <th>Mumbai_words</th>
      <th>Mumbai_freq</th>
      <th>Paris_words</th>
      <th>Paris_freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>iot</td>
      <td>29</td>
      <td>ai</td>
      <td>33</td>
      <td>machinelearning</td>
      <td>2</td>
      <td>data</td>
      <td>22</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ai</td>
      <td>25</td>
      <td>iot</td>
      <td>25</td>
      <td>kirkdborne</td>
      <td>2</td>
      <td>read</td>
      <td>20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>data</td>
      <td>15</td>
      <td>read</td>
      <td>23</td>
      <td>aftk</td>
      <td>2</td>
      <td>iainljbrown</td>
      <td>19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>cybersecurity</td>
      <td>13</td>
      <td>data</td>
      <td>21</td>
      <td>datascience</td>
      <td>2</td>
      <td>big</td>
      <td>17</td>
    </tr>
    <tr>
      <th>4</th>
      <td>tech</td>
      <td>13</td>
      <td>iainljbrown</td>
      <td>17</td>
      <td>falling</td>
      <td>1</td>
      <td>datascience</td>
      <td>17</td>
    </tr>
    <tr>
      <th>5</th>
      <td>digital</td>
      <td>13</td>
      <td>datascience</td>
      <td>17</td>
      <td>project</td>
      <td>1</td>
      <td>ai</td>
      <td>16</td>
    </tr>
    <tr>
      <th>6</th>
      <td>fisher85m</td>
      <td>11</td>
      <td>machinelearning</td>
      <td>16</td>
      <td>love</td>
      <td>1</td>
      <td>machinelearning</td>
      <td>15</td>
    </tr>
    <tr>
      <th>7</th>
      <td>vladobotsvadze</td>
      <td>11</td>
      <td>analytics</td>
      <td>15</td>
      <td>block</td>
      <td>1</td>
      <td>iot</td>
      <td>12</td>
    </tr>
    <tr>
      <th>8</th>
      <td>analytics</td>
      <td>10</td>
      <td>google</td>
      <td>12</td>
      <td>short</td>
      <td>1</td>
      <td>ml</td>
      <td>7</td>
    </tr>
    <tr>
      <th>9</th>
      <td>vr</td>
      <td>10</td>
      <td>vladobotsvadze</td>
      <td>11</td>
      <td>alert</td>
      <td>1</td>
      <td>artificialintelligence</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



## Lets query more interesting staff
Lest check the popular words in Tweets about president Trump and Iran in different countries.


```python
df_politics =  pd.DataFrame()
i = 0

# list of words that we don't want to count, because they are part of the query
# lower case is enough, because we filter words in lower case
Qye_words= ['trump', 'iran', 'president', 'us', 'america']

# build a query with logic operators
query_in ='(Trump AND Iran) OR (trump AND iran) OR (TRUMP AND IRAN)'

# define location names
location_list = ['US', 'INDIA', 'ENGLAND']

# define list of string by wich tweets are filtered
query_list = [['NY', 'New York', 'Washington', 'San Fransisco', 'US', 'USA'], 
              ['Mumbai', 'mumbai', 'bombay', 'Bombay', 'Delhi', 
               'India', 'Bangalore', 'INDIA'],
                ['London', 'london', 'Liverpool', 'England', 'Manchester']]


# lets view frequent words about Bigdata in different cities
for i in range(len(location_list)):
    
    location_words = query_list[i]

    print('Retreiving tweets since: ', start_date, ' about', Qye_words[0] ,
          ' Tweeted in locations: ',  location_list[i] )

    words = tw_get_tweets(api,  query_in, Qye_words = Qye_words,
                                      location = location_words,
                                      geo = None,
                                      num_tweets=6000)

    # lets count and sort words
    counts = Counter(words)
    word_list=[]
    freq_list=[]
    
    if (len(counts) > 0):
        for item, frequency in counts.most_common(10):
            word_list.append(item)
            freq_list.append(frequency)


        df_politics[location_list[i] + '_words'] = word_list
        df_politics[location_list[i] + '_freq'] = freq_list  

df_politics.head(10)
```

    Retreiving tweets since:  2018-4-9  about trump  Tweeted in locations:  US
    Retreiving tweets since:  2018-4-9  about trump  Tweeted in locations:  INDIA
    Retreiving tweets since:  2018-4-9  about trump  Tweeted in locations:  ENGLAND
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>US_words</th>
      <th>US_freq</th>
      <th>INDIA_words</th>
      <th>INDIA_freq</th>
      <th>ENGLAND_words</th>
      <th>ENGLAND_freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>deal</td>
      <td>436</td>
      <td>deal</td>
      <td>14</td>
      <td>deal</td>
      <td>82</td>
    </tr>
    <tr>
      <th>1</th>
      <td>nuclear</td>
      <td>149</td>
      <td>nuclear</td>
      <td>4</td>
      <td>nuclear</td>
      <td>31</td>
    </tr>
    <tr>
      <th>2</th>
      <td>decision</td>
      <td>80</td>
      <td>syria</td>
      <td>4</td>
      <td>n't</td>
      <td>19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>obama</td>
      <td>77</td>
      <td>dow</td>
      <td>3</td>
      <td>speech</td>
      <td>16</td>
    </tr>
    <tr>
      <th>4</th>
      <td>world</td>
      <td>50</td>
      <td>went</td>
      <td>3</td>
      <td>donald</td>
      <td>15</td>
    </tr>
    <tr>
      <th>5</th>
      <td>go</td>
      <td>50</td>
      <td>breaks</td>
      <td>3</td>
      <td>fact</td>
      <td>14</td>
    </tr>
    <tr>
      <th>6</th>
      <td>kurteichenwald</td>
      <td>38</td>
      <td>celebrate</td>
      <td>3</td>
      <td>buckle</td>
      <td>14</td>
    </tr>
    <tr>
      <th>7</th>
      <td>went</td>
      <td>37</td>
      <td>facts</td>
      <td>3</td>
      <td>reckless</td>
      <td>14</td>
    </tr>
    <tr>
      <th>8</th>
      <td>stocks</td>
      <td>37</td>
      <td>energy</td>
      <td>3</td>
      <td>checked</td>
      <td>14</td>
    </tr>
    <tr>
      <th>9</th>
      <td>iranian</td>
      <td>37</td>
      <td>matter</td>
      <td>3</td>
      <td>nowthisnews</td>
      <td>14</td>
    </tr>
  </tbody>
</table>
</div>

## Twitter Tips
### printing - causing problems due to character the Twitter creates.
Worked for me only with the following:
```
from bs4 import BeautifulSoup
def my_print(s):
    soup = BeautifulSoup(s)
    print(soup.encode("utf-8"))
```
