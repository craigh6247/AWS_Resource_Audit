import boto3
from datetime import datetime, timedelta

def get_account_id():
    sts_client = session.client('sts')
    caller_identity = sts_client.get_caller_identity()
    account_id = caller_identity['Account']
    return(account_id)

def audit_ebs_volumes(session):
    ec2 = session.client('ec2')
    try:
        volume_details = []
        volumes = ec2.describe_volumes()['Volumes']
        for volume in volumes:
            volume_id = volume['VolumeId']
            snapshots = ec2.describe_snapshots(OwnerIds=['self'], Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])
            last_snapshot = max((snap['StartTime'] for snap in snapshots['Snapshots']), default=None)

            # Evaluate the last snapshot date
            snapshot_status = "Outdated" if not last_snapshot or (datetime.now(last_snapshot.tzinfo) - last_snapshot > timedelta(days=7)) else "Up-to-date"

            # Check for appropriate tagging
            tags = {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])}
            data_classification = tags.get('DataClassification', 'Not Classified')

            volume_details.append({
                'AccountID': get_account_id,
                'VolumeId': volume_id,
                'Size': volume['Size'],
                'Encrypted': volume['Encrypted'],
                'EncryptionStatus': 'OK' if volume['Encrypted'] else 'Not Encrypted',
                'Type': volume['VolumeType'],
                'IOPS': volume.get('Iops', 'Not Applicable'),  # IOPS is only applicable for IO1 and IO2 volumes
                'LastSnapshot': last_snapshot,
                'SnapshotStatus': snapshot_status,
                'State': volume['State'],
                'AvailabilityZone': volume['AvailabilityZone'],
                'DataClassificationTag': data_classification,
                'Tags': tags
            })
        return volume_details
    except Exception as e:
        return {'error': str(e)}
