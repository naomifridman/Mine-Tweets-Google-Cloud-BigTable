import sys
import pymongo

# Locations collection has the form:
#        'location': 'London',
#        'isTaken': 0
#
# words collection has the form:
#        'word': 'something',
#		 'location' : London
#        'count': 0
# words_nolocation collection has the form:
#        'word': 'something',
# 
### database parameters

dbuser = 'test'
dbpassword = 'nnnn1858'
dbname = 'python_twitter'
host = 'ds121861.mlab.com'
port = 21861
#-----------------------------------------------------------------------
# util functions
def list_db(mydb, n=0):
	i = 0
	for doc in mydb.find():
		if (n > 0 and i>n): break
		i += 1
		print(doc)
		
def list_coolections(db):
    
    print(db.collection_names())
	
def delete_collections(db, dont_delete = []):
    
    dont_delete.append('system.indexes')
    print(dont_delete)
    for col in db.collection_names():
        print(col)
        print(col not in dont_delete)
        if (col not in dont_delete):
            db.drop_collection(col)
			
def reset_location_taken(locations):
    
    locations.update_many({"isTaken": 1}, {'$set': {'isTaken': 0}})
def reset_db():
    list_coolections(db)
    delete_collections(db, dont_delete = ['locations'])
    list_coolections(db)
    reset_location_taken(locations)


def connect_to_db():
    
    # Connect to data base
    connection = pymongo.MongoClient(host, port)
    db = connection[dbname]
    
    db.authenticate(dbuser, dbpassword)
    print('db', db)
    return db, connection
	

#----------------------------------------------------------------
# gloval variables
db = None
connection = None
location = None
	
###############################################################################
# main
###############################################################################
LOCATION_NAME = ['London','Washington','NY','CA']

def main(args):
	
	# connect to data base
	db, connection = connect_to_db()
	topn = 5
	
	words = db['words']
	

	print()	
	print('view few  lines of words collection')
	i = 0
	for doc in db.words.find().limit(10):
		print(doc)
	print()
	
	print()
	print('******** view top words by location')
	print()

	for j in range(len(LOCATION_NAME)):
		location = LOCATION_NAME[j]
		print()
		print('******* Top words in: ', location)
		i = 0
		for post in words.find({'location': location}).sort([("count", pymongo.DESCENDING)]):
			i+=1
			print (post['word'], post['count'])
			if (i > topn): break
	print()
	print('******** view top words by location, from all location')
	print()
	i = 0
	for post in words.find({}).sort([("count", pymongo.DESCENDING)]):
		i+=1
		print (post['word'], post['location'], post['count'])
		if (i > topn): break

	print()
	print('******** view top words over all location')
	print()
	
	words_without_location = db['words_without_location']
	for post in words_without_location.find({}).sort([("count", pymongo.DESCENDING)]).limit(5):
		print (post['word'],  post['count'])


	connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])