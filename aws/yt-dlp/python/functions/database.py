import boto3
import os
import logging

client = boto3.client('dynamodb')
table_name = os.environ['TableName']

def get_item(id):
    response = client.get_item(
        TableName=table_name,
        Key = {
            'id': {
                'S': id

            }
        }
    )

    if 'Item' in response:
        return True
    else:
        return False

def put_item(url):
    logging.info(f'Adding item: {url}')
    response = client.put_item(
        TableName = table_name,
        Item = {
            'id': {
                'S': url
            }
        }
    )
    return response