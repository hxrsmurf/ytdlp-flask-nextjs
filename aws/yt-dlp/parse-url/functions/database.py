import boto3
import os
import logging
import json

client = boto3.client('dynamodb')

def get_item(id, download_type, table_name):
    logging.info('Getting item')
    response = client.get_item(
        TableName=table_name,
        Key = {
            'id': {
                'S': id
            }
        }
    )

    if 'Item' in response:
        if download_type == 'playlist':
            return response['Item']['latest_video_original_url']['S']
        elif download_type == 'video':
            return response['Item']['like_count']['S']
    else:
        return False

def put_item(item, table_name):
    response = client.put_item(
        TableName = table_name,
        Item = item
    )
    return response

def put_item_channel(original_url, url_info, table_name):
    logging.info(f'Adding {original_url}')

    item = {
        'id': {
            'S': original_url
        },
    }

    for key, value in url_info.items():
        value_type = type(value)
        if key == 'id':
            # The yt-dlp id is the new YouTube handle @. I don't necessarily want that as my primary key/id
            item['external_id'] = {
                'S' : value
            }
        elif value_type == str or value_type == int:
            item[key] = {
                'S': str(value)
            }
        elif value_type == list:
            item[key] = {
                'S': str(value)
            }
        elif value_type == tuple:
            item[key] = {
                'S': ''.join(value)
            }
        else:
            logging.error(f'Cannot convert {key} {value}')

    put_item(item, table_name)

def put_item_video(id, url_info, table_name):
    logging.info(f'Adding {id}')

    item = {
        'id': {
            'S': id
        },
    }

    for key, value in url_info.items():
        value_type = type(value)
        if value_type == str or value_type == int:
            item[key] = {
                'S': str(value)
            }
        elif value_type == list:
            item[key] = {
                'S': str(value)
            }
        elif value_type == tuple:
            item[key] = {
                'S': ''.join(value)
            }
        elif not value:
            item[key] = {
                'NULL': True
            }
        else:
            logging.error(f'Cannot convert {key} {value} {value_type}')

    put_item(item, table_name)