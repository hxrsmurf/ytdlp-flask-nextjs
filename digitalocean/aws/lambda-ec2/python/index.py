import json

import functions.convert_user_data as convert_user_data
import functions.run_ec2 as run_ec2

# sam build; sam deploy --no-confirm-changeset

def handler(event, context):
    json_event = json.loads(json.dumps(event))
    request_context = json_event['requestContext']
    source_ip = request_context['http']['sourceIp']

    try:
        requested_video_id = json_event['queryStringParameters']['id']
    except:
        return({'statusCode': 200, 'body': 'Not current query string'})

    user_data = convert_user_data.convert(video_id=requested_video_id)
    run_ec2.run_instance(user_data)

    return({
            'statusCode': 200,
            'body': 'Success'
        })