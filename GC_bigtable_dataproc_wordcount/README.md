# How I managed to run MapReduce Google Cloude Example 
## And run it on words from Twitter collected by Python script
Let's start the Google cloud tour, with running the famous  MapReduce WordCount BigTable DataProc example. I found that deploying and running this example, took longer then expected. So I forked the example to my git, made some small modifications, and wrote few short guides for each step. <br>
Example repository:https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/tree/master/java/dataproc-wordcount

## Step 1. Set up GCP, Open VM and install Java and Python
Create and configure you GCP account and resources. Walk through begginer guide to set up project in Google Cloud Platform, GCP:<br>
https://github.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud/blob/master/GC_setup_guid.md

Steps are:
* Create Google Cloud account (choose "Individual"), enable billing and Google Cloud APIs
* Select or create a GCP project.
* Enable Google Cloud APIs in GCP->API & Services->Dushboard<br>, or choose enable all APi's in VM creation.
* Create BigTable cluster, this is your data cluster, write the name.
* initilize project parameters with: `gcloud init`
* Install Java, Haddop, Maven
* Install Python, and Python clients for Google Cloud storage.
<br>
Write down project parameters:<br>
* Zone: us-east1-c
* Project id: naomi-topnwords
* Cluster id: naomi-mapreduce-bigtable

#### Credentials
When working in VM opened in browser from GCP, credentials and authentication are done under the cover.

#### Google SDK 
in already installed on the VM instance.

## Step 2. Create Project storage
You need to create Buckets for data storage of the project.<br>
You can create them in GCP console menu:
* GCP -> Storage -> Browser
Or you can create them in your VM with Java Cloud SDK tool, gsutil:<br>
```
gsutil mb -p <project ID> gs://<bucketName>
# For example
gsutil mb -p naomi-topnwords gs://naomi-bucket
```
Make your Buckets pablic:
```
gsutil defacl set public-read gs://naomi-bucket
```
You can give any unique name to the Bucket.


