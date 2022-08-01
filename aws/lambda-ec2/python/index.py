import json
import os

import functions.convert_user_data as convert_user_data
import functions.run_ec2 as run_ec2

# sam build; sam deploy --no-confirm-changeset

def handler(event, context):
    json_event = json.loads(json.dumps(event))
    request_context = json_event['requestContext']
    source_ip = request_context['http']['sourceIp']

    restricted_ips = os.environ['RESTRICTED_IPS']

    if not source_ip in restricted_ips:
        return({'statusCode': 401, 'body': 'Not Authorized'})

    try:
        requested_video_id = json_event['queryStringParameters']['id']
        #requested_bunny_guid = json_event['queryStringParameters']['guid']
    except:
        return({'statusCode': 200, 'body': 'Not current query string'})

    user_data = convert_user_data.convert(video_id=requested_video_id, bunnycdn_guid=None)
    testing_instance_types = ['c5.4xlarge']
    for type in testing_instance_types:
        print(run_ec2.run_instance(user_data=user_data, instance_type=type))

    return({
            'statusCode': 200,
            'body': 'Success'
        })
