# Hadoop MapReduce Word Count on Tweeter text 

This is a fun project to experience Google Cloud Platform computation and Data bases, for BigData projects. mining Tweeter tweets, filtered by location  with Python. The finding the popular ones with mapreduce on Google Cloud. Last step is connect to HBase table with Python, and print the most popular words, for each location.<br>

Google documentation is very clear, but finding the right one requieres deep learning :).  The examples are well coded, but almost no documention, scripts and installation instructions are outdated. <br>




As a learning project I chose a fun data mining project: finding the most popular words in Tweets about a certein subject, and compare top words from different locations.<br>
The Project contains:
* Python script that retrives words from Twets
* Java WordCount class, to count (and sort) the words
* Python script to read the data.


## Working with Google Cloud Data Base
There are 2 options for data base. BigTable and Big Query.<br>
BigQuery is a query Engine for datasets that don't change much, or change by appending. It's a great choice when your queries require a "table scan" or the need to look across the entire database. Think sums, averages, counts, groupings. BigQuery is what you use when you have collected a large amount of data, and need to ask questions about it.<br>

BigTable is a database. It is designed to be the foundation for a large, scaleable application. Use BigTable when you are making any kind of app that needs to read and write data, and scale is a potential issue.<br>
Explanation from: `https://stackoverflow.com/questions/39919815/whats-the-difference-between-bigquery-and-bigtable`<br>
In this example we use BigTable.
To access database from Java code, we use Hadoop HBase<br>
To access database from Python code, we use HappyBase which is a Python client library for HBase.

## Before you begin
You need to setup a Google Cloud project. You can follow the walk through guide here:<br>
https://github.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud/blob/master/GoogleCloudSetUpForrunningBigTableDataProcExamples.md<br>
Or you can use the following Google documentation:

https://cloud.google.com/bigtable/docs/quickstart-hbase#before_you_start<br>
Generally steps are:
* create project, enable billing, enable Google API's
* Create BigTable Cluster.
* Create connect and open in browser, VM instance.
* Initialize Google cloud

## Step 1. Install Python on Google cloud VM instance
You need to install Python, virtual env and Python Google Cloud BigTable and DataProc packages. For detailed walk through, you can foolow the guide:<br>
https://github.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud/tree/master/python_BigTable_utils<br>
Or you can use the following Google documentation:
https://cloud.google.com/python/<br>
If you're not interested in the details, just run the following code In your vm instance:
```
gcloud init #if you haven't done that already
sudo apt update
sudo apt install python python-dev python3 python3-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install --upgrade virtualenv
virtualenv env
source env/bin/activate
#deactivate env
pip install google-cloud
pip install google-cloud-happybase
pip install google-cloud-dataproc
```

## Step 3.  Python Tweeter text  retrieval
For the sake of this example, I wrote simple python file to retrieve tweets that are about BigData, and where tweeted in user selected location.<br>
To run the example, you will need to install the following Python libraries. You can install them from the Google cloud given bandle:<br>
https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27<br>
For simplicity, I installed them manualy with sudo:
```
sudo pip install numpy
sudo pip install pandas
sudo pip install nltk
```
Install Tweeter Python libraries
```
sudo pip install tweetpy
```
Now you can run `collect_tweets_to_file.py `. <br>
The UI is super basic, meant just to demonstrate the basic ideas and methods.<br>
* Parameters are a list of location names to be used in the Tweeter query
* The python code, retrieves all Tweets from last week, which contains variations of the word **"BigData"**.
* The words are filtered with nltk Python library, with addition of few manual cleaning specific to Tweeter style text.
* Output is a txt file that contain the filtered Tweet words.
* If no parameters are given, default location of "NewYork" is used.
Usage example:
```
$ python collect_tweets_to_file.py London london LONDON 
# outputs
Retreiving tweets since: ', '2018-4-8' About BigData Tweeted in locations: ['London', 'london', 'LONDON'])
245  Words collected and saved in: 'London/tweets_from_London.txt'
$ bin/hadoop fs -cat London/tweets_from_London.txt 
# outputs
IainLJBrown
Change
Coming
Artificial
Intelligence
Healthcare...
```
Another Usage example:
```
$ python collect_tweets_to_file.py "New York" NY Newyork NEWYORK NewYork
# outputs
Retrieving tweets since:  2018-4-8  About BigData Tweeted in locations:  ['New York', 'NY', 'Newyork', 'NEWYORK', 'NewYork']
1097  Words collected and saved in  New_York\tweets_from_New_York.txt
```
project, cluster and vm instance.
## Step 3. WordCount with Hadoop MapReduce
Source code is tasken from the following btilient tutorial.<br>
**Reference: https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html**<br>
Copy WordCount java class from the tutorial into WordCount.java file.<br>
To install and run WordCount:<br>
* Setup enviorment variables as follow
```
#export JAVA_HOME=/usr/java/<java files>
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export PATH=${JAVA_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
export HADOOP_HOME=$HOME/hadoop
export PATH=${HADOOP_HOME}:${PATH}
```
_Instruction on installing hadoop and java in this post: xxx_<br>
* Compile WordCount.java and create a jar:
```
cd wordcount
bin/hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
```
If you have PATH issues, like I do :), use:<br>
`${HADOOP_HOME}/bin/hadoop` instead of `bin/hadoop`<br>

