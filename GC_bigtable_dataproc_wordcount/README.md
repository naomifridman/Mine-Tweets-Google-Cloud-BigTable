# How I managed to run MapReduce Google Cloude Java Example 

As a data scientists, in constant need of computation resources, I started my tour in Google cloud, with the known MapReduce WordCount BigTable DataProc example. I found deploying and running this example, took longer then expected, So I thought that writing short guides to each step will be practical. First step is setting up the project in Google Cloud Platform, and opening VM instance.
Example repository:https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/tree/master/java/dataproc-wordcount

## Step 1. Before you begin
Create and configure you GCP account and resources. In the following link have detailed walk through guide to set up project in Google Cloud Platform, GCP:
https://github.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud/blob/master/GC_bigtable_sexample_guide.md

Rougthly steps are:
* Create Google Cloud account, enable billing and Google Cloud APIs
Pay attention: choose "Individual" in account type.*<br>
* Select or create a GCP project.
* Enable the Google Cloud APIs in GCP->API & Services->Dushboard<br>
Make sure your project is selected<br>
For this MapReduce example, you need to Enable:
* Compute Engine API
* Cloud Bigtable API
* Cloud Bigtable Table Admin API
* Google Cloud Dataproc API
Save project parameters:<br>
* Zone: us-east1-c
* Project id: naomi-topnwords
* Instance id: naomi-mapreduce-bigtable
## Credentials
When working in VM opened in browser from GCP, credentials and authentication are done under the cover.
  
## Step 2. Install Java
In your VM SSH, do the following:
```
sudo apt-get update
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
sudo apt-get update
sudo apt-get install oracle-java8-set-default
 ```
To check installation:
```
java -version
```
Check environment variable path:
```
echo $JAVA_HOME 
```
If its not set, check that java is in /usr/lib/jvm/java-8-oracle and:
```
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
sudo apt-get update -y
```
## Step 3. Create Project storage
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

## Step 4. Install Maven and Hadoop
Install Apache Maven, Project managment tool
```
sudo apt-get install maven
```
Install hadoop
```
cd
wget www-eu.apache.org/dist/hadoop/common/hadoop-3.1.0/hadoop-3.1.0.tar.gz
tar xzf hadoop-3.1.0.tar.gz
```
Now you have hadoop-3.1.0 directory in your home. hadoop-3.1.0/bin/hadoop is the binary. Add it to path.
```
cd
mv hadoop-3.1.0 hadoop
export PATH="$PATH:$HOME/hadoop/bin"
```
## Step 5. Clone and Configure MapRduce example.
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
## Step 6. Deploy MapReduce Example
#### Create Google Cloud DataProc cluster
This cluster, is the one asctually runing the jobs. We need to create DataProc cluster, with same features as the BigTable cluster, otherwise the job will fail.<br>
You can create the DataProc xluster in few ways:
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
Minimum workers for mapreduce are 2.
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

## Step 7. Run MapReduce word count BigTable DataProc example
As before, we can run the actual job, from `cluster.sh' or manually from command line:
```
#./cluster.sh start  <your BigTable instance> 
./cluster.sh start  naomi-mapreduce-bigtable 
```
Or run Manually:
```
gcloud dataproc jobs submit hadoop --cluster naomi-mapreduce-bigtable \
    --jar target/wordcount-mapreduce-0-SNAPSHOT-jar-with-dependencies.jar \
    -- wordcount-hbase \
    gs://lesv-big-public-data/books/book \
    gs://lesv-big-public-data/books/b6130 \
    "words-count"
```
Where, gs://name are list of input public files, wordcount-hbase is the main class and last parameter is the output HBase table.
On succsefull run, you should see somthing like:
```
- name: word count
  progress: 1.0
  state: FINISHED
  trackingUrl: http://naomi-mapreduce-bigtable-m:8088/proxy/application_1525724630856_0001/
Output table is: words-count
```
## Step 8. view the results
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
scan
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
 !),                          column=cf:count, timestamp=1525727576042, value=\x00\x00\x00\x01                    
 !=                           column=cf:count, timestamp=1525727564454, value=\x00\x00\x00\x09                    
 !=),                         column=cf:count, timestamp=1525727564580, value=\x00\x00\x00\x01                    
 !=,                          column=cf:count, timestamp=1525727576623, value=\x00\x00\x00\x01                    
 !probationary</pre></div></t column=cf:count, timestamp=1525727567638, value=\x00\x00\x00\x01                    
 d>                                                                                                               
5 row(s) in 0.2130 seconds
```
The data is saves in bytes, 
Exit the HBase shell:
```
exit
```
### python tools
Use the python utils from this git. 
```
cd
cd Top-N-Words-In-Tweets-Google-Cloud/python_BigTable_utils/
python base_table_head.py --table "words-count" naomi-topnwords naomi-mapreduce-bigtable
```
Output, in bytes:
```
'!),', {'cf:count': '\x00\x00\x00\x01'})
('!=', {'cf:count': '\x00\x00\x00\t'})
('!=),', {'cf:count': '\x00\x00\x00\x01'})
('!=,', {'cf:count': '\x00\x00\x00\x01'})
('!probationary</pre></div></td>', {'cf:count': '\x00\x00\x00\x01'})
('"', {'cf:count': '\x00\x00\x00\xf4'})
('""', {'cf:count': '\x00\x00\x00\x01'})
('"%5$s"</code>}', {'cf:count': '\x00\x00\x00\x01'})
('"&#8230;&#8203;number', {'cf:count': '\x00\x00\x00\x01'})
('"&lt;html&gt;&#8230;&#8203;"</p></td>', {'cf:count': '\x00\x00\x00\x06'})
```
You can edit the python utilities, for scpecific column_family, to output int values and not bytes.


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
## Terminology and Initials
### Google Cloud BigTable and HBase.
HBase is a NoSQL database. It is based on Google’s Bigtable distributed storage system – as it is described in Google research paper; “A Bigtable is a sparse, distributed, persistent multi-dimensional sorted map. The map is indexed by a row key, column key, and a timestamp; each value in the map is an uninterpreted array of bytes.” 
* GCP - Google Cloud Platform
## Trouble Shooting
* You don't need to authenticate, but sometimes it solves issues, run:
```
gcloud auth application-default login
```




