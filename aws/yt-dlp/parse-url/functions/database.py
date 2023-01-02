import boto3
import os
import logging
import json

client = boto3.client('dynamodb')
table_name = os.environ['TableName']

def get_item(id):
    logging.info(f'Getting item: {id}')
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

def put_item(id, info):
    logging.info(f'Adding item: {id}')
    response = client.put_item(
        TableName = table_name,
        Item = {
            'id': {
                'S': id
            },
            'info':{
                'S': json.dumps(info)
            }
        }
    )
    return response