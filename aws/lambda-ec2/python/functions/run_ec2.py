import boto3

def run_instance(user_data, instance_type):
    client = boto3.client('ec2')
    response = client.run_instances(
        ImageId='ami-09a41e26df464c548',
        InstanceType=instance_type,
        KeyName='nvme-virginia',
        MinCount=1,
        MaxCount=1,
        UserData=user_data,
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
        },
        BlockDeviceMappings=[{
            'DeviceName': '/dev/xvda',
            'Ebs':{
                'DeleteOnTermination': True,
                'VolumeSize': 30
            }
        }]
    )
    return(response)