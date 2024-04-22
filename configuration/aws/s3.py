import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
import json

def audit_s3_buckets(session):
    client = session.client('s3')
    bucket_details = []

    try:
        buckets = client.list_buckets()['Buckets']

        for bucket in buckets:
            bucket_name = bucket['Name']
            details = {
                'Name': bucket_name,
                'CreationDate': bucket['CreationDate'].isoformat(),
                'BucketPolicy': check_bucket_policy(client, bucket_name),
                'BlockPublicAccess': check_block_public_access(client, bucket_name),
                'BucketACLs': check_bucket_acls(client, bucket_name),
                'Versioning': check_versioning(client, bucket_name),
                'ServerAccessLogging': check_server_access_logging(client, bucket_name),
                'Encryption': check_encryption(client, bucket_name)
            }
            bucket_details.append(details)

        # Optionally, write details to a file
        with open('s3_bucket_details.json', 'w') as f:
            json.dump(bucket_details, f, indent=4)

        return bucket_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def check_bucket_policy(client, bucket_name):
    try:
        policy = client.get_bucket_policy(Bucket=bucket_name)
        return policy['Policy']
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            return "No policy"
        else:
            raise

def check_block_public_access(client, bucket_name):
    try:
        access_block = client.get_public_access_block(Bucket=bucket_name)
        return access_block['PublicAccessBlockConfiguration']
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return "Public access block not configured"
        else:
            raise

def check_bucket_acls(client, bucket_name):
    try:
        acl = client.get_bucket_acl(Bucket=bucket_name)
        return acl['Grants']
    except ClientError as e:
        raise

def check_versioning(client, bucket_name):
    try:
        versioning = client.get_bucket_versioning(Bucket=bucket_name)
        # Check if 'Status' is in the response and return it, otherwise indicate versioning is not enabled
        return versioning.get('Status', "Versioning not enabled")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


def check_server_access_logging(client, bucket_name):
    try:
        logging = client.get_bucket_logging(Bucket=bucket_name)
        return logging['LoggingEnabled'] if 'LoggingEnabled' in logging else "Logging not enabled"
    except ClientError as e:
        raise

def check_encryption(client, bucket_name):
    try:
        encryption = client.get_bucket_encryption(Bucket=bucket_name)
        return encryption['ServerSideEncryptionConfiguration']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            return "Encryption not configured"
        else:
            raise
