import boto3

def audit_ec2_instances(sesion):
    ec2 = sesion.client('ec2')
    try:
        instances_info = []
        reservations = ec2.describe_instances()['Reservations']
        for reservation in reservations:
            for instance in reservation['Instances']:
                instance_details = {
                    'InstanceId': instance.get('InstanceId'),
                    'InstanceType': instance.get('InstanceType'),
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'State': instance['State']['Name']
                }
                instances_info.append(instance_details)
        return instances_info
    except Exception as e:
        # Log error or handle it as needed
        return str(e)
