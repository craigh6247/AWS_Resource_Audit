import boto3
from botocore.exceptions import ClientError

def audit_iam_practices(session):
    iam = session.client('iam')
    results = {
        'roles': [],
        'users': []
    }

    try:
        # Audit IAM roles
        results['roles'] = audit_roles(iam)
        
        # Audit IAM users
        results['users'] = audit_users(iam)

        return results

    except ClientError as e:
        return {'error': str(e)}
def get_account_id():
    sts_client = session.client('sts')
    caller_identity = sts_client.get_caller_identity()
    account_id = caller_identity['Account']
    return(account_id)

def audit_roles(iam):
    role_issues = []
    roles = iam.list_roles()['Roles']
    for role in roles:
        # Example check for attached policies to ensure roles are using least privilege
        policies = iam.list_attached_role_policies(RoleName=role['RoleName'])['AttachedPolicies']
        if not policies:
            role_issues.append({
                'AccountID': get_account_id,
                'RoleName': role['RoleName'],
                'Issue': 'No attached policies, may not be following least privilege.'
            })

    return role_issues

def audit_users(iam):
    user_details = []
    users = iam.list_users()['Users']
    for user in users:
        # Check for MFA devices to ensure security
        mfa_devices = iam.list_mfa_devices(UserName=user['UserName'])['MFADevices']
        mfa_status = 'Enabled' if mfa_devices else 'Not Enabled'
        user_details.append({
            'AccountID': get_account_id,
            'UserName': user['UserName'],
            'MFAStatus': mfa_status
        })

    return user_details
