import boto3

def audit_security_groups(session):
    ec2 = session.client('ec2')
    issues = []

    try:
        security_groups = ec2.describe_security_groups()['SecurityGroups']
        for sg in security_groups:
            sg_issues = {"SecurityGroupID": sg['GroupId'], "Issues": []}
            # Check for unrestricted SSH or RDP access
            for perm in sg['IpPermissions']:
                # Check for SSH and RDP
                if perm['IpProtocol'] == 'tcp' and 'FromPort' in perm and 'ToPort' in perm:
                    if 22 in range(perm['FromPort'], perm['ToPort'] + 1) or 3389 in range(perm['FromPort'], perm['ToPort'] + 1):
                        for ip in perm['IpRanges']:
                            if ip['CidrIp'] == '0.0.0.0/0':
                                sg_issues["Issues"].append(f"Unrestricted SSH/RDP access on port {perm['FromPort']} to {perm['ToPort']}")
                        for ip in perm.get('Ipv6Ranges', []):
                            if ip['CidrIpv6'] == '::/0':
                                sg_issues["Issues"].append(f"Unrestricted SSH/RDP IPv6 access on port {perm['FromPort']} to {perm['ToPort']}")

                # Check for large port ranges
                if perm['IpProtocol'] == 'tcp' and ('FromPort' in perm and 'ToPort' in perm) and (perm['ToPort'] - perm['FromPort'] > 100):
                    sg_issues["Issues"].append(f"Large port range open: {perm['FromPort']}-{perm['ToPort']}")

            if sg_issues["Issues"]:
                issues.append(sg_issues)

        return issues if issues else "No issues found."
    except Exception as e:
        return {'error': str(e)}
