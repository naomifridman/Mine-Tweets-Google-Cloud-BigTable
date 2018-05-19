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
# usage: words_to_HBase_table_in_BigTable.py [-h] [--table TABLE] project_id instance_id

import argparse

from google.cloud import bigtable
from google.cloud import happybase


def main(project_id, instance_id, table_name):
    # [START connecting_to_bigtable]
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    connection = happybase.Connection(instance=instance)
    # [END connecting_to_bigtable]

    try:
        # [START creating_a_table]
        print('Creating the {} table.'.format(table_name))
        column_family_name = 'cf1'
        connection.create_table(
            table_name,
            {
                column_family_name: dict()  # Use default options.
            })
        # [END creating_a_table]

        # [START writing_rows]
        print('Writing some words to table: ', table_name)
        table = connection.table(table_name)
        column_name = '{fam}:words'.format(fam=column_family_name)
        print('column_name ', column_name)
		
        # Do your staff here to create words....
        #
        # For the test we simply hardcode a list of words
        words = [
            'IamWods1',
            'SheIsWord2',
            'HeIsWord3',
        ]

        for i, value in enumerate(words):
            # Note: for large lists of words, this method might have poor performance
            # Since rows are stored in sorted order by key,
            # sequential keys can result in poor distribution of operations
            # across nodes.
            #
            # For more information about how to design a Bigtable schema for
            # the best performance, see the documentation:
            #
            #     https://cloud.google.com/bigtable/docs/schema-design
            print('Writing  word to the table.',i,value)
            row_key = 'words{}'.format(i)
            table.put(row_key, {column_name: value})
        # [END writing_rows]


    finally:
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
        help='Table to create ans write words into it.',
        default='words_table_example')

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.table)