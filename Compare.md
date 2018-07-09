In my Google Cloud toy project, I expirienced many platform and tools. Here is a short summary of comparing the projects.

| Item  | BigTable VM | MongoDB Docker |
| ------------- | ------------- | ------------- |
|  Twitter API | REST  | Stream  |
|  DataBase | BigTable, Hbase  | MongoDB , pymongo |
|  DataBase Provaider | Google Cloud  | mLab |
|  Map Reduce | Hadoop  | Kubernetes |
|  Results obtained | 5 top words for one location  | a collection of word freq by location  |
|  Running time for both systems  | ¬5 min as we reset the bucket | 100 relevant twitts / min  |
|  Ease of use, the ability to make changes to both systems  | very easy since input is word and location  | not easy - needs to deploy image (could be easy be using client node)  |
|  Computing costs in both cases  | very have (map reduce, restart bucket)  | lighter  |
