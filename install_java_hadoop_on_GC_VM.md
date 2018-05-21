# Install Java and Hadoop on Google Cloud VM instance

I started my research on Google Cloud, with the example below. I must confess that it took me longer time then expected, and involved a lot of try and error. So I decided it will be a good idea to write short guides to each step. Here is complete total beginner guide for installing java and hadoop on Google Cloud VM instance. 

Example repository: https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/tree/master/java/dataproc-wordcount

## Before you begin
You need to setup a Google Cloud project. You can follow the walk through guide here:<br>
https://github.com/naomifridman/Top-N-Words-In-Tweets-GoogleCloud/blob/master/GoogleCloudSetUpForrunningBigTableDataProcExamples.md<br>
Or you can use the following Google documentation:

https://cloud.google.com/bigtable/docs/quickstart-hbase#before_you_start<br>
Generally steps are:
* create project, enable billing, enable Google API's
* Create BigTable Cluster.
* Create connect and open in browser, Google Cloud VM instance.


## Step 1. Install Java
In your VM SSH, do the following:
```
sudo apt-get update
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
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
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
sudo apt-get update -y
```
## Step 2. Install Maven and Hadoop
Install Apache Maven, Project management tool
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
mv mv hadoop-3.1.0 hadoop

```

Setup enviorment variables as follow
```
#export JAVA_HOME=/usr/java/<java files>
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export PATH=${JAVA_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
export HADOOP_HOME=$HOME/hadoop
export PATH=${HADOOP_HOME}:${PATH}
export PATH="$PATH:$HOME/hadoop/bin"
sudo apt-get update -y
```

## Trouble Shooting
* In many cases, reopening the VM instance solve installation issues.<br>
* In hard cases, delete the VM instance from the GCP menue, and 
* For hadoop issues, try set or correct hadoop environment variables.
```
HADOOP_HOME=$HOME/hadoop
export HADOOP_HOME
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/native"

```






