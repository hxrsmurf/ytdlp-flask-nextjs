import boto3
import functions.convert_user_data as convert_user_data
import functions.run_ec2 as run_ec2
def handler(event, context):
    # sam build; sam deploy --no-confirm-changeset

    base64UserData = convert_user_data.convert(video_id='RlOB3UALvrQ')
    run_ec2.run_instance(base64UserData)

    return({
            'statusCode': 200,
            'body': 'Success'
        })