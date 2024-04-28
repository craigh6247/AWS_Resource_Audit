import boto3

def audit_vpc(session):
    ec2 = session.client('ec2')
    try:
        vpcs_info = []
        vpcs = ec2.describe_vpcs()['Vpcs']
        for vpc in vpcs:
            vpc_id = vpc['VpcId']
            subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets']
            availability_zones = {subnet['AvailabilityZone'] for subnet in subnets}

            vpc_info = {
                'AccountID' : get_account_id,
                'VPC ID': vpc_id,
                'Is Multi-AZ': len(availability_zones) > 1,
                'Subnets': len(subnets),
                'Availability Zones': list(availability_zones),
                'Security Groups': get_security_groups(ec2, vpc_id),
                'Network ACLs': get_network_acls(ec2, vpc_id),
                'Flow Logs': check_flow_logs(ec2, vpc_id)
            }
            vpcs_info.append(vpc_info)
        return vpcs_info
    except Exception as e:
        return {'error': str(e)}
def get_account_id():
    sts_client = session.client('sts')
    caller_identity = sts_client.get_caller_identity()
    account_id = caller_identity['Account']
    return(account_id)
def get_security_groups(ec2, vpc_id):
    security_groups = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['SecurityGroups']
    return [{'GroupId': sg['GroupId'], 'GroupName': sg['GroupName']} for sg in security_groups]

def get_network_acls(ec2, vpc_id):
    acls = ec2.describe_network_acls(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['NetworkAcls']
    return [{'NetworkAclId': acl['NetworkAclId'], 'IsDefault': acl['IsDefault']} for acl in acls]

def check_flow_logs(ec2, vpc_id):
    flow_logs = ec2.describe_flow_logs(Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}])['FlowLogs']
    return 'Enabled' if flow_logs else 'Not Enabled'

# Main call to the audit function
if __name__ == '__main__':
    session = boto3.Session(profile_name='your-profile')
    print("VPC Audit Results:")
    print(audit_vpc(session))
