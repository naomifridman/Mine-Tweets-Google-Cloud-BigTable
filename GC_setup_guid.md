# Google Cloud SetUp For running BigTable DataProc WordCount MapReduce Examples on VM

I am a data scientist building and running deep learning models in Python. Although I have decent computer with NVIDIA Gpu's, Its not enough for training segmentation models as UNet's on large images. So I started explore cloud computation solutions, Mainly Amazon AWS and Google Cloud.<br>
I started my research on Google Cloud, with the example below. I must confess that it took me longer time then expected, and involved a lot of try and error. So I decided it will be a good idea to write short guides to each step. Here is complete total beginner guide to the first setup step of Google Cloud environment. <br>

Example repository:
`https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/tree/master/java/dataproc-wordcount`

## Step1. Before you begin
Create and configure you GCP account and resources. In the following link original example guide:<br>
working in VM instance is slightly different.

https://cloud.google.com/bigtable/docs/quickstart-hbase#before_you_start<br>
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

## Step 2. Create VM Instance
Here you create an instance, and from its SSH you will run the project.<br>
* GCP menu-> Computing engine->VM instance->create
* Choose name: vm-instance-1
* Choose zone same one as before: us-west1-c
* Choose Machine type: 2vCPUs, write down your choice.
* Choose boot disk: ubuntu 16.04, boot disk type SSD disk
* in Identity and API access: Allow full access to all Cloud APIs
* In Firewall: allow both access, HTTP and HTTPs

## Step 3. IMA roles
Reference: https://cloud.google.com/iam/docs/quickstart
 
* In IMA page, make sure your project is selected
* Add yourself as member, Choose owner type.
* Choose edit in member menu, and get dialog to add roles. Add the following Roles: 
* ##*App Engine Admin
* Project Billing Manager
* BigTable Administrator
* Compute Admin
* DataProc Editor
* Project Owner
* Storage Admin
* Logging Admin

## Step 4. Open VM Instance SSH
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

## Step 6. Credentials, Google SDK
When working on VM instance, opened from GCP, as we do in this example, authentication is done automatically. And Google SDK is already instaled.

## Step 7. Install Java
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
