#!/bin/bash
#    Copyright 2015 Google, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

PHASE=""
DEFAULT_ZONE="us-east1-c"
DEFAULT_CLUSTER='naomi-topnwords'


function print_usage() {
  echo 'Usage: $0 [create <bucket> [<clusterName> [zone]] | delete [<clusterName>] | start  <clusterName> <jar> [many options] ]'
  echo ""
  echo "create - builds a 4 core cluster on 2 machines with a 2 core controller"
  echo "will also download 5 files to /tmp and copy them up to your bucket."
  echo ""
  echo "delete - will stop and delete your cluster"
  echo ""
  echo "start - will submit a new job against an existing cluster"
  echo ""
}

if [ $# = 0 ]; then
  print_usage
  exit
fi

COMMAND=$1
case $COMMAND in
  # usage flags
  --help|-help|-h)
    print_usage
    exit
    ;;

# create DataProc cluster
# edit the definitions below to be compatible
# with the BigData instance you created
create)   # create <bucket> [<clusterName> [zone]]

  if (( $# < 2 )); then
    print_usage
    exit
  fi
  ZONE=${4:-$DEFAULT_ZONE}
  CLUSTER="${3:-$DEFAULT_CLUSTER}"

  gcloud dataproc clusters create "${CLUSTER}" \
    --bucket "$2" \
    --num-workers 2 \
    --zone $ZONE \
    --master-machine-type n1-standard-2 \
    --worker-machine-type n1-standard-2
  ;;

delete)  # delete [<clusterName>]

  CLUSTER="${2:-$DEFAULT_CLUSTER}"
  gcloud -q dataproc clusters delete "$CLUSTER"
  ;;

# run mapreducw word count
# i commented most of the books to make it faster
start)  # start [<clusterName>]

  CLUSTER="${2:-$DEFAULT_CLUSTER}"

  TARGET="WordCount-$(date +%s)"
  gcloud dataproc jobs submit hadoop --cluster "$CLUSTER" \
    --jar target/wordcount-mapreduce-0-SNAPSHOT-jar-with-dependencies.jar \
    -- wordcount-hbase \
    gs://lesv-big-public-data/books/book \
#    gs://lesv-big-public-data/books/b10 \
#    gs://lesv-big-public-data/books/b100 \
#    gs://lesv-big-public-data/books/b1232 \
    gs://lesv-big-public-data/books/b6130 \
    "${TARGET}"
    echo "Output table is: ${TARGET}"
  ;;

delete)  # delete [<clusterName>]

  CLUSTER="${2:-$DEFAULT_CLUSTER}"
  gcloud -q dataproc clusters delete "$CLUSTER"
   ;;

esac