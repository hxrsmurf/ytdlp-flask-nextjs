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
        return response['Item']['video_id']['S']
    else:
        return False

def put_item(url, info, video_id):
    logging.info(f'Adding item: {url}')
    response = client.put_item(
        TableName = table_name,
        Item = {
            'id': {
                'S': url
            },
            'video_id': {
                'S': video_id
            },
            'info':{
                'S': json.dumps(info)
            }
        }
    )
    return response