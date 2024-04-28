import boto3

def audit_ec2_instances(session):
    ec2 = session.client('ec2')
    inspector = session.client('inspector')
    # Assume SecurityHub and Trusted Advisor are already configured to monitor and report
    try:
        instances_info = []
        reservations = ec2.describe_instances()['Reservations']
        for reservation in reservations:
            for instance in reservation['Instances']:
                instance_id = instance.get('InstanceId')
                instance_details = {
                    'AccountID' : get_account_id,
                    'InstanceId': instance_id,
                    'InstanceType': instance.get('InstanceType'),
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'State': instance['State']['Name'],
                    'SecurityGroups': get_security_group_details(ec2, instance),
                    'Volumes': list_attached_volumes(ec2, instance_id),
                    #'PatchManagement': get_inspector_findings(inspector, instance_id), # Assuming you have specific assessments set up
                    'Tags': instance.get('Tags', [])
                }
                instances_info.append(instance_details)
        return instances_info
    except Exception as e:
        # Log error or handle it as needed
        return str(e)
def get_account_id():
    sts_client = session.client('sts')
    caller_identity = sts_client.get_caller_identity()
    account_id = caller_identity['Account']
    return(account_id)

def get_security_group_details(ec2, instance):
    """Retrieve details for all security groups attached to the instance."""
    security_groups = instance.get('SecurityGroups', [])
    detailed_sgs = []
    for sg in security_groups:
        sg_details = ec2.describe_security_groups(GroupIds=[sg['GroupId']])
        detailed_sgs.append(sg_details['SecurityGroups'][0])  # Assuming the call is successful and SG exists
    return detailed_sgs

def list_attached_volumes(ec2, instance_id):
    """List all volumes attached to the instance and their encryption status."""
    volumes = ec2.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])
    volume_details = []
    for volume in volumes['Volumes']:
        volume_details.append({
            'VolumeId': volume['VolumeId'],
            'Encrypted': volume['Encrypted'],
            'Type': volume['VolumeType'],
            'State': volume['State']
        })
    return volume_details

def get_inspector_findings(inspector, instance_id):
    """Get latest Amazon Inspector findings for the given instance."""
    # Example to get findings, you must set up a proper Inspector assessment target and template
    findings = inspector.list_findings(AssessmentRunArns=['your-assessment-run-arn'])
    findings_details = inspector.describe_findings(FindingArns=findings['FindingArns'])
    return findings_details['Findings']

# Main call to the audit function
if __name__ == '__main__':
    session = boto3.Session(profile_name='your-profile')
    print(audit_ec2_instances(session))
