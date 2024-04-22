from fastapi import FastAPI, HTTPException
import boto3
from configuration.aws import s3, ec2, ebs, vpc  # Updated import path

app = FastAPI()

# Initialize a Boto3 Session
session = boto3.Session(
     profile_name='ob'
)

@app.get("/configuration/aws/{service}/")
async def get_aws_configuration(service: str):
    service_map = {
        "s3": s3.audit_s3_buckets,
        "ec2": ec2.audit_ec2_instances,
        "ebs": ebs.audit_ebs_volumes,
        "vpc": vpc.audit_vpc,
    }

    if service not in service_map:
        raise HTTPException(status_code=404, detail="Service not supported")

    try:
        # Call the corresponding function from the service module
        response = service_map[service](session)
        return response
    except HTTPException as e:
        # Pass along HTTPException raised by service modules
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