## Step 3. Clone and Configure MapRduce example.
Since it was tedious to configure the original example, I copied it to my git, and made some modifications.
Clone mt modified example:
```
git clone https://github.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud.git
cd Top-N-Words-In-Tweets-Google-Cloud/GC_bigtable_dataproc_wordcount/
#mvn clean package -Dbigtable.projectID=YOUR_PROJECT_ID -Dbigtable.instanceID=YOUR_INSTANCE_ID
mvn clean package -Dbigtable.projectID=naomi-topnwords -Dbigtable.instanceID=naomi-mapreduce-bigtable 
```
You should see something like this:
```
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 45.303 s
[INFO] Finished at: 2018-05-07T20:00:31+00:00
[INFO] Final Memory: 73M/753M
[INFO] ------------------------------------------------------------------------
```
## Step 4. Deploy MapReduce Example
#### Create Google Cloud DataProc cluster
This cluster, is the one asctually runing the jobs. We need to create DataProc cluster, with same name as the BigTable cluster, annd same features as the VM you created.<br>
You can create the DataProc cluster in few ways:
* GCP Console: GCP->DataProc->Clusters->Create
* ./cluster.sh create <bucket name>
* Manualy from command line with Google Cloud SDK
The original command is:
```
gcloud dataproc clusters create "${CLUSTER}" \
    --bucket "$2" \
    --num-workers 4 \
    --zone $ZONE \
    --master-machine-type n1-standard-4 \
    --worker-machine-type n1-standard-4
```
Edit the this part of `cluster.sh` file to suit the number of workers and Cpu's that where chosen for the VM instance. If follow this example, change it from 4 to 2. while you at it, change the default zone and default cluster defined in the file.<br>
Manually from command line, run:
```
gcloud dataproc clusters create "naomi-mapreduce-bigtable" \
    --bucket "naomi-bucket" \
    --num-workers 2 \
    --zone us-east1-c \
    --master-machine-type n1-standard-2 \
    --worker-machine-type n1-standard-2
```
*Minimum workers for mapreduce are 2.*<br>
Or run with script:
```
chmod a+x cluster.sh 
./cluster.sh create naomi-bucket
```
On successful creation, you should see something like:
```
Waiting on operation [projects/[Project-Id]/regions/global/operations/b811e0c2-2f6b-420e-a4d5-bc846326f9c5].
Waiting for cluster creation operation...done.                                         
Created [https://dataproc.googleapis.com/v1/projects/naomi-mapreduce/regions/global/clusters/naomi-mapreduce-bigtable] Cluster placed in zone [us-central1-b]
```
View the created cluster, in GCP console:
![DataProc Cluster](https://raw.githubusercontent.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud/master/assets/GCP_console_dataproc_clusters.png)<br>

## Step 5. Run MapReduce word count BigTable DataProc example
As before, we can run the actual job, from `cluster.sh' or manually from command line:
```
#./cluster.sh start  <your BigTable instance> 
./cluster.sh start  naomi-mapreduce-bigtable 
```
Or run Manually:
```
gcloud dataproc jobs submit hadoop --cluster naomi-mapreduce-bigtable \
    --jar target/wordcount-mapreduce-1.0-jar-with-dependencies.jar \
    -- wordcount-hbase \
    gs://lesv-big-public-data/books/book \
    gs://lesv-big-public-data/books/b6130 \
    "words-count"
```
Where, gs://name are list of input public files, wordcount-hbase is the main class and last parameter is the output HBase table. In the original example jar file are saved in GC bucket, I changt it to local since I needed to examine it.<br>
The actual command that is running on the dataproc cluster is:
```
hadoop jar target/wordcount-mapreduce-1.0-jar-with-dependencies.jar  wordcount-hbase     gs://naomi-bucket/tweet/tweet_words.txt  "words-count"
```
To test your Jar, you can run mapreduce on small local txt file:
```
hadoop jar target/wordcount-mapreduce-1.0-jar-with-dependencies.jar  wordcount-hbase     small_file.txt  "words-count"
```
To test your GC setup, you can copy your small text file to bucket, and run mapreduc wordcount on your dataproc cluster:
```
gsutil cp  small_file.txt gs://naomi-bucket/tweet 
gcloud dataproc jobs submit hadoop --cluster naomi-mapreduce-bigtable     --jar target/wordcount-mapreduce-1.0-jar-with-dependencies.jar     -- wordcount-hbase     gs://naomi-bucket/tweet    "test-words-count"
# to check results run
python3 hbase_table_head.py --table "test-words-count" naomi-topnwords naomi-mapreduce-bigtable
```
On succsefull run, you should see somthing like:
```
- name: word count
  progress: 1.0
  state: FINISHED
  trackingUrl: http://naomi-mapreduce-bigtable-m:8088/proxy/application_1525724630856_0001/
Output table is: words-count
```
## Step 6. view the results
In GCP boser menue at: GCP > Dataproc > Jobs, you can see the log of the project's job.<br>
To View the results, you have 2 choices:
* Hhbase shell. 
* Use pythgon tools
### HBase Shell
Install it from the original example:<br>
https://cloud.google.com/bigtable/docs/quickstart-hbase <br>
```
cd
git clone https://github.com/GoogleCloudPlatform/cloud-bigtable-examples.git
cd cloud-bigtable-examples/quickstart/
./quickstart.sh 
```

Few basic hbase shell comands:<br>
List the tables:
```
list
```
To output the table content:
```
scan "table name"
```
output table description:
```
describe "table name"
```

Count rows in table, will also print a rowa once in 1000 raes:
```
count "table name
```
Will output somthing like:
```
Current count: 121000, row: vainest                                                                               
Current count: 122000, row: vitae,                                                                                
Current count: 123000, row: wearing.                                                                              
Current count: 124000, row: will'd)                                                                               
Current count: 125000, row: wound,)                                                                               
125778 row(s) in 0.9430 seconds
```
Output 5 rows of the table:
```
scan "table name" ,{RAW => true, LIMIT =>5} 
```
will Output:
```
ROW                           COLUMN+CELL                                                                                              
 yearly                   column=cf:count, timestamp=1527121094736, value=\x00\x00\x00\x01                                   
 yearn                    column=cf:count, timestamp=1527121103964, value=\x00\x00\x00\x01                       
 years                    column=cf:count, timestamp=1527121103964, value=\x00\x00\x00&                                   
 years'                   column=cf:count, timestamp=1527121094736, value=\x00\x00\x00\x02                                 
 years)                   column=cf:count, timestamp=1527121103964, value=\x00\x00\x00\x01         
 d>                                                                                                               
5 row(s) in 0.2130 seconds
```
The data in columns is saves in bytes, while the key data is saved as is. We can see that in the Reducer java code:
```
public void reduce(ImmutableBytesWritable key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
      int sum = sum(values);
      Put put = new Put(key.get());
      put.addColumn(COLUMN_FAMILY, COUNT_COLUMN_NAME, Bytes.toBytes(sum));
      context.write(null, put);
    }
 ```
Exit the HBase shell:
```
exit
```
### Python tools
Use the python utils from this git. 
#### 
```
cd
cd Top-N-Words-In-Tweets-Google-Cloud/python_BigTable_utils/
python3 hbase_table_head.py --table "words-count" naomi-topnwords naomi-mapreduce-bigtable
```
Output, in bytes:
```
1  word:  "'Tis count:  9
2  word:  '!=' count:   9
3  word:  '"(PrefixFilter'  encoded:  2
4  word:  '"\'Tis' count:   9
5  word:  '"\'Tuque' count:   1
```
####
```
$ python3 hbase_table_topn_by_value.py --table 'words-count' naomi-topnwords naomi-mapreduce-bigtable 
```
Will outpot:
```
existing tables:  ['words-count']
Scanning all words in table:  words-count
column_name  cf:count
b'the' 20802
b'to' 7613
b'of' 7529
b'and' 7216
b'<div' 6579
```
You can edit the python utilities, for scpecific column_family, to output int values and not byte strings.

## Step 7 Collect Tweet words with Python
The python script `collect_tweets_to_csv.py`, retrives tweets from Twitter API, filter them by query and location, and save to txt file. Detailed description abouy tweet mining in the mine_tweet.<br>
Copy the txt file to a bucket in your storage with GC SDK.
As example, run, with default query: `(Royal AND wedding) OR (wedding AND Meghan) OR (Harry AND wedding) OR (Harry AND Meghan)`
and location London, will output:
```
      London
