# import json
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import NoCredentialsError, ClientError
from wasabit.wasabi_auth import wasabi_auth
import os
from botocore.exceptions import NoCredentialsError


def wasabi_upload(s3, bucket_name, wasabi_path, local_file_path):
    """
    function to upload files from local to wasabi, it will create folder path for the dataset that we
    are wroking on and add the files from local path.

    params:
    s3 : Element which returns after authentication using wasabi_auth function
    bucket_name: dev-data or prod-data
    wasabi_path: dataset_name + (data path from monorepo) | Ex: agcensus/raw/andhra_pradesh/anantapur/data.csv
    local_file_path: path of file in the system in which processing is being done.
    """
    for bucket in s3.list_buckets()["Buckets"]:
        if bucket["Name"] == bucket_name:
            print(bucket_name + " bucket already exists")
            wasabi_bucket = bucket_name
            pass
        else:
            wasabi_bucket = s3.create_bucket(Bucket=bucket_name)

    def upload_to_wasabi(file_name, bucket, data):
        """
        Function to upload a dataset on to the wasabi cloud
        """
        try:
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    data = open(local_file_path, "rb")
    wasabi_bucket = bucket_name
    # invoking the upload function to wasabi or amazon s3.
    upload_to_wasabi(wasabi_path, wasabi_bucket, data)
    print("file uploaded to wasabi on this path: ", wasabi_path)



def upload_to_wasabi(folder_path: str, bucket_name: str, wasabi_path: str, access_key = None, secret_key = None) -> None:
    """
    Uploads all files present in a specific folder to a specified Wasabi bucket and subfolder or prefix.
    :param folder_path: The path of the folder containing the files to be uploaded.
    :param bucket_name: The name of the Wasabi bucket where the files will be uploaded.
    :param wasabi_path: The prefix or subfolder within the bucket where the files will be uploaded.
    :param access_key: The Wasabi access key.
    :param secret_key: The Wasabi secret key.
    """
    transfer_config = TransferConfig(
    multipart_threshold=1024 * 25,  # 25MB
    max_concurrency=10,
    num_download_attempts=10,
)
    try:
        # create an S3 client
        s3 = wasabi_auth(access_key,secret_key)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                remote_file = file_path.split('/')[-1]
                remote_file = wasabi_path + remote_file
                # upload the file
                s3.upload_file(file_path, bucket_name,remote_file,Config=transfer_config)
                print(f'{file_path} is uploaded to {remote_file}')
    except NoCredentialsError as e:
        print("Credentials not found, please check your access key and secret key.")
    except ClientError as e:
        if e.response['Error']['Code'] == "InvalidAccessKeyId":
            print("Invalid access key, please check your access key.")
        elif e.response['Error']['Code'] == "SignatureDoesNotMatch":
            print("Invalid secret key, please check your secret key.")
        else:
            print(f'An error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

        

def file_upload_to_wasabi(csv_file_path: str, bucket_name: str, wasabi_path: str, access_key, secret_key) -> None:
    """
    Uploads a specific CSV file to a specified Wasabi bucket and subfolder or prefix.
    :param csv_file_path: The full path of the CSV file to be uploaded.
    :param bucket_name: The name of the Wasabi bucket where the file will be uploaded.
    :param wasabi_path: The prefix or subfolder within the bucket where the file will be uploaded.
    :param access_key: The Wasabi access key.
    :param secret_key: The Wasabi secret key.
    """
    transfer_config = TransferConfig(
        multipart_threshold=1024 * 25,  # 25MB
        max_concurrency=10,
        num_download_attempts=10,
    )
    try:
        # create an S3 client
        s3 = wasabi_auth(access_key,secret_key)
        # get the file name from the full path
        file_name = os.path.basename(csv_file_path)
        remote_file = wasabi_path + file_name
        # upload the file
        s3.upload_file(csv_file_path, bucket_name, remote_file, Config=transfer_config)
        print(f'{csv_file_path} is uploaded to {remote_file}')
    except NoCredentialsError as e:
        print("Credentials not found, please check your access key and secret key.")
    except ClientError as e:
        if e.response['Error']['Code'] == "InvalidAccessKeyId":
            print("Invalid access key, please check your access key.")
        elif e.response['Error']['Code'] == "SignatureDoesNotMatch":
            print("Invalid secret key, please check your secret key.")
        else:
            print(f'An error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')