# Mine Tweet's with Python, MongoDB and Docker on Google cloud Kubernete
## Python and MongoDB
MongoDB is great non-SQL database service. Essay to connect with python from any machine or cloud. Practical and essay to use pymongo library help fast development. The small free account of https://mlab.com is great to learn how to use MongoDB. The web interface to your database is practical and useful.
The only disadvantage, is the fast change rate, so most documentation online, has wrong format.
### Create MongoDB account and database
MongoDB is a scalable, high-performance, open source, document-oriented NoSQL database. It supports a large number of languages and application development platforms.
There are few options to MongoDB, I chose mLab, mainly bacause I liked the documentation.
Create an account here:
https://mlab.com/
Choose free account to start with, and you will get:
* Sandbox
> Our free Sandbox plan provides a single database with 0.5 GB of storage on a shared database server process running on a shared virtual machine (VM). This plan is best for development and prototyping.

### Connect to MongoDB data base
After your new deployment is created, choose it in the mLab web page, and you will get the connection information.  To connect you need:
* Database: db_name
* host, port
* dbuser, dbpassword
Pay attention, for dbuser and dbpassword , you need to create a user in the database.
Install pymongo python library.  On anaconda, I used:
```
conda install -c anaconda pymongo 
```
To connect using the mongoDB shell:
`mongo host:port/db_name -u <dbuser> -p <dbpassword>`
To connect from python script, using pymongo, use:
```
	connection = pymongo.MongoClient(host, port)
    db = connection[dbname]
    db.authenticate(dbuser, dbpassword)a d
   ```


### Python scripts to mine and save Tweeets in MongoDB
The idea is to run the python code, listening to twitter stream from few dockers, each for different location.
#### Step 1. Initialize
Create mongoDB collection with the locations definition. Each app/python code, will take a location from this joined table, and mark is as taken. The words we will track in the Tweeter stream, are saved to MongoDB as well.
This step run only once, prior to ruining the python code.
```
 $ python pymongo_initialize_mongodb.py
 ```
#### Step 2.  Listen to Tweeter stream and save words in MongoDB
Connect to your database in Mongodb, choose location from locations table, mark it as taken, read the words to track from db. Listen to a Tweeter stream according filtered by location and track words. Tokenize and clean any relevant Tweet, and insert to tables in Mongodb.
This python code will be implemented in Docker image.
```
pymongo_collect_tweets.py
```
#### Ste 3. Read and show results from MongoDB
Connect to your MongoDB database and print out the most popular words in tweets, in general and by location.
```
 pymongo_collect_tweets.py
 ```
#### Python utils for MongoDB 
Delete all collections from data base. use:
```
 $ python pymongo_clean_mongodb.py
 ```
 If you need to restart a dead process, you can reset the locations table:
 ```
  $ python pymongo_reset_taken_locations.py
  ```

## Dockers
Create Docker file and Package python code for ruining on docker. Intstructions here are short modified version of the tutorial:
* https://docs.docker.com/get-started/
* https://docs.docker.com/get-started/part2/

#### Step 1. Install Docker
When you run from Google Kubernete engine, Docker is already install. If you want to run dockers from your local machine, you need to install Docker 1.13 or higher.  Download from:
* https://docs.docker.com/engine/installation/
##### On local machine
* start docker deamon
1.  Run  `docker --version`  and ensure that you have a supported version of Docker
2.  Run  `docker info`  or (`docker version`  without  `--`) to view even more details about your docker installation:
3.  Give your environment a quick test run to make sure you’re all set up:
```
docker run hello-world
```
Expected output:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```
#### Step 2. Define a container with  `Dockerfile`
`Dockerfile` defines what goes on in the environment inside your container.
Access to resources like networking interfaces and disk drives is virtualized inside this environment, which is isolated from the rest of your system. With all the resources defined in Dockerfile, you can expect that the build of your app defined in this `Dockerfile` behaves exactly the same wherever it runs.

Create a file called  `Dockerfile`,with the following content. Take note of the comments that explain each statement in your new Dockerfile.

```
# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
# Temporary directory is created, so any name works.
WORKDIR /app

# Copy the current directory contents into the container at /app
# So keep only needed files in this directory
ADD . /app

# Install any needed packages specified in requirements.txt
# List all needed python packages in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run pymongo_collect_tweets.py when the container launches
CMD ["python", "pymongo_collect_tweets.py"]
```

#### Step 3. Build docker image
We are ready to build the app. Its not really an app, but docker has a structure suitable for app.  cd to the directory where you have:
```
Dockerfile	pymongo_collect_tweets.py			requirements.txt
```
Now run the build command. This creates a Docker image, which we’re going to tag using  `-t`  so it has a friendly name.
```
docker build -t pymongotweet  .
```
Where is your built image? It’s in your machine’s local Docker image registry:
```
$ docker image ls

REPOSITORY            TAG                 IMAGE ID
pymongotweet		latest              c64a865902a8
```
#### Step 4. Run the Python script

Run the app, mapping your machine’s port 4000 to the container’s published port 80 using  `-p`.  to run the app in the background, in detached mode use-d :
```
docker run -d -p 4000:80 pymongotweet
```
To see the abbreviated container ID with  `use:
```
$ docker container ls
CONTAINER ID   IMAGE         COMMAND               ...
1fa4ab2cf395  pymongotweet  "python pymongo_coll…" ...
```
Stop the container using  `CONTAINER ID`, like so:
```
docker container stop 1fa4ab2cf395
```
> Don't forget to clean and initialize MongoDB with python scripts `pymongo_initialize_mongodb.py` and `pymongo_clean_mongodb.py`
> To see the mined words, use ` pymongo_show_results.py`

