#!/usr/bin/python

import sys
import pymongo

### Create location data

LOCATION_DATA = [
    {
        'location': 'London',
        'isTaken': 0
    },
    {
        'location': 'Washington',
        'isTaken': 0
    },
    {
        'location': 'NY',
        'isTaken': 0
    },
	{
        'location': 'Liverpool',
        'isTaken': 0
    },
	{
        'location': 'Dublin',
        'isTaken': 0
    }
]

THE_WORDS = ['trump']

def list_locations(mydb):

    for doc in mydb.find():
        print(doc) # iterate the cursor
    
###############################################################################
# main
###############################################################################

def main(args):

    connection = pymongo.MongoClient('ds121861.mlab.com', 21861)
    db = connection['python_twitter']
    
    db.authenticate('test', 'nnnn1858')
	
    # First we'll add a few songs. Nothing is required to create the songs 
    # collection; it is created automatically when we insert.

    locations = db['locations']
    print('===========================================')
    print('locations', locations)
	
    # Note that the insert method can take either an array or a single dict.
    db.drop_collection('locations')
    locations.insert_many(LOCATION_DATA)

    list_locations(locations)
    # insert the word to mongodb
	
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])