#!/usr/bin/env python
#
# Code is small modification of this example:
#  https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/bigtable/hello_happybase
#    
# Demonstrates how to connect to Cloud Bigtable
# Create table
# insert list of words to the table
# Prerequisites:
#- Create a Cloud Bigtable cluster.
#  https://cloud.google.com/bigtable/docs/creating-cluster
#- Set your Google Application Default Credentials.
#  https://developers.google.com/identity/protocols/application-default-credentials
#
# usage: delete_HBase_table_from_BigTable.py [-h] [--table TABLE] project_id instance_id

import argparse

from google.cloud import bigtable
from google.cloud import happybase

def list_tables(connection):
    table_list = connection.tables()
    for table in table_list:
        print(table)
 
def main(project_id, instance_id, table_name):
    # [START connecting_to_bigtable]
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    connection = happybase.Connection(instance=instance)
    # [END connecting_to_bigtable]
    print('Listing tables in Bigtable cluster: ', instance_id, ' before deleting')
    list_tables(connection)
    #[START deleting_a_table]
    print('Deleting the {} table.'.format(table_name))
    connection.delete_table(table_name)
    # [END deleting_a_table]
    print('Listing tables in Bigtable cluster: ', instance_id, ' after deleting')
    list_tables(connection)
	

    connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument(
        'instance_id', help='ID of the Cloud Bigtable instance to connect to.')
    parser.add_argument(
        '--table',
        help='Table to destroy.')

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.table)