#### Step 5. Share your image

Upload the built image into a repository, to make it available to run anywhere. 
A registry is a collection of repositories, and a repository is a collection of images—sort of like a GitHub repository, except the code is already built. 
> **Note**: We use Docker’s public registry here just because it’s free and pre-configured, but there are many public ones to choose from, and you can even set up your own private registry using  [Docker Trusted Registry](https://docs.docker.com/datacenter/dtr/2.2/guides/).
##### Log in with your Docker ID

If you don’t have a Docker account, sign up for one at  [hub.docker.com](https://hub.docker.com/). Make note of your username.

Log in to the Docker public registry on your local machine.

```
$ docker login
```
##### Tag the image

A repository on a registry is  `username/repository:tag`. The tag is optional, but recommended, since it use to give Docker images a version.  Run  `docker tag image`  :
```
docker tag image username/repository:tag
```
For example:
```
docker tag pymongotweet naomifridman/pymongo:v1
```
##### Publish the image

Upload your tagged image to the public repository:
```
docker push naomifridman/pymongo:v1
```
Once complete, the results of this upload are publicly available. If you log in to  [Docker Hub](https://hub.docker.com/), you see the new image there, with its pull command.

##### Pull and run the image from the public remote repository

From now on, you can run your app on any machine using:
```
docker run -p 4000:80 naomifridman/pymongo:v1
```
If the image isn’t available locally on the machine, Docker pulls it from the repository.
### Running the container in a service
To scale our application and enable load-balancing, we must go  up in the hierarchy of a distributed application: the **service**.
Services are really just “containers in production.” A service only runs one image, but it codifies the way that image runs—what ports it should use, how many replicas of the container should run so the service has the capacity it needs, and so on. Scaling a service changes the number of container instances running that piece of software, assigning more computing resources to the service in the process. We can scale up on local machine, and use swarm to run few dockers simultaneously. 
We will scale up on Google cloud Keberenete engine.

## Run container on Google Kubrnete Engine
Visit the  [Kubernetes GitHub repository](https://github.com/kubernetes/kubernetes/tree/release-1.10/examples/guestbook)  to download the example used in this tutorial:
https://cloud.google.com/kubernetes-engine/docs/tutorials/guestbook

First setup Google cloud account, create project, then open VM instance.
Google cloud platform: https://cloud.google.com
Go to Google cloud platform:
* Select Compute > Compute Engine > VM Instances.
To the right of the instance, select Open in browser.
* To save time typing time, set the defaults:
```
gcloud config set project PROJECT_ID
gcloud config set compute/zone us-east1-b
```
Create the kubernete cluster, and check it:
```
gcloud container clusters create mycluster --num-nodes=4
gcloud container clusters list
gcloud container clusters describe mycluster
```
>  If you are using an existing Kubernetes Engine cluster or if you have created a cluster through Google Cloud Platform Console, you need to run the following command to retrieve cluster credentials.
```
gcloud container clusters get-credentials mycluster
```
`kubectl`  is used to manage Kubernetes, the cluster orchestration system used by Kubernetes Engine. You can install  `kubectl`  using  `gcloud`:
 ```  
 gcloud components install kubectl
```   
We will use 4 masters and no slave, so its enought to create the following  configuration yml file :
``` 
kind: ReplicationController
metadata:
  name: pymongo-master
  # these labels can be applied automatically 
  # from the labels in the pod template if not set
  labels:
    app: pymongo
    role: master
    tier: backend
spec:
  replicas: 5
  template:
    metadata:
      labels:
        app: pymongo
        role: master
        tier: backend
    spec:
      containers:
      - name: master
        image: naomifridman/pymongo:v1
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        ports:
        - containerPort: 6379
```
Start up the pymongo master's Service by running:
```
$ kubectl create -f controller.yaml --validate=false
replicationcontroller "pymongo-master" created
```

To check services and pods, run:

```
kubectl get service
```
Output:
```
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes     ClusterIP   10.47.240.1     <none>        443/TCP    18h
redis-master   ClusterIP   10.47.244.146   <none>        6379/TCP   17h
```
Check that all 4 processes are working:
```
kubectl get pods
```
Output:
```
NAME                   READY     STATUS             RESTARTS   AGE
pymongo-master-5knt6   0/1       ImagePullBackOff   0          31m
pymongo-master-b8rmz   0/1       ImagePullBackOff   0          31m
pymongo-master-jg855   0/1       ImagePullBackOff   0          31m
pymongo-master-nqbjr   0/1       ImagePullBackOff   0          31m
pymongo-master-sbvdb   0/1       ImagePullBackOff   0          31m
```
Cleanup,
To delete services, use the following command:
```
kubectl delete service redis-master
```
**Delete the container cluster:**  This step will delete the resources that make up the container cluster, such as the compute instances, disks and network resources.
```
gcloud container clusters delete mycluster
```
### Tweeter mining results
Run pymongo_show_results.py and get output of the form:
```
******* Top words in:  London
president 33
donald 21
uk 20
administration 18
baby 18
******* Top words in:  Washington
donald 35
president 34
realdonaldtrump 32
administration 30
******** view top words over all location

president 180
know 114
donald 114
realdonaldtrump 104
mueller 102
```
