# How I managed to run MapReduce Google Cloude Java Example 


**Example repository:**
* https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/tree/master/java/dataproc-wordcount

## Step1. Before you begin
Create and configure you GCP account and resources. In the following link have all information to do:

https://cloud.google.com/bigtable/docs/quickstart-hbase#before_you_start
#### Create Google Cloud account
Follow the link above, "before you start" to create Google cloud account.<br>
Accept term of service.<br>

#### Create Project enable billing and Google Cloud APIs
1. Select or create a GCP project.
Write down, Project name, Project id and Project number.
2. Enable billing for your project.<br>
GCP menu -> Billing<br>
**Pay attention: choose "Individual" in account type !**<br>
Insert you credit card, accept terms of service.<br>
**Prepaid credit cards are not acceptable**<br>
3. Enable the Google Cloud APIs needed for this example<br>
GCP menu->API & Services->Dushboard<br>
Make sure your project is selected<br>
You get a page with long list of applications. Chose the APIs needed for this Project, and enable the one by one.<br>
For this MapReduce example, you need to Enable:
* Compute Engine API
* Cloud BigTable API
* Cloud BigTable Table Admin API
* Google Cloud DataProc API
* Cloud BigTable Admin API

## Step 2. Create BigTable Cluster
**A Cloud BigTable instance is a container for up to two Cloud BigTable clusters.**<br>
GCP menu->BigTable->create instance
Reference: https://cloud.google.com/bigtable/docs/creating-instance
* Choose instance name: for example - naomi-mapreduce-bigtable
* Write down the Instance id: for example - naomi-mapreduce-bigtable
* In Instance type: Choose Development
* In Storage type: Choose SSD
* You get a Cluster creation Dialog, write down your the cluster info:
* 	Cluster ID: for example - naomi-mapreduce-bigtable-c1
* 	Zone: Choose and write down your choice.  Best is to use same zone for all the resources and actions in the project: us-west-1-c
* 	Select "Done" in Cluster dialog, and Create.

## Step 3. Create VM Instance
Here you create an instance, and from its SSH you will run the project.<br>
* GCP menu-> Computing engine->VM instance->create
* Choose name: vm-instance-1
* Choose zone same one as before: us-west1-c
* Choose Machine type: 2vCPUs, write down your choice.
* Choose boot disk: ubuntu 16.04, boot disk type SSD disk
* in Identity and API access: Allow full access to all Cloud APIs
* In Firewall: allow both access, HTTP and HTTPs

## Step 4. Credentials and IMA roles
Reference: https://cloud.google.com/iam/docs/quickstart
#### API Credentials ???? trying without it
GCP menu -> API & services -> Credentials -> Create credentials -> 
* In IMA page, make sure your project is selected
* Add yourself as member, Choose owner type.
* Choose edit in member menu, and get dialog to add roles. Add the following Roles: 
* * App Engine Admin
* * Project Billing Manager
* * BigTable Administrator
* * Compute Admin
* * DataProc Editor
* * Project Owner
* * Storage Admin
* * Logging Admin