* Using WordCount class:<br>
WordCount class will scan all the files in directory input, count the words, and output a result file into output directory.
You can use hadoop to list and view your files:
```
$ bin/hadoop fs -ls input/
-rw-rw-r--   1 naomi_fridman naomi_fridman         21 2018-05-08 11:35 input/filfe1.txt
-rw-rw-r--   1 naomi_fridman naomi_fridman         22 2018-05-08 11:36 input/filfe2.txt
$ bin/hadoop fs -cat input/filfe1.txt
Hello from file1.txt
$ bin/hadoop fs -cat input/filfe2.txt 
Hello from file2.txt
```
Run the application:
```
bin/hadoop jar wc.jar WordCount input/ output_new
```
Application creates new output directory, if it allready exists, an error will be issued.<br>
View output:
```
bin/hadoop fs -cat output_new/part-r-00000
```
Will output the following:
```
Hello   2
file1.txt       1
file2.txt       1
from    2
```
You can run WordCount on archive files, jars etc. All info in the tutorial.

## Step 4. Hadoop MapReduce Top N Word Count 
Running WordCount on the output text files of the Python script, will create files containing list of words and their frequencies, number of occurrence in the Tweets.<br>
It's probably possible to perform top n search with word count in one map reduce operation but it requires to limit to one reducer, which effect the performance. <br>
I chose to run another Top n hadoop map reduce on the output of word count.<br>
**Top n map reduce**<br>
The keys generated by the mapper are automatically sorted by MapReduce Framework, i.e. Before starting of reducer, all intermediate key-value pairs in MapReduce that are generated by mapper get sorted by key and not by value. So, To find the top n frequent words, all we need to to is alter WordCount:
* Add comperator functionality.
* Limit to 1 reducer.
* In the reducer clean up, keep just the top n words.
Java file for Top N words is: `TopNwords.java`, to compile do:
```
bin/hadoop com.sun.tools.javac.Main TopNwords.java 
jar cf tnw.jar TopNwords*.class
```
Store word count out put from the previous stage in word_count and run:
```
bin/hadoop jar tnw.jar TopNwords word_count top_10words
```
You will get a result file of the form:
```
fintech 250
Sector  181
Healthcare      48
EnterRecruit    32
...
```
Another option is to put the 2 mapreduce operation in one driver class, as in this repository: `https://coe4bd.github.io/HadoopHowTo/multipleJobsSingle/multipleJobsSingle.html`<br>
But that requiers handling temporary files, of the word count and taking care that jobs will run in the right order.
## Step 5. Put it all Together
For full process, we need to run:
```
python collect_tweets_to_file.py NY "New York" Newyork NewYork
# (136, ' Words collected and saved in ', 'NY/tweets_from_NY.txt')
bin/hadoop jar wc.jar WordCount NY word_count
bin/hadoop jar tnw.jar TopNwords word_count top_10words
```
output:
```
set     27
data    15
big     12
sector  5
digital 5
`````
When I  finish the script, I'll post it here. :)


## Step 6. Adding Google cloud storage

General app 

