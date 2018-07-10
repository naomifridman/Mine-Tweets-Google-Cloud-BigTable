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

def find_words_in_all_location_old(db):
	
	words_without_location = db['words_without_location']
	words = db['words']
	db.drop_collection('tmp')
	db_tmp = db['tmp']
	
	for post in words_without_location.find():#.limit():
		the_word = post['word']
		found = True
		for j in range(len(LOCATION_NAME)):
			in_this_location=False
			location_c = LOCATION_NAME[j]
			for doc in words.find({'word': the_word, 'location': location_c}).limit(1):
				in_this_location = True
			if(not in_this_location):
				found=False
				break
		
		if (found):
			db_tmp.insert_one({ 'word': the_word, 'count':post['count']})
	#print('db_tmp')
	#list_db(db_tmp)
	print('********** View top-words that apear inall the locations **')
	for post in db_tmp.find().sort([("count", pymongo.DESCENDING)]).limit(5):
		print(post['word'], post['count'])	
	#db.drop_collection('tmp')
def tmp(db):
	we= 'test1'
	words_without_location = db['words_without_location']
	words = db['words']
	for post in words_without_location.find({'word':we}):
		print(post)
	for post in words.find({'word':we}):
		print(post)
		
def find_words_in_all_location(db):
	
	words_without_location = db['words_without_location']
	words = db['words']
	db.drop_collection('tmp')
	db.drop_collection('db_words_in_all_locations')
	db.drop_collection('db_words_in_all_locations')
	db_words_in_all_locations = db['db_words_in_all_locations']
	db_words_in_one_locations = db['db_words_in_one_locations']
	
	for post in words_without_location.find():#.limit():
		the_word = post['word']
		found = True
		n_locations=0
		for j in range(len(LOCATION_NAME)):

			in_this_location=False
			location_c = LOCATION_NAME[j]
			n = words.find({'word': the_word, 'location': location_c}).limit(1)
			#words.count({'word': the_word, 'location': location_c})
			if (n):
				in_this_location = True
				n_locations += 1
			if (not in_this_location):
				found=False
				break
		
		if (n_locations == 1):
			db_words_in_one_locations.insert_one({ 'word': the_word, 'count':post['count']})
		if (n_locations == len(LOCATION_NAME)):
			db_words_in_all_locations.insert_one({ 'word': the_word, 'count':post['count']})
	#print('db_tmp')
	#list_db(db_tmp)
	print()
	print('********** View top-words that apear in all the locations **')
	print()
	for post in db_words_in_all_locations.find().sort([("count", pymongo.DESCENDING)]).limit(5):
		print('***: ', post['word'], post['count'])	
		for doc in db.words.find({'word': post['word']}):
			print(doc['word'], doc['location'], doc['count'])
		print()
	print('********** View top-words that apear in one locations **')
	print()

	for post in db_words_in_one_locations.find().sort([("count", pymongo.DESCENDING)]).limit(5):
		for w in words.find({ 'word': the_word}):
			print(w['word'], w['count'])	
		
	#db.drop_collection('tmp')
	
def find_words_in_all_location_old(db):
	
	words_without_location = db['words_without_location']
	words = db['words']
	db.drop_collection('tmp')
	db_tmp = db['tmp']
	
	for post in words_without_location.find().limit(200):
		the_word = post['word']
		found = True
		for j in range(len(LOCATION_NAME)):

			in_this_location=False
			location_c = LOCATION_NAME[j]
			n = words.find({'word': the_word, 'location': location_c}).limit(1)
			#words.count({'word': the_word, 'location': location_c})
			if (n):
				in_this_location = True
			if (not in_this_location):
				found=False
				break
		
		if (found):
			db_tmp.insert_one({ 'word': the_word, 'count':post['count']})
	#print('db_tmp')
	#list_db(db_tmp)
	print()
	print('********** View top-words that apear inall the locations **')
	print()
	for post in db_tmp.find().sort([("count", pymongo.DESCENDING)]).limit(5):
		print(post['word'], post['count'])	
	#db.drop_collection('tmp')
		
def find_words_only_in_given_location(db, the_location):
	
	db_only_in_location = db['only_in_location']
	words = db['words']
	words_without_location = db['words_without_location']
	
	for post in words.find({'location': the_location}):#.limit(200):
		the_word = post['word']
		not_found = True
		for j in range(len(LOCATION_NAME)):
			#print('loking for:', the_word, ' in location ', LOCATION_NAME[j])
			location_c = LOCATION_NAME[j]
			if (location_c == the_location): continue
			n = words.count({'word': the_word, 'location': location_c})
			#doc in words.find({'location': location_c}).limit(1):
			if (n > 0):
				not_found = False
				break
		if (not_found):
			db_only_in_location.insert_one({ 'word': the_word, 'count':post['count']})
	
	for post in db_only_in_location.find().sort([("count", pymongo.DESCENDING)]).limit(5):
		print(post['word'], post['count'])
	db.drop_collection('only_in_location')
	
def tmp_test(db):
	
	w = ['aa','bb','aa','cc','b','bb']
	lo= 'local'
	db.drop_collection('tt')
	tt = db['tt']
	for we in w:
		print('before entring ', we)
		list_db(tt)
		doc = tt.find_one_and_update(
			{ 'word' : we , 'location' : lo},
			{ '$inc': { "count": 1 } },
			upsert=True)
		print('after entring ', we)
		list_db(tt)
#----------------------------------------------------------------
# gloval variables
db = None
connection = None
location = None
	
###############################################################################
# main
###############################################################################
LOCATION_NAME = ['London','Washington','NY','CA']
LOCATION_NAME_PRINT = ['London','Washington','NewYork','California']

def main(args):
	
	# connect to data base
	db, connection = connect_to_db()

	
	words = db['words']

	for post in words.find().sort([("count", pymongo.DESCENDING)]).limit(7):
	
		print(post['word'], post['count'])

	connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])