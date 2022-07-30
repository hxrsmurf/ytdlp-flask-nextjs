import boto3

def handler(event, context):
    # sam build; sam deploy --no-confirm-changeset
    client = boto3.client('ec2')

    response = client.run_instances(
        ImageId='ami-09a41e26df464c548',
        InstanceType='t2.micro',
        KeyName='nvme-virginia',
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=[{
            'AssociatePublicIpAddress': True,
            'DeleteOnTermination': True,
            'DeviceIndex': 0,
            'SubnetId': 'subnet-0d8fa1295c21f9ead'
        }],
        InstanceMarketOptions={
            'MarketType': 'spot',
            'SpotOptions': {
                'SpotInstanceType' : 'one-time'
            }
        }
    )

    print(response)
    return({
            'statusCode': 200,
            'body': 'Success'
        })