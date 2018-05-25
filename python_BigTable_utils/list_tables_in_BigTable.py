#!/usr/bin/env python
#
# Code is a modification of this example:
#  https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/bigtable/hello_happybase
#    
# Demonstrates how to connect to Cloud Bigtable and list the table names in it.
#
# usage: list_tables_in_BigTable.py [-h] project_id instance_id

import argparse

from google.cloud import bigtable
from google.cloud import happybase


def main(project_id, instance_id):
    # [START connecting_to_bigtable]
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    connection = happybase.Connection(instance=instance)
	# [END connecting_to_bigtable]
	
    table_list = connection.tables()
    print('Listing tables in Bigtable clister: ', instance_id)
    for table in table_list:
        print(table)
    
    connection.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument(
        'instance_id', help='ID of the Cloud Bigtable instance to connect to.')

    args = parser.parse_args()
    main(args.project_id, args.instance_id)
