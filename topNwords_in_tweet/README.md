# Hadoop MapReduce Word Count on Tweeter text 
### Python BigTable Google Cloud Example 


**Example repository:**
* https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/bigtable/hello

## Before you begin
You need to create Google Cloud project with billing, storage and credentials. Follow the this post:xxx or use the following link:

https://cloud.google.com/bigtable/docs/quickstart-hbase#before_you_start
Roughtly steps are:
* create project, enable billing, enable app's
* Create BigTable Cluster, add storage and credentials
* Create connect and open in browser, VM instance.
* Initialize Google cloud
If you followed the previous post xxx you can continue from here, in the same 

## Step 1. Install Python on Google cloud VM instance
Reference: https://cloud.google.com/python/<br>
In your vm instance, after initializing and authenticating Google cloud, do:
```
cd
sudo apt update
sudo apt install python python-dev python3 python3-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
# check
pip --version
```
you should sea something like this:
```
pip 10.0.1 from /usr/local/lib/python2.7/dist-packages/pip (python 2.7)
```
You can install virtual environment, as specified bellow, or install as superuser with sudo. This is just an example, so I chose to work as super user.<br>
Install virtual environment 
```
sudo pip install --upgrade virtualenv
virtualenv env
source env/bin/activate
#deactivate env
```
Install Python libraries for Google cloud storage
```
sudo pip install google-cloud-storage
```

## Step 3.  Python Tweeter text  retrieval
For the sake of this example, I wrote simple python file to retrieve tweets that are about BigData, and where tweeted in user selected location.<br>
To run the example, you will need to install the following Python libraries. You can install them from the Google cloude given bandle:<br>
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

http://kamalnandan.com/hadoop/how-to-find-top-n-values-using-map-reduce/
http://santoshsorab.blogspot.co.il/2014/12/hadoop-java-map-reduce-sort-by-value.html