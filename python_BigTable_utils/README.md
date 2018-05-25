# Python Utils To Work with BigTable HBase tables

This branch, contains Python scripts with basic BigTable database tasks. The source is a simple general sketch of how to work with BigTable tables from Python script. There are utils for create table, write data into tables, read data from tables, list and delete tables. The README file, contains a complete bigginer guide for setup Google Cloud project, to run this example, and other python script using BigTable.<br>
Reference: http://happybase.readthedocs.io/en/latest/user.html

## Working with Google Cloud Data Base
There are 2 Google Cloud APIs for working with database: BigTable and BigQuery.<br>
BigQuery is a query Engine for datasets that don't change much, or change by appending. It's a great choice when your queries require a "table scan" or the need to look across the entire database. Think sums, averages, counts, groupings. BigQuery is what you use when you have collected a large amount of data, and need to ask questions about it.<br>

BigTable is a database. It is designed to be the foundation for a large, scaleable application. Use BigTable when you are making any kind of app that needs to read and write data, and scale is a potential issue.<br>
Explanation from: `https://stackoverflow.com/questions/39919815/whats-the-difference-between-bigquery-and-bigtable`<br>
In this example we use BigTable.
To access database from Java code, we use Hadoop HBase<br>
To access database from Python code, we use HappyBase which is a Python client library for HBase.

## Before you begin
You need to setup a Google Cloud project. You can follow the walk through guide here:<br>
https://github.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud/blob/master/GC_setup_guid.md<br>
Or you can use or use the following Google documentation:

`https://cloud.google.com/bigtable/docs/quickstart-hbase#before_you_start`<br>
Generally steps are:
* create project, enable billing, enable Google API's
* Create connect and open in browser, VM instance.
* Initialize Google cloud

## Step 1. Install Python on Google cloud VM instance
Reference: https://cloud.google.com/python/<br>
In your vm instance, after initializing Google cloud, do:
```
sudo apt update
sudo apt install python python-dev python3 python3-dev
sudo python get-pip.py
# check
pip --version
```
you should see something like this:
```
pip 10.0.1 from /usr/local/lib/python2.7/dist-packages/pip (python 2.7)
```
To work with python3 you need to install install pip3:
```
sudo apt-get update
sudo apt-get -y install python3-pip
# Then to verify installation try
pip3 --help 
#For checking version :
pip3 --version 
```
Install virtual environment 
```
sudo pip install --upgrade virtualenv
virtualenv env
source env/bin/activate
#deactivate env
```
You can also install needed packages as superuser with sudo. <br>
Install Python libraries for Google cloud storage


## Step 2. Add Google Cloud storage to Python

https://cloud.google.com/bigtable/docs/samples-python-hello-happybase<br>

install python packages needed for working with BigTable:
```
pip install google-cloud-storage
pip install google-cloud-happybase
pip install google-cloud-dataproc
```
Now all needed Python libraries, should be installed.<br>
To check, run:
```
$ pip freeze | grep google
```
You should see something like:
```
google-api-core==0.1.4
google-auth==1.4.1
google-cloud-bigtable==0.26.0
google-cloud-core==0.26.0
google-cloud-dataproc==0.1.0
google-cloud-happybase==0.26.0
google-cloud-storage==1.10.0
google-cloud-vision==0.29.0
google-gax==0.15.16
google-resumable-media==0.3.1
googleapis-common-protos==1.5.3
```
## Step 3. Connect to Google Cloud BigTable storage from Python
If all installations went successfully, The following modules can now be imported.
```
from google.cloud import bigtable
from google.cloud import happybase
```

In the hierarchy of API concepts

* a Client owns an Instance
* an Instance owns a Table
* a Table owns a ColumnFamily
* a Table owns a Row (and all the cells in the row)<br>
You can also use Client.instance(already_existing_instance_id) to create a local wrapper for instances that have already been created with the API, or through the web console.<br>
Connect to the Cloud Bigtable:
```
# The client must be created with admin=True for permitions to create Tables
client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
connection = happybase.Connection(instance=instance)
```
Creating a table and its column families:
```
column_family_name = 'cf1'
connection.create_table(
    table_name,
    {
        column_family_name: dict()  # Use default options.
    })
```

After creating the table object: 
```
table = connection.table(table_name)
```
## Utilities and Usage
clone the git and cd to folder:
```
git clone https://github.com/naomifridman/Top-N-Words-In-Tweets-Google-Cloud.git
cd Top-N-Words-In-Tweets-Google-Cloud/python_BigTable_utils
```
#### words_to_HBase_table_in_BigTable.py 
Python script that creates a BigTable table, and insert into the created table a list of words.<br>
`usage: words_to_HBase_table_in_BigTable.py [-h] [--table TABLE] project_id instance_id`<br>
Run:
```
python words_to_HBase_table_in_BigTable.py naomi-topnwords naomi-mapreduce-bigtable
```
You will get:
```
Creating the words_table_example table.
('Writing some words to table: ', 'words_table_example')
('column_name ', 'cf1:words')
('Writing  word to the table.', 0, 'IamWods1')
('Writing  word to the table.', 1, 'SheIsWord2')
('Writing  word to the table.', 2, 'HeIsWord3')
```
#### list_tables_in_BigTable.py
Python script that list all tables in given BigTable cluster<br>
`usage: list_tables_in_BigTable.py [-h] project_id instance_id`<br>
Run:
```
python words_to_HBase_table_in_BigTable.py --table Test3 naomi-topnwords naomi-mapreduce-bigtable
python list_tables_in_BigTable.py naomi-topnwords naomi-mapreduce-bigtable
```
You will get:
```
('Listing tables in Bigtable cluster: ', 'naomi-mapreduce-bigtable')
Test3
words_table_example
```
When words_table_example is the default table name for words_to_HBase_table_in_BigTable.py, when no name is given.
#### delete_HBase_table_from_BigTable.py
Delete a table from BigTable<br>
`usage: delete_HBase_table_from_BigTable.py [-h] [--table TABLE] project_id instance_id`<br>
Run:
```
python delete_HBase_table_from_BigTable.py --table Test3 naomi-topnwords naomi-mapreduce-bigtable
```
You will get:
```
Test3
words_table_example
Deleting the Test3 table.
('Listing tables in Bigtable cluster: ', 'naomi-mapreduce-bigtable', ' after deleting')
words_table_example
```
#### words_from_BigTable_tables_to_output.py
This python script scan a given table, and print them.<br>
'usage: words_from_BigTable_tables_to_output.py [-h] [--table TABLE] project_id instance_id`
Run:
```
python words_from_BigTable_tables_to_output.py --table words_table_example naomi-topnwords naomi-mapreduce-
bigtable
```
You will get:
```
('Scanning all words in table: ', 'words_table_example')
('column_name ', 'cf1:words')
        words0: IamWods1
        words1: SheIsWord2
        words2: HeIsWord3
Deleting the words_table_example table.
```