There are two option to use Cloud storage, Cloud Dataflow and Cloud Dataproc.I must confess I did not fully understand the exact difference between the App's DataProc and DataFlow. I used DataProc details on what best for you, in here: <br> 
Reference: https://cloud.google.com/dataproc/<br>
After creating storage as explained before XXX, lets add the needed functionality to the Python and Java, to use Google cloud storage.<br>
### 6.1 Setup
* intall Google Cloud SDK , if you haven't already
```
curl https://sdk.cloud.google.com | bash
```
* Authenticate: `
```
gcloud auth application-default login
```
* Create Storage, from GCP menu, or directly from SSSH.
```
gsutil mb gs://[YOUR-BUCKET-NAME]
# Make the bucket publicly readable so it can serve file:
gsutil defacl set public-read gs://[YOUR_BUCKET_NAME]
```
https://cloud.google.com/sdk/downloads
https://cloud.google.com/java/

### 6.2 Adding Cloud Stotage to Java 

I must confess I did not fully understand the difference between the apps DataProc DataFlow, I used DataProc.<br>
I used BigTable cluster, which is a sort of data base, which you accses with HBase Api.

Reference: https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/tree/master/java/dataproc-wordcount/src/main/java/com/example/bigtable/sample<br>
Upload retrive data from java
https://github.com/GoogleCloudPlatform/google-cloud-java/tree/master/google-cloud-storage

Add the following imports at the top of your file:
```
import static java.nio.charset.StandardCharsets.UTF_8;

import com.google.cloud.storage.Blob;
import com.google.cloud.storage.Bucket;
import com.google.cloud.storage.BucketInfo;
```
Creating an authorized service object
To make authenticated requests to Google Cloud Storage, you must create a service object with credentials. You can then make API calls by calling methods on the Storage service object. The simplest way to authenticate is to use Application Default Credentials. These credentials are automatically inferred from your environment, so you only need the following code to create your service object:
```
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;

Storage storage = StorageOptions.getDefaultInstance().getService();
```
### 6.3 Add Google Cloud storage Python

https://cloud.google.com/bigtable/docs/samples-python-hello-happybase<br>
**SetUP**<br>
create requirements.txt file, which contain the following line:
```
google-cloud-happybase==0.26.0
```
Now run:
```
pip install -r requirements.txt
```
Now all needed Python libraries, should be installed.
To check, run:
```
$ pip freeze | grep google
```
You should see something like:
```
google-api-core==0.1.4
google-auth==1.4.1
google-cloud-bigtable==0.26.0
google-cloud-core==0.28.1
google-cloud-happybase==0.26.0
google-cloud-storage==1.10.0
google-cloud-vision==0.29.0
google-compute-engine==2.7.5
google-gax==0.15.16
google-resumable-media==0.3.1
googleapis-common-protos==1.5.3
```

The following modules can now be imported.
```
from google.cloud import bigtable
from google.cloud import happybase
```
Connect to the Cloud Bigtable by passing a bigtable.Client to a happybase.Connection.
```
# The client must be created with admin=True because it will create a
# table.
client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
connection = happybase.Connection(instance=instance)
```
Creating a table and its column families.
```
bigtable/hello_happybase/main.py VIEW ON GITHUB
print('Creating the {} table.'.format(table_name))
column_family_name = 'cf1'
connection.create_table(
    table_name,
    {
        column_family_name: dict()  # Use default options.
    })
```
The Python client for Cloud Bigtable provides two APIs for Cloud Bigtable:

A native API that provides an idiomatic interface for using Cloud Bigtable.
A HappyBase-compatible API. (HappyBase is a Python client library for HBase, an open-source product that is similar to Cloud Bigtable.) Use the HappyBase-compatible API if you need to move an existing HBase workload to Cloud Bigtable.
The Python client uses gRPC to communicate with the production servers. The Python client supports Python 2.7 and Python 3.<br>

To use the Python native API client for Cloud Bigtable, install: 

```
pip install google-cloud
```
To use the Python HappyBase-compatible API client for Cloud Bigtable, install:
```
pip install google-cloud-happybase
```
```
pip install google-cloud-dataproc
```
**Its recomended to work in your defined virtualenv**<br>
Install this library in a virtualenv using pip. virtualenv is a tool to create isolated Python environments. The basic problem it addresses is one of dependencies and versions, and indirectly permissions.<br>

With virtualenv, it’s possible to install this library without needing system install permissions, and without clashing with the installed system dependencies.
```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
```
Unlike HappyBase, `google-cloud-happybase uses google-cloud-bigtable` under the covers, rather than Apache HBase.<br>
To use the API, the Client class defines a high-level interface which handles authorization and creating other objects:
```
from google.cloud.bigtable.client import Client
client = Client()
```
**Authentication:** For an overview of authentication in google-cloud-python, see:<br>
`https://google-cloud-python.readthedocs.io/en/latest/core/auth.html`<br>
**Project IDL** you can set the GOOGLE_CLOUD_PROJECT environment variable for the Google Cloud Console project. Then client:<br>
```
>>> from google.cloud import bigtable
>>> client = bigtable.Client()
```
Or pass in, credentials and project explicitly:
```
>>> from google.cloud import bigtable
>>> client = bigtable.Client(project='my-project', credentials=creds)
```
The simplest way to use credentials from a user account is via Application Default Credentials using gcloud auth login (as mentioned above) and google.auth.default():
```
import google.auth

credentials, project = google.auth.default()
```
If you’ll be using your client to make Instance Admin and Table Admin API requests, you’ll need to pass the admin argument:
```
client = bigtable.Client(admin=True)
```
In the hierarchy of API concepts

