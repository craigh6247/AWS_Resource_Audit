from fastapi import FastAPI, HTTPException
import boto3
import json
import logging
from configuration.aws import s3 as s3_audit, ec2, ebs, vpc, security_groups, iam

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# Initialize a Boto3 Session
session = boto3.Session(profile_name='ob')
s3_client = session.client('s3')
sts_client = session.client('sts')
bucket_name = 'cloudstatustesting'  # Replace with your actual S3 bucket name

@app.get("/configuration/aws/{service}/")
async def get_aws_configuration(service: str):
    service_map = {
        "s3": s3_audit.audit_s3_buckets,
        "ec2": ec2.audit_ec2_instances,
        "ebs": ebs.audit_ebs_volumes,
        "vpc": vpc.audit_vpc,
        "sg": security_groups.audit_security_groups,
        "iam": iam.audit_iam_practices,
    }

    if service not in service_map:
        raise HTTPException(status_code=404, detail="Service not supported")

    try:
        # Call the corresponding function from the service module
        response = service_map[service](session)
        
        # Convert the response data to JSON
        response_json = json.dumps(response, default=str)  # Ensuring datetime is converted to string if present
        
        # Retrieve the AWS account ID from the caller identity
        caller_identity = sts_client.get_caller_identity()
        account_id = caller_identity['Account']
        
        # Construct the filename
        filename = f"Configuration-AWS-{account_id}-{service}.json"
        # Write the JSON data to S3
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=response_json)
        
        return {"message": f"Data written successfully to {filename} in bucket {bucket_name}"}
    except Exception as e:
        # Catch any other exception and raise an HTTPException
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, loglevel="debug")