## Step 5. Open VM Instance SSH
GCP menu -> Compute engine -> VM instance
From VM instance menu page, Choose SSH, under connect, and Choose "Open browser window".<br>
![Open VM Instance](https://raw.githubusercontent.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud/master/assets/vm_instance.PNG)<br>
From here on, by default, the instruction related to this SSH.

## Step 5. Initialize Google Cloud
In your VM instance do the following:
```
gcloud init 
```
You will be asked to confirm: account, project and choose default zone.<br>
If some needed application, wasn't enables, you will be asked to enable it now.
<br>

## Step 6. Install Java
In your VM SSH, do the following:
```
sudo apt-get update
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer  # pay attention and answer "yes" to service terms
sudo apt-get update
sudo apt-get install oracle-java8-set-default
 ```
check instalation:
```
java -version
```
You should see somthing like:
```
java version "1.8.0_171"
Java(TM) SE Runtime Environment (build 1.8.0_171-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.171-b11, mixed mode)
```
Check enviorment variable path
```
echo $JAVA_HOME 
```
If its not set, check that java is in /usr/lib/jvm/java-8-oracle and:
```
JAVA_HOME=/usr/lib/jvm/java-8-oracle
export JAVA_HOME
sudo apt-get update -y
```

## Step 7. Install Maven and Hadoop
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
Now you have hadoop-3.1.0 directory in your home. hadoop-3.1.0/bin/hadoop is the binary. <br>
Add Haddop and Java binaries to path.
```
cd
mv hadoop-3.1.0 hadoop
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export PATH=${JAVA_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
export HADOOP_HOME=$HOME/hadoop
export PATH=${HADOOP_HOME}:${PATH}
```
Steps 1 to 7, needed in any application using java and Hadoop. Fron now on, instructions are specific to this BigTable, DataProc example.<br>
## Step 8. Create Project storage
You need to create Buckets for data storage of the project.<br>
You can create them in GCP broweset menue:
* GCP -> Storage -> Browser
Or you can create them in your VM with Java cloude tool, gsutil:<br>
```
gsutil mb -p <project ID> gs://<bucketName>
# For example
gsutil mb -p naomi-mapreduce gs://naomi-bucket2
```
Make your Buckets pablic:
```
gsutil defacl set public-read gs://naomi-bucket1
gsutil defacl set public-read gs://naomi-bucket2
```
You can give any unique name to the Bucket. You need 2 buckets for this project.
## Step 9. Clone and Configure MapRduce example.

Clone the example:
```
git clone https://github.com/GoogleCloudPlatform/cloud-bigtable-examples.git
cd cloud-bigtable-examples/java/dataproc-wordcount/
#mvn clean package -Dbigtable.projectID=YOUR_PROJECT_ID -Dbigtable.instanceID=YOUR_INSTANCE_ID
mvn clean package -Dbigtable.projectID=naomi-mapreduce -Dbigtable.instanceID=naomi-mapreduce-bigtable 
```
You should see somthing likje this:
```
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 45.303 s
[INFO] Finished at: 2018-05-07T20:00:31+00:00
[INFO] Final Memory: 73M/753M
[INFO] ------------------------------------------------------------------------
```
## Step 10. Deploy MapReduce Example
Edit the following part of cluster.sh file to suit your number of workers and cpu's you choose when vreated the instance. 
```
gcloud dataproc clusters create "${CLUSTER}" \
    --bucket "$2" \
    --num-workers 4 \
    --zone $ZONE \
    --master-machine-type n1-standard-4 \
    --worker-machine-type n1-standard-4
```
In this post's example, we change 4 machine and 4 workers to 2, as we choose when created BigTable instance.<br>
On succesfull creation, you should see somthing like:
```
Waiting on operation [projects/[Project-Id]/regions/global/operations/b811e0c2-2f6b-420e-a4d5-bc846326f9c5].
Waiting for cluster creation operation...done.                                         
Created [https://dataproc.googleapis.com/v1/projects/naomi-mapreduce/regions/global/clusters/naomi-mapreduce-bigtable] Cluster placed in zone [us-central1-b]
```
Configure Hadoop for the project.
```
hadoop  jar hadoop-streaming.jar \
    -input input \
    -output output \
    -outputformat org.apache.hadoop.mapred.SequenceFileOutputFormat\
    -mapper MapperClass \
    -reducer ReducerClass
```
## Step 11. Run MapReduce and view Output
```
cd cloud-bigtable-examples/java/dataproc-wordcount/
#./cluster.sh start  <your BigTable instance> 
./cluster.sh start  naomi-mapreduce-bigtable 
```
On succsefull run, you should see somthing like:
```
- name: word count
  progress: 1.0
  state: FINISHED
  trackingUrl: http://naomi-mapreduce-bigtable-m:8088/proxy/application_1525724630856_0001/
Output table is: WordCount-1525727487
```
In GCP boser menue at: GCP > Dataproc > Jobs, you can see the log of the project's job.<br>
To View the results, you need to use  hbase shell. Information here:
https://cloud.google.com/bigtable/docs/quickstart-hbase <br>
```
cd $HOME/cloud-bigtable-examples/quickstart
./quickstart.sh
```

Few basic hbase shell comands:<br>
* `list` - List the tables
* `scan "table name"` - output the table content
* `describe "table name"` - output table description
* Type `exit` and press Enter to exit the HBase shell. You will see a series of log messages after you exit, which is normal.
* 'count "table name" - will give you somthing like:
```
Current count: 121000, row: vainest                                                                               
Current count: 122000, row: vitae,                                                                                
Current count: 123000, row: wearing.                                                                              
Current count: 124000, row: will'd)                                                                               
Current count: 125000, row: wound,)                                                                               
125778 row(s) in 0.9430 seconds

=> 125778
```
* `scan "table name" ,{RAW => true, LIMIT =>5}` will output 5 rows. In this project we got:
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


## Clean up
There is a cleaning script in the example:
```
#gcloud -q dataproc clusters delete <cluster id>
gcloud -q dataproc clusters delete naomi-mapreduce
```
I think its a good idea to delete everything from GCP browser menu.
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




