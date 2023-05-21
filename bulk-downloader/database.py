import boto3
import os

client = boto3.client('dynamodb')

table = "yt-dlp-channels-tf"

response = client.scan(
    TableName = table,
)

channels = response['Items']

with open('channels.txt', 'w') as f:
    for c in channels:
        url = c['webpage_url']['S']
        try:
            f.write(url + '\n')
        except:
            print(url)