#!/usr/bin/python

import sys
import pymongo

### Create location data


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
	
    dont_delete = []
    dont_delete.append('system.indexes')
    print(dont_delete)
    for col in db.collection_names():
        
        #print(col not in dont_delete)
        if (col not in dont_delete):
            print('deleting', col)
            db.drop_collection(col)
	
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])