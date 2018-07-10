## # Experimenting with Google Cloud
### BigTable, MongoDB and Dockers
Google gives 300$, so its a good opertunaty to experiment. In this toy project, I chose to explore Google cloud Platform (GCP) utilities to run an app that listen, analize and save texte. I used python script listening to Tweeter stream as testing app. The goal was to filter, tokenize and save tweets containing a kye word, and compare most popular words in different locations.
I tried 2 ways, one with BigTable, Hbase, DataProc, Python and Java. The second with MongoDB, Python and Docker.
## Project 1. Python and Java Project on Google Cloud with BigTable and DataProc
Here I wrote python script to retrive tweets, filter, tokenize words, and save them in BigTable data base. Then I run Hadoop Mapreduce, to count word frequencies. Mapreduce was not really needed here, it was written mainly for learning purposes.
## Project 2. Python, MongoDB and Docker.
Here I worte a python script to listen to Tweeter stream, filter , tokenize and save words to MongoDB collections.Compar 2 Tweet mining project
Here is a short summary of comparing the projects.

| Item  | BigTable - Google cloud VM | MongoDB - Docker - Kubernete |  
| ------------- | ------------- | ------------- | 
|  Twitter API | Twitter REST - mine historical Tweets  | Twitter Stream - Listen to stream  |
|  DataBase | Google Cloud BigTable, Hbase  | mLab, MongoDB , pymongo |
|  Programming tools| Java, Hadoop , MapReduce | Python, pymongo |
|  Running on | VM machine on Google cloude |  Dockers on Kubernetes Google cloud engine |
|  Results obtained | most frequent words per location  | Collections of word frequency by location  |
|  Running time  | 3-5 min to initialize | mine 100 relevant twitts in less then a minute  |
|  Ease of use | Developing on Google cloud is complicated and not convinient  | MongoDB and Docker are eassy to use and fast to learn |
|  Scalability | Google Cloud BigTable, Hbase  | mLab, MongoDB , pymongo |
|  Computation costs  | havey, learning time is long  | light, most of the work is done on your local machine |

## My conclusions
### Dockers and Containers vs Virtual Machine
Working with Dockers was eassy and practical. I wrote and tested the code on mt local machine, then in few simple steps, I could run in on  Kubernete engine.  all the source on 
### MongoDB vs BigTable
Here MongoDB wins. Learning is eassy and fast, authentication is painless and work smoothly from any environment.