* a Client owns an Instance
* an Instance owns a Table
* a Table owns a ColumnFamily
* a Table owns a Row (and all the cells in the row)<br>
You can also use Client.instance() to create a local wrapper for instances that have already been created with the API, or through the web console:
```
instance = client.instance(existing_instance_id)
instance.reload()
```
After creating the table object, make a CreateTable API request: 
```
table.create()
```
To create a ColumnFamily object:
```
column_family = table.column_family(column_family_id)
```
After creating column family object, make a CreateColumnFamily API request:
```
column_family.create()
```
Unlike the previous string values we’ve used before, the row key must be bytes.
```
row = table.row(row_key)
```
To create an AppendRow
```
append_row = table.row(row_key, append=True)
```
Note: The Python client library for Cloud Bigtable is not compatible with App Engine's standard hosting environment. If you are using App Engine, you can deploy your application to App Engine's flexible environment.
Before using the Python client library for Cloud Bigtable, refer to the Python Development Environment Setup Guide to install the latest version of Python 2 and 3, pip, virtualenv, and other useful packages and tools.

To use the Python native API client for Cloud Bigtable, install the google-cloud library using the pip tool:

The Python client for Cloud Bigtable provides two APIs for Cloud Bigtable:

A native API that provides an idiomatic interface for using Cloud Bigtable.
A HappyBase-compatible API. (HappyBase is a Python client library for HBase, an open-source product that is similar to Cloud Bigtable.) Use the HappyBase-compatible API if you need to move an existing HBase workload to Cloud Bigtable.


Upload data to storage from Python script
```
import os

    import google.cloud.storage

    # Create a storage client.
    storage_client = google.cloud.storage.Client()

    # TODO (Developer): Replace this with your Cloud Storage bucket name.
    bucket_name = 'Name of a bucket, for example my-bucket'
    bucket = storage_client.get_bucket(bucket_name)

    # TODO (Developer): Replace this with the name of the local file to upload.
    source_file_name = 'Local file to upload, for example ./file.txt'
    blob = bucket.blob(os.path.basename(source_file_name))

    # Upload the local file to Cloud Storage.
    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        bucket))
```
Clean UP
This is a learning project, so I deleted all from GCP menu.

Thanks Google for the 300% to use on the Cloud.Apriciation feedback:<br>
The documantation is clearbut hard to find what yoy need. 
It was great if Google can publish few posts with full examples of basic tasks as, running machine learning model on some data , or data mining and processing project. <br>
Google support where very kind and helpful. But, as many customer support, emails are very long. tedious mission for non native English speaker.More code Less words, please.<br> ```
http://kamalnandan.com/hadoop/how-to-find-top-n-values-using-map-reduce/
http://santoshsorab.blogspot.co.il/2014/12/hadoop-java-map-reduce
### Python BigTable Google Cloud Example 


**Example repository:**
* https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/bigtable/hello<br>-sort-by-value.html

http://happybase.readthedocs.io/en/latest/user.html<br>

https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/read-write-to-cloud-storage<br>
https://cloud.google.com/bigtable/docs/python/<br>
** Best source for python **
https://cloud.google.com/bigtable/docs/samples-python-hello-happybase