0 royalcentral
1     princess
2    charlotte
3         boss
4   bridesmaids
```
Copy the file to your storage bucket:
```
gsutil cp tweet_words.txt gs://naomi-bucket
```
## Step 8 High frequency words with MapReduce wordcount on Tweet words
Run MapReduce on the txt file containing words filtered from tweets:
```
'gcloud dataproc jobs submit hadoop --cluster naomi-mapreduce-bigtable \
    --jar target/wordcount-mapreduce-1.0-jar-with-dependencies.jar \
    -- wordcount-hbase \
    gs://naomi-bucket/tweet_words.txt \
    "tweet-words-count"
 ```
 The tweets we retrive is not really a lot, so running the topn python tool will show:
 ```
$python3 hbase_table_topn_by_value.py --table 'tweet-words-count' naomi-topnwords naomi-mapreduce-bigtable 
existing tables:  ['tweet-words-count', 'words-count']
Scanning all words in table:  tweet-words-count
column_name  cf:count
b'princess' 24
b'like' 18
b'thank' 9
b'accepting' 9
b'bridesmaids' 3
```
## Step 9. Compare Tweets in different locations
Just for fun of comparing, a poorly written script is added that run all the proces in a loop on different locations, and presets results for each location. Run with default query and location:
```
run_if_all_on_gc.py -q "Trump"
```
You can get for example:
```
#-- Python collect tweets about Trump in location NY
Retreiving tweets since:  2018-4-27  about: Trump
Tweeted in locations:  NY
Example of words in Tweets about: Trump

            NY
0    b'shaunking
1     b'complete
2  b'fabrication
3          b'law
4       b'exists
# -- then mapreduce wordcount run on the file and produce:
NY_freq NY_words            London_frea London_words   
3      b'administration       3     b'people
1      b'obama                2     b'children
1      b'fabrication          2     b'ice
1      b'policy               1     b'renedenfeld
1      b'reminding            1     b'point
#-- running with location Dublin ...
NY_freq NY_words         London_frea London_words  Dublin_freq Dublin_words 
3      b'administration  3       b'people              3           b'upset
1      b'obama             2     b'children            3           b'media
1      b'fabrication       2     b'ice                 1           b'full
1      b'policy            1     b'renedenfeld         1           b'bannon
1      b'reminding         1     b'point               1           b'call
```
// TODO
Twitter respons is not always reliable. To get more clean tweets, run in a loop on time lap of 16 minutes, and handle all exceptions.
## Clean up
There is a cleaning script in the example:
```
#gcloud -q dataproc clusters delete <cluster id>
gcloud -q dataproc clusters delete naomi-mapreduce-bigtable
```
I think its a good idea to delete everything from GCP browser menu. Or enable billing
### Trouble Shooting
* If you get the following error:<br>
```
ERROR: (gcloud.dataproc.clusters.create) INVALID_ARGUMENT: Default Service Account '[PROJECT NUM]-compute@developer.gserviceaccount.com' is missing required permissions: [dataproc.agents.create, dataproc.agents.get, dataproc.agents.update, dataproc.tasks.lease, dataproc.tasks.listInvalidatedLeases, dataproc.tasks.reportStatus]. Service Accounts must have either 'Dataproc/Dataproc Worker' role or all permissions granted by the role. See https://cloud.google.com/dataproc/docs/concepts/iam for further details.
```
You need to grand Dataproc worker role to the default service account associated with the project.<br>
* If you get the following error:
```
(gcloud.dataproc.clusters.create) INVALID_ARGUMENT: Bucket is requester pays bucket but no user project provided.
```
In GCP browser menu: Choose GCP->Storage->Browser, set to off the Requester pays  column for each bucket you want to enable. Link to the resource: https://cloud.google.com/storage/docs/requester-pays<br>

* For hadoop issues, try set or correct hadoop enviorment variables.
```
HADOOP_HOME=$HOME/hadoop
export HADOOP_HOME
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/native"

```
* You don't need to authenticate, but sometimes it solves issues, run:
```
gcloud auth application-default login
```
## Terminology and Initials
### Google Cloud BigTable and HBase.
HBase is a NoSQL database. It is based on Google’s Bigtable distributed storage system – as it is described in Google research paper; “A Bigtable is a sparse, distributed, persistent multi-dimensional sorted map. The map is indexed by a row key, column key, and a timestamp; each value in the map is an uninterpreted array of bytes.” 
* GCP - Google Cloud Platform

## Reference
* http://hbase.apache.org/0.94/book/mapreduce.example.html
Good reference for hadoop mapreduce options

