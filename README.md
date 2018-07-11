# Python and Java Project on Google Cloud with BigTable and DataProc
As a data scientists, in constant need of computation resources, I started my tour in Google cloud with fun application that mine Twitter and run Java MapReduce on the retrived data. <br>
## Google_Cloud_setup.md
Complete Begginer guide to set up a Java Python project on Google Cloud Platform, with creation of all needed resources.
Steps are:
* Create Google Cloud account (choose "Individual"), enable billing and Google Cloud APIs
* Select or create a GCP project.
* Enable Google Cloud APIs in GCP->API & Services->Dushboard<br>, or choose enable all APi's in VM creation.
* Create BigTable cluster, this is your data cluster.
* initilize project parameters with: `gcloud init`
* Install Java, Haddop, Maven
* Install Python, and Python clients for Google Cloud storage.
## MapReduce_Hadoop_BigTable_DataProc
We start with running the famous  MapReduce WordCount BigTable DataProc example:<br>
https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/tree/master/java/dataproc-wordcount<br>
Since I found deploying and running this example, take longer then expected, I forked the example to my git, made some small modifications. At first step, I run mapreduce wordcount on public files stored on GC storage.<br>
Next step, is runing a Python script to mine Tweets about certain subject, and filter them by location, The tweet words, saved in txt file, which uploaded to Google Cloud storage.<br>
In the last step, a Python utility is used to read the HBase table created by wordcount mapreduce, and find the hioghest requency words in the table<br>
## Python_BigTable_utils
Set of simple Python utilities to access and manage **HBase** table data with **Happybase** Python client. Utilities are:
* **delete_hbase_table_from_bigtable.py** - connect to Cloud Bigtable, and delete a table.
* **hbase_table_head.py** - connect to Cloud Bigtable, and print few first rows.
* **python hbase_table_topn_by_value.py** - get the words with highest frequency
* **list_tables_in_BigTable.py** - connect to Bigtable cluster and list the table names in it.
* **words_from_BigTable_tables_to_output.py** - print out n=100 rows from a BigTable table
* **words_to_hbase_table_in_BigTable.py** - connect to Cloud Bigtable create table and insert words in it

## mine_tweets
In this directory, I mine tweets about a subject, and compare most frequent words in different locations. I Collect the words people Tweet, on a given query, filtered by location, tokenize and strip the text, count words and find highest frequency ones. <br>
There are python jupyter notobook, and python script, to play with Twitter mining options.

## assets
Images etc. needed in md files



