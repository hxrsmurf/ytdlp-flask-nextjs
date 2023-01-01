import boto3
import os

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