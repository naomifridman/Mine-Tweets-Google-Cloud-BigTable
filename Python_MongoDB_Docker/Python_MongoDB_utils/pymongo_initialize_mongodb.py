#!/usr/bin/python

import sys
import pymongo

### Create location data

LOCATION_DATA = [
    {
        'location': 'London',
        'isTaken': 0,
		"consumer_key": u'ZSmlxcmobz32HKzL2w8MtFKt2',
		"consumer_secret": u'IIuYGyQIBthbwadzXQjLjYAie6DgogbY1GuU4rpo7Ab21lCVWS',
		"access_token": u'338343863-H2rz5dItEJX4pq9lYBjEVCeE8Q8GfMWWRgiMGNkZ',
		"access_token_secret": u'3TB7TYqRjZvrclUYhZWhlEI8kfAt9vEFlXz9BcS7gKAUp'
    },
    {
        'location': 'Washington',
        'isTaken': 0,
		"consumer_key": u'ZSmlxcmobz32HKzL2w8MtFKt2',
		"consumer_secret": u'IIuYGyQIBthbwadzXQjLjYAie6DgogbY1GuU4rpo7Ab21lCVWS',
		"access_token": u'338343863-H2rz5dItEJX4pq9lYBjEVCeE8Q8GfMWWRgiMGNkZ',
		"access_token_secret": u'3TB7TYqRjZvrclUYhZWhlEI8kfAt9vEFlXz9BcS7gKAUp'
    },
    {
        'location': 'NY',
        'isTaken': 0,
		"consumer_key": u'zAPC4qAvnkTs1jNWYNlpBkNvY',
        "consumer_secret": u'VmLswihKAgfMkdO6NBME7l9KEvowQATVJFGeO3tbhdcJvfU7AQ',
        "access_token": u'1015931275515957248-1n05zMR4zHt6TtS9bVseBGdgrfSSHk',
        "access_token_secret": u'XGVlLnAOhGCQkavhw9zLebqtODg3OYpZqUYW7yEKeOkP1'

    },
	{
        'location': 'CA',
        'isTaken': 0,
		"consumer_key": u'zAPC4qAvnkTs1jNWYNlpBkNvY',
        "consumer_secret": u'VmLswihKAgfMkdO6NBME7l9KEvowQATVJFGeO3tbhdcJvfU7AQ',
        "access_token": u'1015931275515957248-1n05zMR4zHt6TtS9bVseBGdgrfSSHk',
        "access_token_secret": u'XGVlLnAOhGCQkavhw9zLebqtODg3OYpZqUYW7yEKeOkP1'
    },
]

THE_WORDS = ['trump']

def list_locations(mydb):

    for doc in mydb.find():
        print(doc['location'], 'isTaken: ',doc['isTaken']) 
    
###############################################################################
# main
###############################################################################

def main(args):

    connection = pymongo.MongoClient('ds121861.mlab.com', 21861)
    db = connection['python_twitter']
    
    db.authenticate('test', 'nnnn1858')
	
    # First we'll add a few songs. Nothing is required to create the songs 
    # collection; it is created automatically when we insert.

	
    # Note that the insert method can take either an array or a single dict.
    db.drop_collection('locations')
    locations = db['locations']
    locations.insert_many(LOCATION_DATA)
	
    locations = db['locations']
    print('===========================================')
    print('locations', locations)

    list_locations(locations)
    # insert the word to mongodb
    db.drop_collection('track_words')
    track_words = db['track_words']
    track_words.insert_one({ 'the_words': THE_WORDS})
    print('===========================================')
    print('the track words')
    for doc in track_words.find():
        print(doc)
	
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])