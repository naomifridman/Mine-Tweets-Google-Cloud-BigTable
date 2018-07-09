## Compar 2 Tweet mining project
In my Google Cloud toy project, I expirienced many platform and tools. Here is a short summary of comparing the projects.

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
