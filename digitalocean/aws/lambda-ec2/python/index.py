import boto3

def handler(event, context):
    # sam build; sam deploy --no-confirm-changeset
    print(event)
    return({
            'statusCode': 200,
            'body': 'Success'
        })