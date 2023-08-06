import json
import os
import boto3

# from botocore.exceptions import NoCredentialsError


import boto3

def wasabi_auth(ACCESS_KEY, WASABI_SECRET):
    """
    Creates an authenticated client for interacting with an S3 bucket hosted on the Wasabi cloud storage service.
    
    Args:
    ACCESS_KEY (str): Wasabi Access Key
    WASABI_SECRET (str): Wasabi Secret Key
    
    Returns:
    s3 (boto3.client): An authenticated client object for interacting with Wasabi S3
    
    """

    # Set the Wasabi Access Key and Secret Key
    WASABI_ACCESS_KEY = ACCESS_KEY
    WASABI_SECRET_KEY = WASABI_SECRET

    # Create a session object using the Wasabi Access Key and Secret Key
    session = boto3.Session(
        aws_access_key_id=WASABI_ACCESS_KEY,
        aws_secret_access_key=WASABI_SECRET_KEY,
    )
    
    # Create an S3 client object using the session object and the Wasabi endpoint URL
    s3 = session.client(
        "s3", endpoint_url="https://s3.ap-southeast-1.wasabisys.com"
    )
    
    # Return the S3 client object
    return s3

def wasabi_auth_client():
    pass