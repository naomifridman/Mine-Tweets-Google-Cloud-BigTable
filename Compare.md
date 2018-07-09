In this section i would compare the use of docker and streaming using mongodb to mapreduce and rest API using cloud bucket:  

| compare item  | BigTable VM | MongoDB Docker |
| ------------- | ------------- | ------------- |
|  Twitter API | REST  | Stream  |
|  DB | BigTable, Hbase  | MongoDB  |
|  DB Location | Cloud bucket  | mLab |
|  Map Reduce | Hadoop  | Kubernetes |
|  Results obtained | 5 top words for one location  | a collection of word freq by location  |
|  Running time for both systems  | ¬5 min as we reset the bucket | 100 relevant twitts / min  |
|  Ease of use, the ability to make changes to both systems  | very easy since input is word and location  | not easy - needs to deploy image (could be easy be using client node)  |
|  Computing costs in both cases  | very have (map reduce, restart bucket)  | lighter  |
