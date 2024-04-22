# AWS Compliance Audit

This a project designed to help with platfrom auidting of services based on AWS Secruity and Best Practices.


## Technology Stack

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Boto3**: The Amazon Web Services (AWS) SDK for Python. It allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2.
- **Uvicorn**: A lightning-fast ASGI server, built on uvloop and httptools.

## Folder Structure

```
project_root/
│
├── main.py             # Main FastAPI application entry point
└── config/
    ├── __init__.py     # Makes config a Python package
    ├── configuration/
        ├── __init__.py # Makes configuration a sub-package within config
        └── aws/
            ├── __init__.py # Makes aws a sub-package within configuration
            ├── s3.py       # Module for Amazon S3 operations
            └── ec2.py       # Module for Amazon EC2 operations
        └── azure/
```

### main.py

This is the entry point for the FastAPI application. It includes routing and the setup for the API server.

### config/configuration/aws/

This directory contains the modules specific to AWS operations:
- **s3.py**: Handles the interaction with Amazon S3, such as listing buckets and checking configurations.
- **ec2.py**: Manages Amazon EC2 instance interactions, such as auditing and listing instances.

## Running the Application

To run the application, ensure you have Python installed along with FastAPI and Uvicorn. You can start the server using the following command:

```bash
uvicorn main:app --reload
```

This command will start the FastAPI application with hot reloading enabled.

## API Usage

After starting the application, you can access the API at `http://127.0.0.1:8000`. The API endpoints include:

- `/configuration/aws/s3/`: Interacts with Amazon S3.
- `/configuration/aws/ec2/`: Interacts with Amazon EC2.

## License

Specify the license under which the project is made available.
