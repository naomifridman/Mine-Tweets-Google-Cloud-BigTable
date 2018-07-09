# Experimenting with Google Cloud, MongoDB and Dockers
Google gives 300$, so its a good opertunaty to experiment. In this toy project, I chose to explore Google cloud Platform (GCP) utilities to run an app that listen, analize and save texte. I used python script listening to Tweeter stream as testing app. The goal was to filter, tokenize and save tweets containing a kye word, and compare most popular words in different locations.
I tried 2 ways, one with BigTable, Hbase, DataProc, Python and Java. The second with MongoDB, Python and Docker.
## Project 1. Python and Java Project on Google Cloud with BigTable and DataProc
Here I wrote python script to retrive tweets, filter, tokenize words, and save them in BigTable data base. Then I run Hadoop Mapreduce, to count word frequencies. Mapreduce was not really needed here, it was written mainly for learning purposes.
## Project 2. Python, MongoDB and Docker.
Here I worte a python script to listen to Tweeter stream, filter , tokenize and save words to MongoDB collections.

